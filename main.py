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
from facebook import Facebook
from messenger import Facebook_messenger
from icecream import ic
import json
import time
import os
import sys

#################### SETTINGS ################################
__check__()
clr = __clr__()
header = get_header()
RUN = True
FACEBOOK_CLIENT: Client = None


def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)

def login_with_cookies():
    dict_list = ["sb", "fr", "c_user", "datr", "xs"]
    os.system(clr)
    print(logo)
    print(line)
    data = dict()
    for word in dict_list:
        print(f"\033[1;92m║ Input \033[1;97m{word.upper()}:")
        cookie_value = get_cookie_input(word)
        data[word] = cookie_value
    try:
        with open("cookies/cookies.json", "w") as f:
            json.dump(data, f)
            f.close()
            save_cookies_in_the_list(cookies=data, account_name=data["c_user"])
            log("Add cookies success.")
            input()
            home()
    except Exception as e:
        log_error(e)
        input()
        home()

def get_cookie_input(cookie_name: str):
    while True:
        a = pick()
        if a == "" or len(a) < 5 or a == None:
            log_error(f"Please input correct {cookie_name.upper()} value")
            continue
        elif a == "exit":
            home()
        else:
            return a        

def login():
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mFacebook login")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mInput cookies")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mBack")
    login_pick()


def login_pick():
    p = pick()
    if p == "1":
        Generate_Cookies()
    elif p == "2":
        login_with_cookies()
    elif p == "0":
        home()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        home_pick()


def Generate_Cookies():
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ email/number/username/etc:")
    user = pick()
    print("\033[1;92m║ \033[1;92mYour Password:")
    userpass = pick()
    cookies = open_cookies()
    if "c_user" in cookies or "checkpoint" in cookies:
        clear_cookies()
    clear_logs()
    login = Facebook(user, userpass)
    login.login()


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
    cookies = open_cookies() # json.loads(open("cookies/cookies.json", "r").read())
    try:
        FACEBOOK_CLIENT = Facebook_messenger("", "", session_cookies=cookies)
    except FBchatUserError:
        log_error(f"\033[1;92m║ Account login error please login again.")
        input("Return: Enter")
        home()
    display_account_info(client=FACEBOOK_CLIENT)
    try:
        if FACEBOOK_CLIENT.isLoggedIn():
            while True:
                try:
                    FACEBOOK_CLIENT.listen()
                except KeyboardInterrupt:
                    log("User interrup exiting...")
                    time.sleep(3)
                    home()
                except Exception as e:
                    log_error(f"\033[1;92m║ Error in listening: {e}")
                    time.sleep(6)
                    log(f"\033[1;92m║ Reconnecting: {e}")
    except AttributeError:
        input("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
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
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mChatBot Manager")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mSettings")
    print("\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mLogin")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    home_pick()


def home_pick():
    p = pick()
    if p == "1":
        start_bot()
    elif p == "2":
        bot_manager()
    elif p == "3":
        settings()
    elif p == "4":
        login()
    elif p == "0":
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        home_pick()


if __name__ == "__main__":
    home()
