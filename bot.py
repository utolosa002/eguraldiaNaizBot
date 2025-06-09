import os
import requests
from telegram import Bot
import asyncio
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import *
from mastodon import Mastodon

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN')
NOIZ = os.getenv('NOIZ')
MASTODON_URL = 'https://mastodon.eus'

def get_iragarpena(noiz):
    url = f'https://www.naiz.eus/eu/eguraldia/iker-ibarluzea'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.main
    job_elements = results.find_all("div", class_="area-main")
    iragarpena='';
    if len(job_elements) > 0:    
        job_element = job_elements[0]
        if noiz=="goiza":
            title_element = job_element.find("h2")
            p_element   = job_element.find_all("p")
            i=0
            while p_element[i].text=='' :
                 i=i+1
            iragarpena=title_element.text+"\n"+p_element[i].text
            #print(p_element[i].text)
            #print(title_element.text)
        else:
            title_element = job_element.find_all("h2")
            if len(title_element) > 1:    
                title_element = title_element[1]
            p_element   = job_element.find_all("p")
            i=0
            while p_element[i].text=='' or p_element[i].text== p_element[i+1].text:
                if len(p_element) > i+1 :
                    i=i+1   
            if len(p_element) > i+1 :
                i=i+1
            iragarpena=title_element.text+"\n"+p_element[i].text
    else:
        iragarpena="Gaur ez dago iragarpenik"
        
    return iragarpena
    

async def send_telegram(message):
    tgbot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await tgbot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message+ ' https://www.naiz.eus/eu/eguraldia/iker-ibarluzea')

async def send_mastodon(message):
    Masto_api = Mastodon(
                access_token=MASTODON_ACCESS_TOKEN,
                api_base_url=MASTODON_URL
            )
    message=message[:445]
    Masto_api.status_post(message+ ' https://www.naiz.eus/eu/eguraldia/iker-ibarluzea')

async def main():
    iragarpena = get_iragarpena(NOIZ)
    await send_mastodon(iragarpena)
    await send_telegram(iragarpena)
   
if __name__ == '__main__':
    asyncio.run(main())