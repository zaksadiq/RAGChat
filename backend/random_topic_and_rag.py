from parse_pdf import LOCAL_DATA_STORE_FOLDER
#
import random
import os
import pickle
import json
import chromadb



def get_data_from_binary():
    binary_folder_path = LOCAL_DATA_STORE_FOLDER + "/"
    binary_file = binary_folder_path + "variables_binary.pkl"

    with open(binary_file, "rb") as file:
        message_payload_received = pickle.load(file)

    return message_payload_received


def pick_random_topic(generated_pages_topics):
    selected_random_topic = random.choice(range(7)) # Supporting 7 topics - TODO: Add NUMBER_OF_TOPICS constant globally.
    print('Random topic:')
    print(selected_random_topic)
    print(type(selected_random_topic))
    return selected_random_topic


# The method to be called. 
# Expects a chromadb_client global variable.
def select_random_topic_and_do_rag(chromadb_client):
    # Get data from parse_pdf.py (pickled / variables in binary)
    message_payload = get_data_from_binary()
    generated_topics_by_page = message_payload[0]
    extracted_text_by_page = message_payload[1]
    embeddings_model = message_payload[2]
    print('generated_topics_by_page: ', generated_topics_by_page)
    #
    vector_database_collection = chromadb_client.get_collection("pdf_chunks")

    # Deal with topics. (Pick)
    randomly_selected_topic = pick_random_topic(generated_topics_by_page)
    print('randomly selected topic: ', randomly_selected_topic)


    # Query vector database for randomly selected topic.
    topic_words = generated_topics_by_page[2][randomly_selected_topic]
    print('topic words: ', topic_words)
    query = " ".join(topic_words)
    query = "Get the section of the text corresponding most to the following words : " + query + "."
    print('query: ', query)
    query_embeddings = embeddings_model.encode(query).tolist()
    
    # Get result of relevant documents.
    results = vector_database_collection.query(
        query_embeddings=query_embeddings, # Dummy embeddings as not needed. Could be useful in future.
        n_results=1, # Large number to get all matches.
        # where={f"topic_{randomly_selected_topic}": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id. Available here in-case future work requires it.
    )
    
    documents = results["documents"]
    print('documents: ', documents)
    metadatas = results["metadatas"]
    print('metadatas: ', metadatas)
    similarities = results["distances"] # Similarity between query embeddings and embeddings for result document in the vector database.
    print('similarities: ', similarities)
    
    print('printing documents, ', len(documents[0]))
    relevant_doc_based_on_random_topic = documents[0]
    print('got document: ', relevant_doc_based_on_random_topic)
    
    return relevant_doc_based_on_random_topic