import json
from icecream import ic
from typing import List

TAGS_MAPPING = json.loads(open("data/tags_mapping.json", "r").read())

def get_required_words():
    storage = []
    while True:
        try:
            __input__ = input("\033[1;97mrequired words: \033[1;92m")
            if __input__ == "":
                return storage
            if __input__ != "":
                storage.append(__input__)
            print(f"Required words patterns: {storage} \033[1;93mskip to exit\033[1;92m")
        except Exception as e:
            ic(e)
            
def get_response():
    storage = []
    while True:
        try:
            __input__ = input("\033[1;97mResponse: \033[1;92m")
            if __input__ == "" and len(storage) != 0:
                return storage
            if __input__ == "" and len(storage) == 0:
                print("\033[1;93mPlease add words before skip!\033[1;92m")
            if __input__ != "":
                storage.append(__input__)
            print(f"Sender patterns: {storage} \033[1;93mskip to exit\033[1;92m")
        except Exception as e:
            ic(e)

def get_patterns():
    storage = []
    while True:
        try:
            __input__ = input("\033[1;97mChat patterns: \033[1;92m")
            if __input__ == "" and len(storage) != 0:
                return storage
            if __input__ == "" and len(storage) == 0:
                print("\033[1;93mPlease add words before skip!\033[1;92m")
            if __input__ != "":
                storage.append(__input__)
            print(f"Sender patterns: {storage} \033[1;93mskip to exit\033[1;92m")
        except Exception as e:
            ic(e)
            
def get_tag():
    print("Tags:")
    for key, value in TAGS_MAPPING.items():
        print(f"\033[1;92m{key}. {value}")
    
    tags = input("\033[1;97mEnter the tag number: \033[1;92m")
    return TAGS_MAPPING.get(tags, "General Inquiries")

def is_new(patterns, tags):
    config = openconfig()
    for i in config.get(tags, []):
        try:
            print("Current element:", i)
            if isinstance(i, dict) and 'patterns' in i and any(pattern in i['patterns'] for pattern in patterns):
                return False
        except Exception as e:
            print("Error:", e)
            input()
    return True
    
def save_json(tags, patterns, response, single_response, required_words):
    new = is_new(patterns=patterns, tags=tags)
    if new:
        save_new(tags, patterns, response, single_response, required_words)
    else:
        save_already(tags, patterns, response, single_response, required_words)

def save_already(tags: str, patterns: List[str], response: List[str], single_response: bool, required_words: List[str]):
    check_tags(tags=tags)
    config = openconfig()
    configuration = config.get(tags, [])

    if not isinstance(configuration, list):
        raise ValueError(f"Invalid configuration format for tag '{tags}'.")

    for entry in configuration:
        if 'patterns' in entry and any(pattern in entry['patterns'] for pattern in patterns):
            # Convert response to set to remove duplicates
            existing_response_set = set(entry['response'])
            new_response_set = set(response)

            # Extend the set with the new response strings
            existing_response_set.update(new_response_set)

            # Convert the set back to a list
            entry['response'] = list(existing_response_set)

            entry['single_response'] = single_response
            entry['required_words'].extend(required_words)

    config_w(config)
    ic("Existing configuration updated.")


def check_tags(tags):
    config = openconfig()
    if tags not in config:
        config[tags] = []
        config_w(config)
    return

def save_new(tags, patterns, response, single_response, required_words=[]):
    check_tags(tags=tags)
    config = openconfig()
    data = {
        "patterns": patterns,
        "response": response,
        "single_response": single_response,
        "required_words": required_words
    }
    config[tags].append(data)
    config_w(config)
    ic("New configuration saved.")

def openconfig():
    try:
        with open('data/config.json', 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {}

def config_w(config):
    with open('data/config.json', 'w') as file:
        json.dump(config, file)