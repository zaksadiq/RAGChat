from parse_pdf import LOCAL_DATA_STORE_FOLDER

import random
import os
import pickle
import json
import chromadb


def get_data_from_binary():
    binary_folder_path = LOCAL_DATA_STORE_FOLDER + "/"
    # binary_files = [os.path.join(binary_folder_path, f) for f in os.listdir(binary_folder_path)]
    # # Get latest file.
    # latest = max(binary_files, key=os.path.getctime)
    # print('latest file:')
    # print(latest)
    binary_file = binary_folder_path + "variables_binary.pkl"

    with open(binary_file, "rb") as file:
        message_payload_received = pickle.load(file)

    return message_payload_received

# def get_vector_database_collection_data():
#     file_path = LOCAL_DATA_STORE_FOLDER + "/" + "data_from_collection.json"
#     data = None
#     with open(file_path, "r") as file:
#         print('doing json load.')
#         data = json.load(file)
#         print('done json load.')
#     return data

# def rebuild_vector_database_collection(chromadb_client):
#     print('creating chromadb client.')
#     vector_database_client = chromadb_client
#     print('created chromadb client.')
#     print('creating collection.')
#     vector_database_collection = vector_database_client.create_collection(name="pdf_chunks_rebuild")
#     print('created collection.')
#     vector_database_collection.add(
#         embeddings=data["embeddings"],
#         documents=data["documents"],
#         ids=data["ids"],
#         metadatas=data["metadatas"]
#     )
#     print('added to collection.')
#     return vector_database_collection

def pick_random_topic(generated_pages_topics):
    # Create a set (because this will only allow unique additions, unlike an Array/List.)
    # all_topics_in_one_set = set()
    # for page in generated_pages_topics:
    #     for topic in page:
    #         all_topics_in_one_set.add(topic[0]) # Array index 0 contains the topic ID.

    # selected_random_topic = random.choice(list(all_topics_in_one_set))
    selected_random_topic = random.choice(range(7)) # Supporting 7 topics - TODO: Add NUMBER_OF_TOPICS constant globally.
    print('Random topic:')
    print(selected_random_topic)
    print(type(selected_random_topic))
    
    return selected_random_topic

def retrieve_page_from_topic(generated_topics_by_page, randomly_selected_topic):
    highest_relevance_score = 0
    most_relevant_section_of_any_page = None
    most_relevant_section_page = None
    page_id = 0
    page_section_id = 0
    for page in generated_topics_by_page:
        print('new page', page)
        print('id', page_id)
        if (isinstance(page[0][0], str)): # Account for strange entry at end of pages array with strings.
            print('skipping.')
            continue # skip this page
        for page_section_topics in page: 
            print('page_section_topics', page_section_topics)
            for topic in page_section_topics:
                # print('topic', topic)
                # print('typeof', type(topic))
                # print('typeof', type(topic[0]))
                if (topic[0] == randomly_selected_topic[0]): # Compare topic IDs.
                    relevance_score = topic[1]
                    # print('relevance_score', relevance_score)
                    if (relevance_score > highest_relevance_score): # Compare relevance score of topic on this particular page with the highest found.
                        highest_relevance_score = relevance_score
                        most_relevant_section_of_any_page = page_section_id
                        most_relevant_section_page = page_id
                        
            page_section_id += 1
        page_id += 1
    # Give back the page with the highest topic relevance score. TODO: Amend to consider unlikely edge case of two pages having the same relevance score.
    return page_id

def select_random_and_do_rag(chromadb_client):
    # Get data from parse_pdf.py (pickled / variables in binary)
    message_payload = get_data_from_binary()
    generated_topics_by_page = message_payload[0]
    extracted_text_by_page = message_payload[1]
    embeddings_model = message_payload[2]
    print('generated_topics_by_page: ', generated_topics_by_page)
    #
    # Rebuild vector_database_collection from parse_pdf.py (data_from_collection.json)
    vector_database_collection = chromadb_client.get_collection("pdf_chunks")
    # vector_database_collection_data = get_vector_database_collection_data()
    # vector_database_collection = rebuild_vector_database_collection(chromadb_client)

    # Deal with topics. (Pick, get relevant chunk/page)
    randomly_selected_topic = pick_random_topic(generated_topics_by_page)
    print('randomly selected topic: ', randomly_selected_topic)

    # most_relevant_page = retrieve_page_from_topic(generated_topics_by_page, randomly_selected_topic)
    # print('got most relevant page: ', most_relevant_page)

    # relevant_text_for_randomly_selected_topic = extracted_text_by_page[most_relevant_page]
    # print('text of most relevant: ', extracted_text_by_page[most_relevant_page])
    #

    # Query vector database for randomly selected topic.
    ## Have to do it manually due 
    results = vector_database_collection.query(
        query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
        n_results=10000, # Large number to get all matches.
        where={f"topic_{randomly_selected_topic}": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    )
    # if (randomly_selected_topic == 0):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_0": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    # elif (randomly_selected_topic == 1):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_1": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    # elif (randomly_selected_topic == 2):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_2": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    # elif (randomly_selected_topic == 3):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_3": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    # elif (randomly_selected_topic == 4):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_4": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    # elif (randomly_selected_topic == 5):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_5": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    # elif (randomly_selected_topic == 6):
    #     results = vector_database_collection.query(
    #         query_embeddings=[[0]*384], # Dummy embeddings as not needed. Could be useful in future.
    #         n_results=10000, # Large number to get all matches.
    #         where={"topic_6": {"$eq": 1} } # Get chunks where the topics contain an element with random_topic's id as the topic id.
    #     )
    
    documents = results["documents"]
    # print('documents: ', documents)
    metadatas = results["metadatas"]
    print('metadatas: ', metadatas)
    similarities = results["distances"] # Similarity between query embeddings and embeddings for result document in the vector database.
    print('similarities: ', similarities)
    
    highest_relevance_score = 0
    highest_relevance_score_id = None
    for chunk_metadata in metadatas[0]:
        chunk_id = chunk_metadata["chunk_id"]
        topic_relevance_score = chunk_metadata[f"topic_{randomly_selected_topic}_relevance"]
        if (topic_relevance_score > highest_relevance_score):
            highest_relevance_score = topic_relevance_score
            highest_relevance_score_id = chunk_id
    
    print('highest score: ', highest_relevance_score)
    print('highest score id: ', highest_relevance_score_id)
        # Get chunk for highest relevancy score.
    print('printing documents, ', documents[0][highest_relevance_score_id])
    return documents[0][highest_relevance_score_id]
    # return documents[]
    #

    # return relevant_text_to_randomly_selected_topic