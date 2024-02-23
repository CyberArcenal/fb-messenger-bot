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
    get_page_title, get_title_dexcription, get_title_message, \
    get_youtube_link, save_ongoing_chat, translator, weather
from tools.tools import get_tag, get_patterns, get_response_patterns, \
    get_required_words, save_json
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

        if "//video.xx.fbcdn" in msg:
            return msg
        else:
            return str(message_object).split(",")[19][20:-1]
    except Exception as e:
        try:
            msg = message_object.text.lower()
            return msg
        except Exception as e:
            print(f"Error in check_message: {e}")
            return None


class Facebook_messenger(Client):
    def TypingStatusStart(self, thread_id="", thread_type="", sleep: int = 2):
        self.setTypingStatus(TypingStatus.TYPING,
                             thread_id=thread_id, thread_type=thread_type)
        time.sleep(sleep)
        return

    def TypingStatusStop(self, thread_id="", thread_type=""):
        self.setTypingStatus(TypingStatus.STOPPED,
                             thread_id=thread_id, thread_type=thread_type)
        return

    def download_on_youtube(self, message, thread_type, thread_id):
        final_link = get_youtube_link(message=message)
        if final_link != None:
            self.TypingStatusStart(thread_id=thread_id,
                                   thread_type=thread_type, sleep=2)
            self.TypingStatusStop(thread_id=thread_id, thread_type=thread_type)
            self.sendRemoteFiles(
                file_urls=final_link, message=None, thread_id=thread_id, thread_type=thread_type)
        else:
            self.TypingStatusStart(thread_id=thread_id,
                                   thread_type=thread_type, sleep=2)
            reply = "Sorry something went wrong when i browsing your link:("
            self.TypingStatusStop(thread_id=thread_id, thread_type=thread_type)
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)

    def searchUser(self, msg: str, thread_id, thread_type):
        
        try:
            name = " ".join(msg.split()[2:4])
            limit = get_limit(message=msg)
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
    ###################### MESSAGE PROCESS CENTER#############################

    def message_proccessing_unit(self, msg: str, thread_id, thread_type):
        try:
            if "search" in msg and "user" in msg or "search" in msg and "friend" in msg:
                self.searchUser(msg=msg, thread_id=thread_id,
                                thread_type=thread_type)
            elif ("download youtube" in msg.lower()):
                self.download_on_youtube(
                    message=msg, thread_id=thread_id, thread_type=thread_type)
            elif ("search pdf" in msg.lower()):
                self.searchFiles(
                    self, msg=msg, thread_id=thread_id, thread_type=thread_type)
            elif ("search image" in msg):
                self.imageSearch(self, msg.lower())

            elif ("program to" in msg.lower()):
                self.programming_solution(self, msg)
            elif ("translate" in msg.lower()):
                reply = translator(self, msg, msg.split()[-1])
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
            elif "weather of" in msg.lower():
                indx = msg.index("weather of")
                query = msg[indx+11:]
                reply = weather(query)
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
            elif ("calculus" in msg.lower()):
                self.stepWiseCalculus(
                    " ".join(msg.split(" ")[1:]), thread_id=thread_id, thread_type=thread_type)
            elif ("algebra" in msg.lower()):
                self.stepWiseAlgebra(
                    " ".join(msg.split(" ")[1:]), thread_id=thread_id, thread_type=thread_type)
            elif ("query" in msg.lower()):
                self.stepWiseQueries(
                    " ".join(msg.split(" ")[1:]), thread_id=thread_id, thread_type=thread_type)

            elif "find" in msg.lower() or "solve" in msg.lower() or "evaluate" in msg.lower() or "calculate" in msg.lower() or "value" in msg.lower() or "convert" in msg.lower() or "simplify" in msg.lower() or "generate" in msg.lower():
                app_id = "Y98QH3-24PWX83VGA"
                client = wolframalpha.Client(app_id)
                query = msg.split()[1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                reply = f'Answer: {answer.replace("sqrt", "√")}'
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
            elif ("mute conversation" in msg.lower()):
                try:
                    self.muteThread(mute_time=-1, thread_id=thread_id)
                    reply = "muted 🔕"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
                except:
                    pass
            else:
                # Simulate typing
                self.setTypingStatus(
                    TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
                reply = mybot.get_response(msg)
                # Stop simulating typing
                if len(str(reply)) < 15:
                    time.sleep(2)
                elif len(str(reply)) > 20 and len(str(reply)) < 30:
                    time.sleep(3)
                else:
                    time.sleep(4)
                self.setTypingStatus(
                    TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)
                if str(reply) == "" or reply == None:
                    return
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        except Exception as e:
            log_error(e)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        try:
            if author_id == self.uid:
                return
            save_ongoing_chat(author_id=author_id, mid=mid, msg=msg)
            msg = check_message(
                message_object, author_id=author_id, uid=self.uid)
            if msg:
                # Perform actions based on the message content
                save_ongoing_chat(author_id=author_id, mid=mid, msg=msg)
                self.message_proccessing_unit(
                    msg=msg, thread_id=thread_id, thread_type=thread_type)
        except Exception as e:
            print(f"Error in onMessage: {e}")
        self.markAsDelivered(author_id, thread_id)

    def searchFiles(self, msg, thread_id, thread_type):
        query = " ".join(msg.split()[2:])
        file_urls = []
        url = "https://filepursuit.p.rapidapi.com/"

        querystring = {"q": query, "filetype": msg.split()[1]}

        headers = {
            'x-rapidapi-host': "filepursuit.p.rapidapi.com",
            'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        response = json.loads(response.text)
        file_contents = response["files_found"]
        try:
            for file in random.sample(file_contents, 10):
                file_url = file["file_link"]
                file_name = file["file_name"]
                self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                          thread_id=thread_id, thread_type=ThreadType.USER)
        except:
            for file in file_contents:
                file_url = file["file_link"]
                file_name = file["file_name"]
                self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                          thread_id=thread_id, thread_type=ThreadType.USER)

    def imageSearch(self, msg, thread_id, thread_type):
        try:
            count = int(msg.split()[-1])
        except:
            count = 10
        query = " ".join(msg.split()[2:])
        try:
            x = int(query.split()[-1])
            if type(x) == int:
                query = " ".join(msg.split()[2:-1])
        except:
            pass
        image_urls = []

        url = "https://bing-image-search1.p.rapidapi.com/images/search"

        querystring = {"q": query, "count": str(count)}

        headers = {
            'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
            'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
        }
        print("sending requests...")
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        print("got response..")
        data = json.loads(response.text)
        img_contents = (data["value"])
        # print(img_contents)
        for img_url in img_contents:
            image_urls.append(img_url["contentUrl"])
            print("appended..")

        def multiThreadImg(img_url):
            if (thread_type == ThreadType.USER):
                self.sendRemoteFiles(
                    file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
            elif (thread_type == ThreadType.GROUP):
                self.sendRemoteFiles(
                    file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(multiThreadImg, image_urls)

    def programming_solution(self, query, msg, thread_id, thread_type):
        try:
            count = int(msg.split()[-1])
        except:
            count = 6
        try:
            x = int(query.split()[-1])
            if type(x) == int:
                query = " ".join(msg.split()[0:-1])
        except:
            pass
        image_urls = []

        url = "https://bing-image-search1.p.rapidapi.com/images/search"

        querystring = {"q": query, "count": str(count)}

        headers = {
            'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
            'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        img_contents = (data["value"])
        # print(img_contents)
        for img_url in img_contents:
            image_urls.append(img_url["contentUrl"])
            print("appended..")

        def multiThreadImg(img_url):
            if (thread_type == ThreadType.USER):
                self.sendRemoteFiles(
                    file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
            elif (thread_type == ThreadType.GROUP):
                self.sendRemoteFiles(
                    file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(multiThreadImg, image_urls)

    def stepWiseQueries(self, query, thread_id, thread_type):
        query = query.replace("+", "%2B")
        api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
        json_data = requests.get(api_address).json()
        try:
            try:
                answer = json_data["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
                answer = answer.replace("sqrt", "√")
                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
        except:
            self.send(Message(text="Cannot find the solution of this problem"), thread_id=thread_id,
                      thread_type=thread_type)

    def stepWiseAlgebra(self, query, thread_id, thread_type):
        query = query.replace("+", "%2B")
        api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input=solve%203x^2+4x-6=0&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
        json_data = requests.get(api_address).json()
        try:
            answer = json_data["queryresult"]["pods"][1]["subpods"][2]["plaintext"]
            answer = answer.replace("sqrt", "√")

            self.send(Message(text=answer), thread_id=thread_id,
                      thread_type=thread_type)

        except Exception as e:
            pass
        try:
            answer = json_data["queryresult"]["pods"][1]["subpods"][3]["plaintext"]
            answer = answer.replace("sqrt", "√")

            self.send(Message(text=answer), thread_id=thread_id,
                      thread_type=thread_type)

        except Exception as e:
            pass
        try:
            answer = json_data["queryresult"]["pods"][1]["subpods"][4]["plaintext"]
            answer = answer.replace("sqrt", "√")

            self.send(Message(text=answer), thread_id=thread_id,
                      thread_type=thread_type)

        except Exception as e:
            pass
        try:
            answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
            answer = answer.replace("sqrt", "√")

            self.send(Message(text=answer), thread_id=thread_id,
                      thread_type=thread_type)

        except Exception as e:
            pass
        try:
            answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
            answer = answer.replace("sqrt", "√")

            self.send(Message(text=answer), thread_id=thread_id,
                      thread_type=thread_type)

        except Exception as e:
            pass

    def stepWiseCalculus(self, query, thread_id, thread_type):
        query = query.replace("+", "%2B")
        try:
            try:
                api_address = f"https://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Step-by-step%20solution&output=json&format=image"
                json_data = requests.get(api_address).json()
                answer = json_data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"]
                answer = answer.replace("sqrt", "√")

                if (thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif (thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
            except:
                pass
            try:
                api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
                json_data = requests.get(api_address).json()
                answer = json_data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
                answer = answer.replace("sqrt", "√")

                if (thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif (thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            except:
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][1]["img"]["src"]
                    answer = answer.replace("sqrt", "√")

                    if (thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif (thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                except:
                    pass
        except:
            pass

    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
        reply = f"You just unsent a message."
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
        # self.markAsDelivered(author_id, thread_id)
        # return
        if (author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                print("connected")
                c = conn.cursor()
                c.execute("""
                SELECT * FROM "{}" WHERE mid = "{}"
                """.format(str(author_id).replace('"', '""'), mid.replace('"', '""')))

                fetched_msg = c.fetchall()
                conn.commit()
                conn.close()
                unsent_msg = fetched_msg[0][1]

                if ("//video.xx.fbcdn" in unsent_msg):

                    if (thread_type == ThreadType.USER):
                        reply = f"You just unsent a video"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif (thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent a video"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                elif ("//scontent.xx.fbc" in unsent_msg):

                    if (thread_type == ThreadType.USER):
                        reply = f"You just unsent an image"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif (thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent an image"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                else:
                    if (thread_type == ThreadType.USER):
                        reply = f"You just unsent a message:\n{unsent_msg} "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                    elif (thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent a message:\n{unsent_msg}"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
            except:
                pass

    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You changed the theme ✌️😎"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onEmojiChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You changed the emoji 😎. Great!"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onImageChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "This image looks nice. 💕🔥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onNicknameChange(self, mid=None, author_id=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = f"You just changed the nickname to {new_nickname} But why? 😁🤔😶"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onReactionRemoved(self, mid=None, author_id=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You just removed reaction from the message."
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallStarted(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply = "You just started a call 📞🎥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallEnded(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply = "Bye 👋🙋‍♂️"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onUserJoinedCall(self, mid=None, joined_id=None, is_video_call=None,
                         thread_id=None, thread_type=None, **kwargs):
        reply = f"New user with user_id {joined_id} has joined a call"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)


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
