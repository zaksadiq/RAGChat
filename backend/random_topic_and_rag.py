from parse_pdf import LOCAL_DATA_STORE_FOLDER

import random
import os
import pickle

def pick_random_topic(generated_pages_topics):
    # Create a set (because this will only allow unique additions, unlike an Array/List.)
    all_topics_in_one_set = set()
    for page in generated_pages_topics:
        for topic in page:
            all_topics_in_one_set.add(topic[0]) # Array index 0 contains the topic ID.

    selected_random_topic = random.choice(list(all_topics_in_one_set))
    print('Random topic:')
    print(selected_random_topic)
    
    return selected_random_topic

def get_topics_from_binary():
    binary_folder_path = LOCAL_DATA_STORE_FOLDER + '/'
    binary_files = [os.path.join(binary_folder_path, f) for f in os.listdir(binary_folder_path)]
    # Get latest file.
    latest = max(binary_files, key=os.path.getctime)
    print('latest file:')
    print(latest)

    with open(latest, "rb") as file:
        generated_topics_by_page = pickle.load(file)

    return generated_topics_by_page

def select_random_and_do_rag():
    generated_topics_by_page = get_topics_from_binary()
    randomly_selected_topic = pick_random_topic(generated_topics_by_page)
    print(generated_topics_by_page)