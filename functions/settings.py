import os
from settings.version import __check__, __clr__
from settings.settings import blue, white, green, \
    red, yellow, line, line2, logo, DEBUG, \
    session, ACCOUNT
from functions.ck import save_cookies_in_the_list, display_cookies, \
    save_cookies, clean_cookie, clear_cookies, clear_logs, \
    open_cookie_list, open_cookies, switch_cookiefile
from functions.logger import log, log_error
from icecream import ic
import json, time

def pick():
    user_input = input("\033[1;92m╚═════\033[1;91m>>>\033[1;97m ")
    return str(user_input)


def Switch_Account():
     os.system(__clr__())
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
               settings()
          log("Switching account...")
          time.sleep(2)
          switch_cookiefile(cookie_list["cookies_list"][int(a)]["cookies"])
          return_home()
   
     except Exception as e:
          log_error(e)
          input()
          return_home()
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
    os.system(__clr__())
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
            settings()
        display_cookiefile(cookie_list["cookies_list"][int(a)]["cookies"])
    except Exception as e:
        log_error(e)
        input()
        View_Cookies()
def settings():
     os.system(__clr__())
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
     print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mSwitch Account")
     print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mView Cookies")
     print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mReset Bot")
     print("\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mUpdate")
     print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mBack")
     settings_pick()
     return_home()

def return_home():
     from main import home
     home() 

def reset_bot():
     print("\033[1;92m║ \033[1;91mAre you sure you want to reset your bot memory?[y/n]")
     choose = pick()
     if choose.lower() == "y":
          print("\033[1;92m║ \033[1;91mDeleting data...")
          from browser.browser import wait
          wait()
          try:
               os.remove("data/config.json")
               
          except Exception as e:
               log_error(e)
     else:
          print("\033[1;92m║ \033[1;92mDelete canceled.")
          input()
          return_home()
          

def settings_pick():
     while True:
          p = pick()
          if p == "1":
               Switch_Account()
          elif p == "2":
               View_Cookies()
          elif p == "3":
               reset_bot()
          elif p == "4":
               os.system("git pull")
               os.system("python3 main.py")
          elif p == "0":
               return_home()
          else:
               print("\033[1;92m║ \033[1;91minvalid input")
