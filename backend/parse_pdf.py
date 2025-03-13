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

FOLDER_PROCESSED = "processed"
FOLDER_VECTOR_DB = "vector_db"
os.makedirs(FOLDER_PROCESSED, exist_ok=True)
os.makedirs(FOLDER_VECTOR_DB, exist_ok=True)

# Where we will put the generated topics as a binary file.
LOCAL_DATA_STORE_FOLDER = 'generated_topics'


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

def save_to_file(file_name, generated_topics_by_page, extracted_text_by_page):

    # Create the upload folder if it doesn't exist
    if not os.path.exists(LOCAL_DATA_STORE_FOLDER):
        os.makedirs(LOCAL_DATA_STORE_FOLDER)

    file_path_and_name = LOCAL_DATA_STORE_FOLDER + "/" + file_name + ".pkl"

    message_payload = (generated_topics_by_page, extracted_text_by_page)

    with open(file_path_and_name, "wb") as file:
        pickle.dump(message_payload, file)

def parse_pdf(pdf_path):
    file_name = os.path.basename(pdf_path).replace(".pdf", "") # Remove file extension for file name.
    output_path = os.path.join(FOLDER_PROCESSED, file_name + ".json")

    extracted_text_by_page = get_text_from_pdf(pdf_path)
    print('extracted_pages_text:')
    print(extracted_text_by_page)
    generated_topics_by_page = generate_topics_from_text(extracted_text_by_page)
    print('topics:')
    for topic in generated_topics_by_page[1]: 
        print(topic)

    save_to_file(file_name, generated_topics_by_page, extracted_text_by_page)
    
    return generated_topics_by_page