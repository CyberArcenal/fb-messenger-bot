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
from functions.ck import save_cookies_in_the_list, \
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
import mybot
import threading
import json
import random
import requests
import time
import math
import os
import sys
import re
try:
    from fbchat import Client, log, _graphql
    from fbchat.models import *
    from fbchat.models import ThreadType
    from icecream import ic
    import concurrent.futures
    import wolframalpha
except:
    os.system("pip install -r requirements.txt")
try:
    import sqlite3
except:
    pass
try:
    import openai
except:
    pass



def chatGPT(query):
    try:
        api = json.load(open("openai_key.json", "r"))
        client = openai.OpenAI(
            # This is the default and can be omitted
            # api_key=os.environ.get("OPENAI_API_KEY")
            api_key=api['api_key'],
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": "Say this is a test"}],
            stream=False,
        )
        return (completion.choices[0].message.content)
    except Exception as e:
        log_error(e)
        return None


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
    def display_session_cookies(self):
        try:
            current_cookies = self.getSession()
            log(current_cookies)
        except AttributeError:
            log_error("Error: 'getSession()' did not return a valid session object.")
        
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
            self.TypingStatusStart(thread_id=thread_id,
                                   thread_type=thread_type)
            time.sleep(2)
            self.send(Message(text=f"Finding {name} in facebook please wait."), thread_id=thread_id,
                      thread_type=thread_type)
            self.TypingStatusStop(thread_id=thread_id, thread_type=thread_type)
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
        msg = msg.lower()
        try:
            if "search" in msg and "user" in msg or "search" in msg and "friend" in msg or "pakihanap" in msg and "si" in msg:
                self.searchUser(msg=msg, thread_id=thread_id,
                                thread_type=thread_type)
            elif ("chatgpt" in msg or "darius ai" in msg or "darius" and "ai" in msg):
                for word in ["chatgpt", "darius ai", "darius", "ai"]:
                    msg = msg.replace(word, "")
                reply = chatGPT(msg)
                if reply is not None:
                    reply = f"Darius AI: {reply}"
                    self.send(Message(text=reply), thread_id=thread_id,
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
                if "//video.xx.fbcdn" not in msg:
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
