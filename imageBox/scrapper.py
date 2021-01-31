import asyncio
from bs4 import BeautifulSoup
from random import choice
from aiohttp import ClientSession
import aiofiles
import configparser
import glob
import os

ALPHANUM = 'abcdefghijklmnopqrstuvwxyz0123456789'
IMAGE_ID_LEN = 6
BASE_URL = 'https://prnt.sc/{}'
TEMP_PATH = 'temp/{}.png'
SAVED_PATH = 'saved/{}.png'

def random_image_id():
    return ''.join([choice(ALPHANUM) for _ in range(IMAGE_ID_LEN)])

def custom_headers(): # for not being detected as a bot
    return {
            "ACCEPT" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "ACCEPT-LANGUAGE": "en-US,en;q=0.9",
            "DEVICE-MEMORY": "8",
            "DOWNLINK": "10",
            "DPR": "1",
            "ECT": "4g",
            "HOST": "prnt.sc",
            "REFERER": "https://www.google.com/",
            "RTT": "50",
            "SEC-FETCH-DEST": "document",
            "SEC-FETCH-MODE": "navigate",
            "SEC-FETCH-SITE": "cross-site",
            "SEC-FETCH-USER": "?1",
            "UPGRADE-INSECURE-REQUESTS": "1",
            "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "VIEWPORT-WIDTH": "1920",
        }

async def image_url_from_page(session, url):
    async with session.get(url, headers=custom_headers()) as resp:
        if resp.status != 200:
            raise Exception(f"Error {resp.status} for {url}")
        content = await resp.text()
        soup = BeautifulSoup(content,'html.parser')
        img_element = soup.find('img', {'id': 'screenshot-image'})
        if img_element is None:
            raise Exception(f"The {url} does not contain any image")
        return img_element['src']

async def download_image(session, image_url, image_id):
    final_path = TEMP_PATH.format(image_id)
    async with session.get(image_url) as resp:
        if resp.status != 200:
            raise Exception(f"Error {resp.status} for {url}")
        f = await aiofiles.open(final_path, mode='wb')
        await f.write(await resp.read())
        await f.close()
    return final_path

async def random_image():
    """Download a random image to temp file and return it name"""
    session = ClientSession()
    try:
        image_id = random_image_id()
        page_url = BASE_URL.format(image_id)
        image_url = await image_url_from_page(session, page_url)
        await download_image(session, image_url, image_id)
    except Exception as err:
        await session.close()
        raise err
    else:
        await session.close()
        return image_id

def clear_temp():
    files = glob.glob(TEMP_PATH.format('*'))
    for f in files:
        os.remove(f)

def next_image():
    clear_temp()
    return asyncio.run(random_image())

def save_image(image_id, name):
    os.replace(TEMP_PATH.format(image_id), SAVED_PATH.format(name))