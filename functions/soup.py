import json
import bs4
import sys
import requests
from requests import Response
from .logger import log, log_error
from settings.settings import DEBUG
from settings.settings import green, yellow
from typing import List

def save_ongoing_chat():
    try:
        conn = sqlite3.connect("messages.db")
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS "{}" (
            mid text PRIMARY KEY,
            message text NOT NULL
        );

        """.format(str(author_id).replace('"', '""')))

        c.execute("""

        INSERT INTO "{}" VALUES (?, ?)

        """.format(str(author_id).replace('"', '""')), (str(mid), msg))
        conn.commit()
        conn.close()
    except:
        pass

def weather(city):
    api_address = "https://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
    url = api_address + city
    json_data = requests.get(url).json()
    kelvin_res = json_data["main"]["temp"]
    feels_like = json_data["main"]["feels_like"]
    description = json_data["weather"][0]["description"]
    celcius_res = kelvin_res - 273.15
    max_temp = json_data["main"]["temp_max"]
    min_temp = json_data["main"]["temp_min"]
    visibility = json_data["visibility"]
    pressure = json_data["main"]["pressure"]
    humidity = json_data["main"]["humidity"]
    wind_speed = json_data["wind"]["speed"]

    return(
        f"The current temperature of {city} is %.1f degree celcius with {description}" % celcius_res)

def stepWiseCalculus(query):
    query = query.replace("+", "%2B")
    try:
        try:
            api_address = f"https://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Step-by-step%20solution&output=json&format=image"
            json_data = requests.get(api_address).json()
            answer = json_data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"]
            answer = answer.replace("sqrt", "√")

            if(thread_type == ThreadType.USER):
                self.sendRemoteFiles(
                    file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
            elif(thread_type == ThreadType.GROUP):
                self.sendRemoteFiles(
                    file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
        except:
            pass
        try:
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            answer = json_data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
            answer = answer.replace("sqrt", "√")

            if(thread_type == ThreadType.USER):
                self.sendRemoteFiles(
                    file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
            elif(thread_type == ThreadType.GROUP):
                self.sendRemoteFiles(
                    file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

        except:
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][1]["img"]["src"]
                answer = answer.replace("sqrt", "√")

                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            except:
                pass
    except:
        pass

def stepWiseAlgebra(query):
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

def stepWiseQueries(query):
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

def programming_solution(self, query):
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

def translator(self, query, target):
    query = " ".join(query.split()[1:-2])
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {"to": target, "api-version": "3.0",
                   "profanityAction": "NoAction", "textType": "plain"}

    payload = f'[{{"Text": "{query}"}}]'

    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
        'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring)

    json_response = eval(response.text)

    return json_response[0]["translations"][0]["text"]

def imageSearch(self, msg):
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

def searchFiles(self):
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



def get_youtube_link(message: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    link = "".join(message.split()[-3:])
    yt_url = link
    print("yt", yt_url)
    try:
        yt_url = yt_url.replace(
            "youtu.be/", "www.youtube.com/watch?v=")
    except:
        pass
    yt_url = yt_url.replace("youtube", "clipmega")
    url = requests.get(yt_url, headers=headers)
    soup = bs4.BeautifulSoup(url.text, "html.parser")
    link = soup.select(".btn-group > a")
    link = link[0]
    link = str(link)
    indx = link.find("href=")
    indx_l = link.find("extension=mp4")
    link = link[indx+6:indx_l+13].replace("amp;", "")
    link = link.replace(" ", "%20")
    final_link = link
    print("final", final_link)
    return final_link

def find_input_fields(html):
    return bs4.BeautifulSoup(html, "html.parser", parse_only=bs4.SoupStrainer("input"))

def find_url(page):
    try:
        soup = bs4.BeautifulSoup(page, "html.parser")
        url = soup.find("form").get("action")
        return (f"https://m.facebook.com:443{url}")
    except AttributeError as e:
        log_error(e)
        # a = input(f"{yellow}Show error page?[y/n]")
        # if a == 'y':
        #     log_error(page)
        sys.exit()

def get_input_data(page):
    soup_data = find_input_fields(page.text)
    data = dict(
        (elem["name"], elem["value"])
        for elem in soup_data
        if elem.has_attr("value") and elem.has_attr("name")
    )
    return data

def create_form_2fa(page):
    action_url = find_url(page.text)
    data = get_input_data(page)
    data['submit[Continue]'] = "continue"
    if 'submit[logout-button-with-confirm]' in data:
        del data['submit[logout-button-with-confirm]']
    return action_url, data


def create_form(response:Response)->List:
    action_url = find_url(response.text)
    data = get_input_data(page=response)
    data["login"] = "Log in"
    if "sign_up" in data:
        del (data["sign_up"])
    return data, action_url

def get_page_title(page_text):
    try:
        s = bs4.BeautifulSoup(page_text, "html.parser")
        title = s.title.text.strip()
        return title
    except Exception as e:
        log_error(e)
        return "none"

def get_title_message(page):
    try:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        title_div = soup.select_one('div#checkpoint_title')
        title_msg = title_div.get_text(strip=True)
    except Exception as e:
        if DEBUG:
            log_error(e)
        title_msg = None
    return title_msg

def get_title_dexcription(page):
    try:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        div_element = soup.select_one('form.checkpoint div._50f4')
        text_div = div_element.select_one('div.y.z div')
        title_dexcription = text_div.get_text(strip=True)
    except Exception as e:
        if DEBUG:
            log_error(e)
        title_dexcription = None
    return title_dexcription

def print_page_title(page_text: str)->None:
      try:
            s = bs4.BeautifulSoup(page_text, "html.parser")
            title_text = s.title.text.strip()
            print(f"\033[1;92m║ {yellow}{title_text}")
      except Exception as e:
            #log_error(e)
            pass

def _print_page__(page_text: str, pritie: bool=False)->None:
    try:
        s = bs4.BeautifulSoup(page_text, "html.parser")
        
        if pritie:
                print(s.prettify())
        else:
                print(page_text)
    except Exception as e:
        #log_error(e)
        pass