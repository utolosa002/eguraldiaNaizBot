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
MASTODON_URL = 'https://mastodon.eus'

def get_iragarpena(noiz):
    url = f'https://www.naiz.eus/eu/eguraldia/iker-ibarluzea'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.main
    job_elements = results.find_all("div", class_="area-main")
    iragarpena='';
    if len(job_elements) > 0:    
        if noiz=="gaurkoa":
            job_element = job_elements[0]
            title_element = job_element.find("h2")
            p_element   = job_element.find_all("p")
            i=0
            while p_element[i]=='' :
                 i=i+1
            iragarpena=title_element.text+"\n"+p_element[i].text
            iragarpena=iragarpena[:480]
            #print(p_element[i].text)
            #print(title_element.text)
        else:
            #TO-DO
            iragarpena="Biharko iragarpena"
    else:
        iragarpena="Gaur ez dago iragarpenik"
        
    return iragarpena
    

async def send_telegram(message):
    tgbot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await tgbot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_mastodon(message):
    Masto_api = Mastodon(
                access_token=MASTODON_ACCESS_TOKEN,
                api_base_url=MASTODON_URL
            )
    message=message[:500]
    Masto_api.status_post(message)

async def main():
    NOIZ="gaurkoa"
    iragarpena = get_iragarpena(NOIZ)
    await send_mastodon(iragarpena)
    await send_telegram(iragarpena)
   
if __name__ == '__main__':
    asyncio.run(main())