import sys
import os

import pdfplumber
from gensim import corpora, models
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

import random

import pickle

from sentence_transformers import SentenceTransformer
import chromadb
import json

# Where we will put the generated topics as a binary file.
LOCAL_DATA_STORE_FOLDER = 'data_store'


# PDF Plumber text extraction on file.
def get_text_from_pdf(pdf_path):
    extracted_text_by_page = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract_text returns all page char objects as a single string. I put it into the array, where each page is a new entry.
            current_page_text = page.extract_text() 
            extracted_text_by_page.append(current_page_text)
    return extracted_text_by_page

def tokenise_text(text_to_tokenise):
    stop_words = set(stopwords.words('english'))
    
    # Split page of pdf into sentences, then break these down into words and filter punctuation and 'stop words' (inconsequential words for our purposes.)
    #
    ## Split into sentences first to give order to words once tokenised, so they have structure and make more sense.
    ## (Yet we just append all words into one array, so this feature isn't actually used, due to a technical limitation (corpus.Dictionary could not support a list of lists of lists, so we eventually create a list of lists instead).)
    sentences = sent_tokenize(text_to_tokenise)
    ##
    words = []
    for sentence in sentences: 
        for word in word_tokenize(sentence.lower()):  
            if word.isalpha() and word not in stop_words:  #alnum => alpha numeric (to remove punctuation.)
                words.append(word)  
    #

    return words

def generate_topics_from_text(array_of_extracted_text_by_page):
    # Currently works with all words on each page, but for more focused discussions we could work by sentence on each page, eventually, once technical details and implementation are worked out.
    
    # Get words on each page.
    tokenised_pages = [tokenise_text(page_text_string) for page_text_string in array_of_extracted_text_by_page]

    # Dictionary and corpus necessary for LDA.
    dictionary = corpora.Dictionary(tokenised_pages) # Takes a list of lists. In our case a list of pages with a list of words.
    corpus = [dictionary.doc2bow(words) for words in tokenised_pages] # Convert words array into a 'bag-of-words' format.

    # Train LDA model.
    NUM_TOPICS = 7
    lda = models.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary)
    # Get topics of each page.
    # Results in an array of arrays, where each array item is a page of the pdf,
    # and this is an array of tuples(?), with each tuple being a topic id, followed by its
    # relevance score for that page.
    generated_topics = [lda[doc_bow] for doc_bow in corpus]
    printed_topics = lda.print_topics(num_topics=7, num_words=3)
    for i, topics in enumerate(generated_topics):
        print(f"Page {i+1} topics: {topics}")
    return [generated_topics, printed_topics]

def save_collection(vector_database_collection):
    data = vector_database_collection.get()
    file_path = LOCAL_DATA_STORE_FOLDER + "/" + "data_from_collection.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

def save_to_file(file_name, generated_topics_by_page, extracted_text_by_page, embedding_model, vector_database_collection):
    # Create the upload folder if it doesn't exist
    if not os.path.exists(LOCAL_DATA_STORE_FOLDER):
        os.makedirs(LOCAL_DATA_STORE_FOLDER)

    file_path_and_name = LOCAL_DATA_STORE_FOLDER + "/" + "variables_binary.pkl"

    message_payload = (generated_topics_by_page, extracted_text_by_page, embedding_model)

    with open(file_path_and_name, "wb") as file:
        pickle.dump(message_payload, file)

    save_collection(vector_database_collection)

def parse_pdf(pdf_path, chromadb_client):
    # Get text from pdf and generate topics.
    
    file_name = os.path.basename(pdf_path).replace(".pdf", "") # Remove file extension for file name.
    # output_path = os.path.join(FOLDER_PROCESSED, file_name + ".json")

    extracted_text_by_page = get_text_from_pdf(pdf_path)
    print('extracted_pages_text: ', extracted_text_by_page)

    generated_topics_by_page = generate_topics_from_text(extracted_text_by_page)
    print('topics:')
    for topic in generated_topics_by_page[1]: 
        print(topic)
    
    #

    # Get chunks from LDA 'processed' pages.
    # all_chunks = []
    # for i, page in enumerate(generated_topics_by_page[0]): # Index 0 is generated topics. (1 is printed topics.)
    #     # Each i is a new page
    #     print('page: ', page)
    #     for chunk in page:
    #         print('chunk: ', chunk)
    #         all_chunks.append(chunk) # Should be an array of tuples, where each tuple is a topic and relevancy score of the topic, the chunk corresponds to.
    #
    #   Not necessary, I just figured out.
    #

    # 13 March 2025.
    # RAG items:
    ## Embeddings
    ## Vector Database
    
    # Embeddings
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = embedding_model.encode(extracted_text_by_page)
    print('embeddings shape: ', embeddings.shape)
    embeddings = embeddings.tolist()
    
    # Vector Database
    vector_database_client = chromadb_client
    vector_database_collection = vector_database_client.create_collection(name="pdf_chunks")
    # PDF page text strings will each be our chunks.
    for i, page_text_string in enumerate(extracted_text_by_page):
        
        topics = generated_topics_by_page[0][i]
        topic_keys_flags = [0,0,0,0,0,0,0] # Supports 7 topics.
        topic_keys_relevance = [0,0,0,0,0,0,0]
        # Switch bits for topics that are active. (Python doesn't have a switch/case statement.)
        for topic in topics:
            if (topic[0] == 0): # First index of topic is id integer.
                topic_keys_flags[0] = 1
                topic_keys_relevance[0] = topic[1] # Relevance score (float).
            elif (topic[0] == 1):
                topic_keys_flags[1] = 1
                topic_keys_relevance[1] = topic[1]
            elif (topic[0] == 2):
                topic_keys_flags[2] = 1
                topic_keys_relevance[2] = topic[1]
            elif (topic[0] == 3):
                topic_keys_flags[3] = 1
                topic_keys_relevance[3] = topic[1]
            elif (topic[0] == 4):
                topic_keys_flags[4] = 1
                topic_keys_relevance[4] = topic[1]
            elif (topic[0] == 5):
                topic_keys_flags[5] = 1
                topic_keys_relevance[5] = topic[1]
            elif (topic[0] == 6):
                topic_keys_flags[6] = 1
                topic_keys_relevance[6] = topic[1]
        
        vector_database_collection.add(
            embeddings=[embeddings[i]],
            documents=[page_text_string],
            ids=[f"{i}"],
            # Chunks are currently pages of the document.
            metadatas=[{
                "chunk_id": i,
                # "chunk_text": page_text_string,# Put page_text in metadata too to help in-case it has to be got at same time as other metadata (single query). 
                # "chunk_topics": json.dumps(generated_topics_by_page[0][i]), # Also 'serialise'? the topics/relevance tuples list as a JSON string.
                "topic_0": topic_keys_flags[0],
                "topic_1": topic_keys_flags[1],
                "topic_2": topic_keys_flags[2],
                "topic_3": topic_keys_flags[3],
                "topic_4": topic_keys_flags[4],
                "topic_5": topic_keys_flags[5],
                "topic_6": topic_keys_flags[6],
                "topic_0_relevance": topic_keys_relevance[0],
                "topic_1_relevance": topic_keys_relevance[1],
                "topic_2_relevance": topic_keys_relevance[2],
                "topic_3_relevance": topic_keys_relevance[3],
                "topic_4_relevance": topic_keys_relevance[4],
                "topic_5_relevance": topic_keys_relevance[5],
                "topic_6_relevance": topic_keys_relevance[6]
                }] 
        )

    #


    # Save for the random_topic_and_rag.py file to pick up.

    save_to_file(file_name, generated_topics_by_page, extracted_text_by_page, embedding_model, vector_database_collection)

    #

    return generated_topics_by_page