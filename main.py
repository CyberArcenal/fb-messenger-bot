from fbchat import Client, log, _graphql
from fbchat.models import *
from fbchat.models import ThreadType
from functions.logger import log, log_error
from settings.br import get_user_agent, get_header
from settings.version import __check__, __clr__
from browser.browser import browser
from settings.settings import blue, white, green, \
    red, yellow, line, line2, logo, DEBUG, \
    session, ACCOUNT
from functions.checker import check
from settings.version import __check__, __clr__
from settings.br import get_header
from functions.ck import save_cookies_in_the_list, display_cookies, \
    save_cookies, clean_cookie, clear_cookies, clear_logs, \
    open_cookie_list, open_cookies
from functions.logger import log, log_error

from functions.soup import find_input_fields, find_url, \
    get_input_data, create_form, create_form_2fa, \
    get_page_title, get_title_dexcription, get_title_message
from tools.tools import get_tag, get_patterns, get_response_patterns, get_required_words, save_json
import mybot
from icecream import ic
import threading
import json
import random
import requests
import time
import math
import os
import sys

#################### SETTINGS################################
__check__()
clr = __clr__()
header = get_header()
RUN = True
FACEBOOK_CLIENT: Client = None


def check_approval(data):
    url = "https://m.facebook.com/login/approvals/approved_machine_check/"
    page = browser(url=url, data=data)

    try:
        # Try to parse the JSON-like response body
        # Remove the prefix "for (;;);"
        json_data = page.text.replace("for (;;);", "")

        # Parse the JSON-like response body
        response_json = json.loads(json_data)
        # Access specific values from the response
        is_approved = True if 'True' in str(response_json) else False
        # Print the values
        if DEBUG:
            print(f"is_approved: {is_approved}")

        if is_approved:
            return True
        else:
            return False
    except json.decoder.JSONDecodeError as e:
        # Handle the case where the response is not valid JSON
        if DEBUG:
            print(f"JSON Decode Error: {e}")
        return False


def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)


class Facebook:
    def __init__(self, account: str, password: str) -> None:
        clean_cookie()
        self.account = account
        self.password = password

    def handle_checkpoint(self):
        # Code to handle checkpoint scenarios
        print('\n\033[1;93m Your Account is in Checkpoint:')
        clean_cookie()
        sys.exit()
        # Additional actions if needed

    def handle_unknown_response(self):
        print(f"{red}\t\tInvalid response, maybe the script is not updated.\n\t\tPlease report it to the developer.{white}")
        clean_cookie()
        sys.exit()

    def Continue(self):
        global RUN
        page: requests.Response = self.page
        while RUN:
            action_url = find_url(page.text)
            data = get_input_data(page)
            title = get_page_title(page_text=page.text)
            data = check(title=title, data=data, page=page)
            page: requests.Response = browser(
                url=action_url, data=data, redirect=False, print_title=True)
            if "c_user" in page.cookies.get_dict():
                print(
                    f"\033[1;92m║ {green}Facebook account login succesfully.")
                print(65 * '\033[1;92m=')
                RUN = False
                display_cookies(account_name=ACCOUNT)
                input()
                home()
            time.sleep(4)

    def bg_check_approval(self, data, action_url):
        global RUN
        data['approvals_code'] = ""
        while RUN:
            if check_approval(data=data):
                page: requests.Response = browser(
                    url=action_url, data=data, redirect=False)
                if "c_user" in page.cookies.get_dict():
                    print(f"{green}Facebook account approve login succesfully.")
                    print(65 * '\033[1;92m=')
                    RUN = False
                    display_cookies(account_name=ACCOUNT)
                    input()
                    home()
            time.sleep(7)
        return

    def two_factor_mode(self):
        global RUN
        action_url, data = create_form_2fa(self.page)
        print(f"\033[1;92m║ {green}Enter login code to continue{white}")
        print(
            f"\033[1;92m║ {green}You can approve login by other device.{white}")
        while RUN:
            code = input(f"\033[1;92m║ {blue}input 6 digit code: {white}")
            if len(str(code)) > 5:
                break
            else:
                print(
                    f"\033[1;92m║ {red}Please enter login code to continue.{white}")
        if RUN == False:
            input()
            home()
        data['approvals_code'] = code
        self.page: requests.Response = browser(url=action_url, data=data)
        title = get_page_title(page_text=self.page.text)
        list_error = ["too many login attempts", "too many", "attemps"]
        if any(word.lower() in title.lower() for word in list_error):
            print(f"\033[1;92m║ {red}{title}")
            input(f"{yellow}Exit:")
            home()
        self.Continue()

    def login(self):
        global RUN
        list_error = ["log into facebook", "log into"]
        list_error_password = ["reset your password", "reset"]
        #### LOAD LOGIN PAGE######
        URL = 'https://m.facebook.com'
        page = browser(URL)
        data, url = create_form(response=page)
        while True:
            ## put email/pass in data dictionary##
            data['email'] = self.account
            data['pass'] = self.password
            # requests login
            self.page: requests.Response = browser(url, data=data)
            # getting page title
            title = get_page_title(page_text=self.page.text)
            print("\033[1;92m║ "+yellow+title)
            if any(word.lower() in title.lower() for word in list_error):
                print(
                    f"\033[1;92m║ {red}Maybe your password is not match or typo, \n\033[1;92m║ please input your correct password.")
                print("\033[1;92m║ email/number/username/etc:")
                self.account = pick()
                print("\033[1;92m║ \033[1;92mYour Password:")
                self.password = pick()
            elif any(word.lower() in title.lower() for word in list_error_password):
                print(
                    f"\033[1;92m║ {red}Maybe your password is not match or typo, \n\033[1;92m║ {red}please input your correct password.")
                print("\033[1;92m║ email/number/username/etc:")
                self.account = pick()
                print("\033[1;92m║ \033[1;92mYour Password:")
                self.password = pick()
            else:
                break
        if "c_user" in self.page.cookies.get_dict():
            print(f"\033[1;92m║ {green}Facebook account login succesfully.")
            print(65 * '\033[1;92m=')
            RUN = False
            display_cookies(account_name=ACCOUNT)
            input()
            home()

        if "checkpoint" in self.page.url and "approvals_code" in self.page.text:
            print('\033[1;92m║ \033[1;93m2FA auth required:')
            action_url, data = create_form_2fa(self.page)
            # Corrected line
            thread = threading.Thread(
                target=self.bg_check_approval, args=(data, action_url))
            thread1 = threading.Thread(target=self.two_factor_mode)
            thread1.start()
            thread.start()
        elif title == "Review Recent Login" or 'submit[Continue]' in self.page.text:
            self.Continue()
        elif "checkpoint_title" in self.page.text:
            self.handle_checkpoint()

        else:
            log_error(
                f"A new title has come please add this {white}{title} in check function.")
            self.handle_unknown_response()


def display_cookiefile(cookies):
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║")
    ic(cookies)
    print("\033[1;92m║")
    print(line2)
    print(f"\n{cookies}")
    input(f"{yellow}Exit:")
    View_Cookies()


def View_Cookies():
    os.system(clr)
    print(logo)
    print(line)
    cookie_list = open_cookie_list()
    for i in range(len(cookie_list['cookies_list'])):
        to_display = cookie_list["cookies_list"][i]
        print(
            f"\033[1;92m║ {white}{str(i)}. \033[1;92mAccount: {to_display['account']}")
        print(
            f"\033[1;92m║ \033[1;92mDate Logged: {to_display['date_logged']}")
        print(line2)
    try:
        a = pick()
        if a == "":
            home()
        display_cookiefile(cookie_list["cookies_list"][int(a)]["cookies"])
    except Exception as e:
        log_error(e)
        input()
        View_Cookies()


def Generate_Cookies():
    global ACCOUNT, RUN
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ email/number/username/etc:")
    user = pick()
    print("\033[1;92m║ \033[1;92mYour Password:")
    userpass = pick()
    cookies = open_cookies()
    if "c_user" in cookies:
        clear_cookies()
    clear_logs()
    ACCOUNT = user
    login = Facebook(user, userpass)
    login.login()

def check_message(message_object, author_id, uid):
    if (author_id == uid):
        return None
    try:
        msg = str(message_object).split(",")[15][14:-1]
        print(msg)

        if "//video.xx.fbcdn" in msg:
            return msg
        else:
            return str(message_object).split(",")[19][20:-1]
    except Exception as e:
        try:
            msg = message_object.text.lower()
            print(msg)
            return msg
        except Exception as e:
            print(f"Error in check_message: {e}")
            return None


class Facebook_messenger(Client):
    def searchUser(self, msg: str, thread_id, thread_type):
        try:
            name = " ".join(msg.split()[2:4])
            try:
                limit = int(msg.split()[4])
            except:
                limit = 10
            params = {"search": name, "limit": limit}
            (j,) = self.graphql_requests(
                _graphql.from_query(_graphql.SEARCH_USER, params))
            users = ([User._from_graphql(node)
                      for node in j[name]["users"]["nodes"]])
            for user in users:
                reply = f"{user.name} profile_link: {user.url}\n friend: {user.is_friend}\n"
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        except Exception as e:
            log_error(e)

    def message_proccessing_unit(self, msg: str, thread_id, thread_type):
        try:
            if "search" in msg and "user" in msg or "search" in msg and "friend" in msg:
                self.searchUser(msg=msg, thread_id=thread_id,
                                thread_type=thread_type)
            else:
                # Simulate typing
                self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
                reply = mybot.get_response(msg)
                # Stop simulating typing
                if len(str(reply)) < 15:
                    time.sleep(2)
                elif len(str(reply)) > 20 and len(str(reply)) < 30:
                    time.sleep(3)
                else:
                    time.sleep(4)
                self.setTypingStatus(TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)
                if str(reply)=="" or reply == None:
                    return
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        except Exception as e:
            log_error(e)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        try:
            msg = check_message(
                message_object, author_id=author_id, uid=self.uid)
            if msg:
                # Perform actions based on the message content
                self.message_proccessing_unit(
                    msg=msg, thread_id=thread_id, thread_type=thread_type)
        except Exception as e:
            print(f"Error in onMessage: {e}")
        self.markAsDelivered(author_id, thread_id)


def display_account_info(client: Client):
    # Get user details
    user_details = client.fetchUserInfo(client.uid)
    user = user_details[client.uid]

    # Print user information
    print("\r\r\r\033[1;92m║User ID:", user.uid)
    print("\033[1;92m║Name:", user.name)
    print("\033[1;92m║First Name:", user.first_name)
    print("\033[1;92m║Last Name:", user.last_name)


def start_bot():
    global FACEBOOK_CLIENT
    sys.stdout.write("\033[1000D\033[1;92m║ Loggining account...")
    sys.stdout.flush()
    cookies = json.loads(open("cookies/cookies.json", "r").read())
    FACEBOOK_CLIENT = Facebook_messenger("", "", session_cookies=cookies)
    display_account_info(client=FACEBOOK_CLIENT)
    try:
        if FACEBOOK_CLIENT.isLoggedIn():
            while True:
                try:
                    FACEBOOK_CLIENT.listen()
                except KeyboardInterrupt:
                    log("User interrup exiting...")
                    time.sleep(3)
                    sys.exit()
                except Exception as e:
                    print(f"\033[1;92m║ Error in listening: {e}")
                    time.sleep(6)
    except AttributeError:
        input("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
        home()


def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)

def test_bot():
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ \033[1;96m=== Chatbot Configuration Tool ===\033[0m")
    while True:
        user_input = input("\033[1;92m║ You: ")
        print(user_input)
        if user_input.lower() == 'exit':
            print("Exiting the chat.")
            break
        
        bot_response = mybot.get_response(user_input)
        print(f"\033[1;92m║ Bot: {bot_response}")
    home()


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

            if single_response.lower() == "y":
                single_response = True
            else:
                single_response = False

            save_json(tags, patterns, response,
                      single_response, required_words)
        except KeyboardInterrupt:
            home()
def home():
    os.system(clr)
    print(logo)
    print(line)
    try:
        cookies = json.loads(open("cookies/cookies.json", "r").read())
        if cookies['c_user'] != "" or cookies['c_user'] != None:
            pass
        else:
            print("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
            print(line)
    except Exception as e:
        # log_error(e.args)
        # print("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
        print("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
        print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mStart Chat-Bot")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mAdd Cookies")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mView Cookies")
    print("\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mTrain ChatBot")
    print("\033[1;92m║ \033[1;91m5. \033[1;94m—> \033[1;92mTest ChatBot")
    print("\033[1;92m║ \033[1;91m6. \033[1;94m—> \033[1;92mLogin")
    print("\033[1;92m║ \033[1;91m7. \033[1;94m—> \033[1;92mUpdate")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    home_pick()


def home_pick():
    p = pick()
    if p == "1":
        start_bot()
    elif p == "4":
        train_main()
    elif p == "5":
        test_bot()
    elif p == "6":
        Generate_Cookies()
    elif p == "7":
        os.system("git pull")
        os.system("python3 main.py")
    elif p == "0":
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        home_pick()


if __name__ == "__main__":
    home()
