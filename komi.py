import os

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

base_url = "https://bato.to"


def save_image(div, title, folder):
    chapter = title.split("-")[0].strip().split(".")[-1].zfill(3)
    img_url = div.find("img").attrs["src"]
    img_page_full = div.find("span", {"class": "page-num"}).contents[0]
    img_page = img_page_full.split('/')[0].strip().zfill(3)
    print(f"Downloading image: {img_page_full}")

    image_request = requests.get(img_url, headers={'User-Agent' : "Magic Browser"})
    if image_request.status_code == 200:
        filename = f"./{folder}/{title}/{chapter}{img_page}.jpg"
        print(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(image_request.content)


def download_chapter(path, driver, folder):
    url = f"{base_url}{path}"
    print(f"\nDownloading {url}")
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find("option", selected=True).contents[0] \
        .replace(":", "-") \
        .replace("\"", "'") \
        .replace("...", "") \
        .replace("?", "")
    print(f"Title: {title}")
    viewer = soup.find("div", {"id": "viewer"})
    divs = viewer.find_all("div", {"class": "item"})

    for div in divs:
        save_image(div, title, folder)

    next_path_div = soup.find("div", {"class": "nav-next"})
    if next_path_div:
        next_path = next_path_div.find("a").attrs["href"]
        
        if "chapter" in next_path:
            download_chapter(next_path, driver, folder)


if __name__ == "__main__":
    # print("Enter path: ")
    # input_path = input()
    input_path = "/chapter/323077"
    input_folder = 'komi'

    options = Options()
    options.headless = True
    with webdriver.Firefox(options=options, executable_path=r'./geckodriver/geckodriver.exe') as gecko_driver:
        download_chapter(input_path, gecko_driver, input_folder)
