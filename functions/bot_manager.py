import os
from settings.version import __check__, __clr__
from settings.settings import blue, white, green, \
    red, yellow, line, line2, logo, DEBUG, \
    session, ACCOUNT
from functions.ck import save_cookies_in_the_list, display_cookies, \
    save_cookies, clean_cookie, clear_cookies, clear_logs, \
    open_cookie_list, open_cookies, switch_cookiefile
from tools.tools import get_tag, get_patterns, get_response_patterns, \
    get_required_words, save_json
from functions.logger import log, log_error
from icecream import ic
import json
import time
import sys
import mybot


def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)


def test_bot():
    os.system(__clr__())
    print(logo)
    print(line)
    print("\033[1;92m║ \033[1;96m=== Chatbot Configuration Tool ===\033[0m")
    while True:
        user_input = input("\033[1;92m║ You: ")
        if user_input.lower() == 'exit':
            print("Exiting the chat.")
            time.sleep(2)
            break

        bot_response = mybot.get_response(user_input)
        print(f"\033[1;92m║ Bot: {bot_response}")
    from main import home
    home()


def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)


def train_main():
    """
    Main function for the Chatbot Configuration Tool.

    This tool allows developers to configure the chatbot's responses.
    It prompts the user for details such as tags, patterns, responses, and required words.
    The configuration is then saved to a JSON file.

    LICENSE:
    This code is licensed under the MIT License.
    See the LICENSE file in the root of this repository for details.

    REMINDER:
    Use this tool responsibly and consider the impact on user experience.

    AUTHOR:
    GitHub: CyberArcenal
    Github: black
    """

    print("\033[1;92m║ \033[1;96m=== Chatbot Configuration Tool ===\033[0m")
    while True:
        try:
            tags = get_tag()
            patterns = get_patterns()
            response = get_response_patterns()
            single_response = input(
                "\033[1;97msingle response? [Y/n]: \033[1;92m").lower()
            required_words = get_required_words()

            if single_response.lower() == "n":
                single_response = False
            else:
                single_response = True

            save_json(tags, patterns, response,
                      single_response, required_words)
        except KeyboardInterrupt:
            from main import home
            home()


def train_with_facebook_data():
    """
    Main function for the Chatbot Configuration Tool.

    This tool allows developers to configure the chatbot's responses.
    It prompts the user for details such as tags, patterns, responses, and required words.
    The configuration is then saved to a JSON file.

    LICENSE:
    This code is licensed under the MIT License.
    See the LICENSE file in the root of this repository for details.

    REMINDER:
    Use this tool responsibly and consider the impact on user experience.

    AUTHOR:
    GitHub: CyberArcenal
    Github: black
    """

    print("\033[1;92m║ \033[1;96m=== Chatbot Configuration Tool ===\033[0m")
    tags = get_tag()
    try:
        print("\033[1;92m║ \033[1;93mMake sure file is in json format.")
        __input__ = input(
            "\033[1;92m║ \033[1;97mFacebook chat file: \033[1;92m")
        print("\033[1;92m║ \033[1;97mParticipants is.")
        file = json.loads(open(__input__, "r").read())
        for user in file["participants"]:
            print(f"\033[1;92m║ \033[1;97m{user}")
        print(
            "\033[1;92m║ \t\033[1;93mPlease Review the chat\n\033[1;92m║\t if the message is chat pattern or your response")
        print(
            "\033[1;92m║ \t\033[1;97mSkip if \033[1;93mYes \033[1;97mor Type \033[1;93m\"n\" \033[1;97mif \033[1;91mNo")
        chat_list = file['messages']
        chat_list.reverse()
        last_message = 0
        for num, chat in enumerate(chat_list):
            if last_message == num:
                continue
            display_chat(chat=chat)
            isChat = input(
                "\033[1;92m║ \033[1;93mThis is chat pattern?[skip/n]: \033[1;92m")
            if isChat == "":
                pattern = chat['content'].strip().split()
            else:
                continue
            add = 1
            while True:
                display_chat(file["messages"][num+add])
                isChatResponse = input(
                    "\033[1;92m║ \033[1;94mThis is chat response?[skip/n/i]: \033[1;92m")
                if isChatResponse == "":
                    response = file["messages"][num+add]['content']
                    response_storage = []
                    response_storage.append(response)
                    save_json(tags=tags, patterns=pattern, response=response_storage,
                              single_response=True, required_words=[])
                    print("\033[1;91m=========================================")
                    last_message = num+add
                    break
                elif isChatResponse == "i":
                    response = input(
                        "\033[1;92m║ \033[1;92mInput your custom response: ")
                    response_storage = []
                    response_storage.append(response)
                    save_json(tags=tags, patterns=pattern, response=response_storage,
                              single_response=True, required_words=[])
                    print("\033[1;91m=========================================")
                    last_message = num+add
                    break
                else:
                    add += 1
            continue

    except Exception as e:
        ic(e)


def display_chat(chat: dict):
    for key, value in chat.items():
        print(f"\033[1;92m║ \033[1;96m{key}: {value}")


def bot_manager():
    os.system(__clr__())
    print(logo)
    print(line)
    print(
        "\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mTrain ChatBot with FBData")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mTrain ChatBot")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mTest ChatBot")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mBack")
    bot_manager_pick()


def bot_manager_pick():
    while True:
        p = pick()
        if p == "1":
            train_with_facebook_data()
            break
        elif p == "2":
            train_main()
            break
        elif p == "3":
            test_bot()
            break
        elif p == "0":
            from main import home
            home()
        else:
            print("\033[1;92m║ \033[1;91minvalid input")
