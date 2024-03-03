from fbchat import Client, log, _graphql
from fbchat.models import *
from fbchat.models import ThreadType
from functions.logger import log, log_error
from settings.br import get_user_agent, get_header
from settings.version import __check__, __clr__
from browser.browser import browser
from settings.settings import blue, white, green, \
    red, yellow, line, line2, logo, DEBUG, \
    session
from functions.checker import check
from settings.version import __check__, __clr__
from settings.br import get_header
from functions.ck import save_cookies_in_the_list, load_cookies, \
    save_cookies, clean_cookie, clear_cookies, clear_logs, \
    open_cookie_list, open_cookies, switch_cookiefile
from functions.logger import log, log_error
from functions.settings import settings
from functions.soup import find_input_fields, find_url, \
    get_input_data, create_form, create_form_2fa, \
    get_page_title, get_title_dexcription, get_title_message, \
    get_youtube_link, save_ongoing_chat, translator, weather
from tools.tools import get_tag, get_patterns, get_response_patterns, \
    get_required_words, save_json
from functions.bot_manager import bot_manager
from functions.search_user import get_limit
import mybot
from icecream import ic
import concurrent.futures
import wolframalpha
import sqlite3
import threading
import json
import random
import requests
import time
import math
import os
import sys

__check__()
clr = __clr__()
header = get_header()
RUN = True
FACEBOOK_CLIENT: Client = None
ACCOUNT = ""
# Create a threading lock
console_lock = threading.Lock()


def pick():
    with console_lock:
        user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)


def check_approval(data):
    if RUN:
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
    else:
        return False


def return_home():
    from main import home
    home()


def is_login_checker():
    global RUN
    while True:
        if RUN == False:
            input("\033[1;92m║ \033[1;93mExit.")
            return_home()
        else:
            time.sleep(1)


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
        global RUN, ACCOUNT
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
                    f"\r\r\r\r\033[1;92m║ {green}Facebook account login succesfully.")
                print(65 * '\033[1;92m=')
                RUN = False
                load_cookies(account_name=ACCOUNT)
            time.sleep(4)

    def bg_check_approval(self, data, action_url):
        global RUN, ACCOUNT
        data['approvals_code'] = ""
        while RUN:
            if check_approval(data=data):
                page: requests.Response = browser(
                    url=action_url, data=data, redirect=False)
                if "c_user" in page.cookies.get_dict():
                    print(
                        f"\r\r\r\r{green}Facebook account approve login succesfully.")
                    print(65 * '\033[1;92m=')
                    RUN = False
                    load_cookies(account_name=ACCOUNT)
            time.sleep(7)
        return

    def two_factor_mode(self):
        global RUN
        action_url, data = create_form_2fa(self.page)
        with console_lock:
            print(f"\033[1;92m║ {green}Enter login code to continue{white}")
            print(
                f"\033[1;92m║ {green}You can approve login by other device.{white}")
        while RUN:
            with console_lock:
                print(f"\033[1;92m║ {blue}input 6 digit code: {white}")
            code = pick()
            if len(str(code)) > 5:
                break
            elif RUN == False:
                return
            else:
                with console_lock:
                    print(
                        f"\033[1;92m║ {red}Please enter login code to continue.{white}")
        if RUN == False:
            return
        data['approvals_code'] = code
        self.page: requests.Response = browser(url=action_url, data=data)
        title = get_page_title(page_text=self.page.text)
        list_error = ["too many login attempts", "too many", "attemps"]
        if any(word.lower() in title.lower() for word in list_error):
            print(f"\033[1;92m║ {red}{title}")
            input(f"{yellow}Exit:")
            return_home()
        self.Continue()

    def login(self):
        global RUN, ACCOUNT
        RUN = True
        list_error = ["log into facebook", "log into"]
        list_error_password = ["reset your password", "reset"]
        #### LOAD LOGIN PAGE######
        ACCOUNT = self.account
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
            print(f"\r\r\r\r\033[1;92m║ {green}Facebook account login succesfully.")
            print(65 * '\033[1;92m=')
            RUN = False
            load_cookies(account_name=ACCOUNT)
            input()
            return_home()

        if "checkpoint" in self.page.url and "approvals_code" in self.page.text:
            print('\033[1;92m║ \033[1;93m2FA auth required:')
            action_url, data = create_form_2fa(self.page)
            # Corrected line
            thread = threading.Thread(
                target=self.bg_check_approval, args=(data, action_url))
            thread1 = threading.Thread(target=self.two_factor_mode)
            thread2 = threading.Thread(target=is_login_checker)
            thread.start()
            time.sleep(1)
            thread1.start()
            time.sleep(1)
            thread2.start()

        elif title == "Review Recent Login" or 'submit[Continue]' in self.page.text:
            self.Continue()
        elif "checkpoint_title" in self.page.text:
            self.handle_checkpoint()

        else:
            log_error(
                f"A new title has come please add this {white}{title} in check function.")
            self.handle_unknown_response()
