from fbchat import Client, log, _graphql
from fbchat.models import *
from fbchat.models import ThreadType
from fun.logger import log, log_error
from chatbot.mybot import get_response
from settings.settings import blue, white, green, \
    red, yellow, line, line2, logo, DEBUG, \
    session, ACCOUNT, RUN
from settings.version import __check__, __clr__
import json
import random
import requests
import time
import math
import os
import sys

__check__()
clr = __clr__()

def check_message(self, message_object, author_id, uid):
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
                reply = get_response(msg)
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        except Exception as e:
            log_error(e)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        try:
            msg = check_message(
                message_object, author_id=author_id, uid=self.uid)
            if msg:
                print(msg)
                # Perform actions based on the message content
                self.message_proccessing_unit(
                    msg=msg, thread_id=thread_id, thread_type=thread_type)
        except Exception as e:
            print(f"Error in onMessage: {e}")
        self.markAsDelivered(author_id, thread_id)



def start_bot():
    cookies = json.loads(open("cookies/cookies.json", "r").read())
    client = Facebook_messenger("",
                                "", session_cookies=cookies)
    print(client.isLoggedIn())

    try:
        client.listen()
    except Exception as e:
        print(f"Error in listening: {e}")
        time.sleep(3)
        client.listen()
def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)
def main():
    os.system(clr)
    print(logo)
    print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mStart Chat-Bot")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mAdd Cookies")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mView Cookies")
    print("\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mLogin")
    print("\033[1;92m║ \033[1;91m5. \033[1;94m—> \033[1;92mUpdate")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    home_pick()


def home_pick():
    p = pick()
    if p == "1":
        start_bot()
        return
    if p == "2":
        pass
    elif p == "5":
        os.system("git pull")
        os.system("python3 main.py")

    elif p == "0":
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        home_pick()
if __name__ == "__main__":
    main()