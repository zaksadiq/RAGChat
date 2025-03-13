from parse_pdf import LOCAL_DATA_STORE_FOLDER

import random
import os
import pickle


def get_data_from_binary():
    binary_folder_path = LOCAL_DATA_STORE_FOLDER + '/'
    binary_files = [os.path.join(binary_folder_path, f) for f in os.listdir(binary_folder_path)]
    # Get latest file.
    latest = max(binary_files, key=os.path.getctime)
    print('latest file:')
    print(latest)

    with open(latest, "rb") as file:
        generated_topics_by_page = pickle.load(file)

    return generated_topics_by_page

def pick_random_topic(generated_pages_topics):
    # Create a set (because this will only allow unique additions, unlike an Array/List.)
    all_topics_in_one_set = set()
    for page in generated_pages_topics:
        for topic in page:
            all_topics_in_one_set.add(topic[0]) # Array index 0 contains the topic ID.

    selected_random_topic = random.choice(list(all_topics_in_one_set))
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

def select_random_and_do_rag():
    message_payload = get_data_from_binary()
    generated_topics_by_page = message_payload[0]
    extracted_text_by_page = message_payload[1]

    randomly_selected_topic = pick_random_topic(generated_topics_by_page)
    print('generated_topics_by_page: ', generated_topics_by_page)

    most_relevant_page = retrieve_page_from_topic(generated_topics_by_page, randomly_selected_topic)
    print('got most relevant page: ', most_relevant_page)

    relevant_text_to_randomly_selected_topic = extracted_text_by_page[most_relevant_page]
    print('text of most relevant: ', extracted_text_by_page[most_relevant_page])

    return relevant_text_to_randomly_selected_topic