import re
import random
import json


def probability_test(message, word_patterns, single_response=False, required_words=[]):
    has_required_words = True
    message_certainty = sum(1 for word in message if str(
        word).lower() in word_patterns)
    percentage = message_certainty / len(word_patterns)
    for word in required_words:
        if word not in message:
            has_required_words = False
    return int(percentage * 100) if has_required_words or single_response else 0


def get_all_data():
    data = []
    config_data = json.loads(open('data/config.json', 'r').read())
    for key, value in config_data.items():
        data.extend(value)
    return data


def check_all_messages(message):
    msg_data = get_all_data()
    unknown_response = json.loads(open('data/unknown.json', 'r').read())
    wordlist = {}

    def response(response, list_of_words, single_response=False, required_words=[]):
        nonlocal wordlist
        wordlist[response] = probability_test(
            message, list_of_words, single_response, required_words)

    for reply in msg_data:
        required_words = reply.get('required_words', [])
        random_reply = random.choice(reply['response'])
        response(random_reply, [str(word).lower() for word in reply['patterns']], bool(
            reply['single_response']), required_words)
    max_score = max(wordlist.values())
    if max_score == 0:
        # Activate typo check when all scores are zero
        return check_typo(message, msg_data, unknown_response)
    else:
        match = max(wordlist, key=wordlist.get)
        print(f'\033[1;92m║ Best match = {match} | Score: {wordlist[match]}')

        return random.choice(unknown_response) if wordlist[match] < 1 else match


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def check_typo(message, msg_data, unknown_response):
    min_distance = float('inf')
    best_match = None

    for reply in msg_data:
        for pattern in reply['patterns']:
            for word in message:
                if word[:3] == pattern[:3]:
                    dist = levenshtein_distance(message, pattern)
                    if dist < min_distance:
                        min_distance = dist
                        best_match = reply
                elif word[:2] == pattern[:2]:
                    dist = levenshtein_distance(message, pattern)
                    if dist < min_distance:
                        min_distance = dist
                        best_match = reply

    # You can adjust the threshold as needed
    typo_threshold = 3
    if min_distance <= typo_threshold:
        # If the minimum distance is below the threshold, consider it a match
        return random.choice(best_match['response'])
    else:
        # No close match found, return a response for a possible typo
        return random.choice(unknown_response)


def get_response(user_input: str) -> str:
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response
