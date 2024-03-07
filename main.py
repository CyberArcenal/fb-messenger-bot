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



def display_account_info():
    global FACEBOOK_CLIENT
    # Get user details
    user = get_current_account_info()
    # Print user information
    print("\r\r\r\033[1;92m║ User ID:", user['uid'])
    print("\033[1;92m║ Name:", user['name'])
    print("\033[1;92m║ Chats:", user['message_count'])


def start_bot():
    global FACEBOOK_CLIENT
    os.system(clr)
    try:
        log("Checking account..")
        FACEBOOK_CLIENT.isLoggedIn()
    except:
        log("Loggining account...")
        cookies = open_cookies()
        try:
            FACEBOOK_CLIENT = Facebook_messenger(
                "", "", session_cookies=cookies)

        except Exception as e:
            log_error(e)
            input("\033[1;92m║ \033[1;93mExit.")
            home()
    try:
        display_account_info()
        update_and_save_cookies()
        while True:
            try:
                FACEBOOK_CLIENT.listen()
            except KeyboardInterrupt:
                log("User interrup exiting...")
                update_and_save_cookies()
                time.sleep(3)
                home()
            except Exception as e:
                log_error(f"\033[1;92m║ Error in listening: {e}")
                time.sleep(6)
                log(f"\033[1;92m║ Reconnecting: {e}")
    except AttributeError:
        input("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
        home()


def update_and_save_cookies():
    global FACEBOOK_CLIENT
    log("Saving session.")
    # I-save ang current cookies
    current_cookies = FACEBOOK_CLIENT.getSession()
    save_session_cookies(session_cookies=current_cookies)
    # Itigil ang client.listen()
    FACEBOOK_CLIENT.stopListening()

def get_current_account_info():
    global FACEBOOK_CLIENT
    client = FACEBOOK_CLIENT
    # Check if user_info.json exists
    try:
        with open("data/user_info.json", "r") as f:
            user_info = json.load(f)
    except FileNotFoundError:
        user_info = None

    if not user_info:
        # Retrieve user details from Facebook
        try:
            user_details = client.fetchUserInfo(client.uid)
            user_info = user_details[client.uid].__dict__
            user_info['type'] = None
            with open("data/user_info.json", "w") as f:
                json.dump(user_info, f, indent=4)
        except Exception as e:
            #print(f"Error retrieving user details: {e}")
            return None

    return user_info
        

def get_current_user_account_name():
    global FACEBOOK_CLIENT
    # Get user details
    user_details = FACEBOOK_CLIENT.fetchUserInfo(FACEBOOK_CLIENT.uid)
    user = user_details[FACEBOOK_CLIENT.uid]
    return user.name


def save_session_cookies(session_cookies: dict = None):
    c = open_cookies()
    if session_cookies:
        save_cookies(cookies=c, session_cookies=session_cookies)
        save_cookies_in_the_list(
            session_cookies, account_name=get_current_user_account_name())
    else:
        log_error("No session cookies")


def save_user_data(data: dict):
    try:
        with open("data/user_data.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

def load_user_data():
    global FACEBOOK_CLIENT
    log("Loading...")
    try:
        user_data = get_current_account_info()
        if user_data['name']:
            return True
    except:
        cookies = open_cookies()
        if cookies['c_user'] != "" or cookies['c_user'] != None and FACEBOOK_CLIENT == None:
            FACEBOOK_CLIENT = Facebook_messenger(
                        "", "", session_cookies=cookies)
            update_and_save_cookies()
            return True
        else:
            return False

def home():
    global FACEBOOK_CLIENT
    try:
        if load_user_data():
            os.system(clr)
            print(logo)
            print(line)
            display_account_info()
            print(line)
        else:
            os.system(clr)
            print(logo)
            print(line)
            print("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
            print(line)
    except Exception as e:
        log(e)
        os.system(clr)
        print(logo)
        print(line)
        print("\r\r\r\033[1;92m║ \033[1;91mNo Account Logged.")
        print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mStart Chat-Bot")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mChatBot Manager")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mSettings")
    print("\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mLogin")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    home_pick()


def home_pick():
    global FACEBOOK_CLIENT
    p = pick()
    if p == "1":
        start_bot()
    elif p == "2":
        bot_manager()
    elif p == "3":
        settings(client=FACEBOOK_CLIENT)
    elif p == "4":
        login()
    elif p == "0":
        FACEBOOK_CLIENT.stopListening()
        update_and_save_cookies()
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        home_pick()


if __name__ == "__main__":
    home()
