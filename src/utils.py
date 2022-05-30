import json
import wget
from typing import Union

from selenium import webdriver
from PIL import Image

import numpy as np
import cv2
import os
from PIL import ImageFont, ImageDraw, Image

import imgkit


ICON_TO_TEXT = {
    "icon-agility": "a",
    "icon-intellect": "b",
    "icon-lore": "b",
    "icon-combat": "c",
    "icon-strength": "c",
    "icon-rogue": "d",
    "icon-survivor": "e",
    "icon-guardian": "f",
    "icon-mystic": "g",
    "icon-seeker": "h",
    "icon-action": "i",
    "icon-fast": "j",
    "icon-free": "j",
    "icon-lightning": "j",
    "icon-skull": "k",
    "icon-cultist": "l",
    "icon-auto_fail": "m",
    "icon-elder_thing": "n",
    "icon-eldersign": "o",
    "icon-elder_sign": "o",
    "icon-willpower": "p",
    "icon-will": "p",
    "icon-tablet": "q",
    "icon-unique": "s",
    "icon-null": "t",
    "icon-per_investigator": "u",
    "icon-bless": "v",
    "icon-curse": "w",
    "icon-frost": "x",
    "icon-seal_a": "1",
    "icon-seal_b": "2",
    "icon-seal_c": "3",
    "icon-seal_d": "4",
    "icon-seal_e": "5",
    "icon-reaction": "!",
    "icon-wild": "?"
}


def download_from_link(url:str, output_path:str):
    wget.download(url, out=output_path)


def setup_chrome():
    driver = webdriver.Chrome(executable_path="data/chromedriver.exe")
    driver.set_window_size(1, 1)
    return driver


def close_chrome(driver):
    driver.close()


def load_image_with_scale(driver, img_path, scale=5, backside=False):
    if backside:
        image_xpath = '//*[@id="list"]/div[2]/div/div/div[4]/div/img'
    else:
        image_xpath = '//*[@id="list"]/div[2]/div/div/div[2]/div/img'

    if not os.path.isfile(img_path):
        card_image = driver.find_element_by_xpath(image_xpath)
        image_src = card_image.get_attribute('src')
        download_from_link(image_src, img_path)

    img = Image.open(img_path)
    img = img.resize((300 * scale, 420 * scale), Image.LANCZOS)

    return img


def check_backside_exist(driver):
    try:
        _ = driver.find_element_by_xpath('//*[@id="list"]/div[2]/div/div/div[4]/div/img')
        return True
    except:
        return False


def get_card_name(driver:webdriver.Chrome, backside=False):
    card_name_elems = driver.find_elements_by_class_name('card-name')
    if backside:
        card_name_elem = card_name_elems[1]
    else:
        card_name_elem = card_name_elems[0]

    card_name = card_name_elem.text

    return card_name


def get_card_subname(driver:webdriver.Chrome, backside=False):
    try:
        card_sub_name_elems = driver.find_elements_by_class_name('card-subname')
        if backside:
            card_sub_name_elem = card_sub_name_elems[1]
        else:
            card_sub_name_elem = card_sub_name_elems[0]
        card_sub_name = card_sub_name_elem.text
    except:
        card_sub_name = ""

    return card_sub_name


def get_card_trait(driver:webdriver.Chrome, backside=False):
    try:
        card_trait_elems = driver.find_elements_by_class_name('card-traits')
        if backside:
            card_trait_elem = card_trait_elems[1]
        else:
            card_trait_elem = card_trait_elems[0]
        card_trait = card_trait_elem.text
    except:
        card_trait = ""

    return card_trait


def get_card_text(driver:webdriver.Chrome, backside=False):
    try:
        card_text_box_elems = driver.find_elements_by_class_name('card-text')
        if backside:
            card_text_box_elem = card_text_box_elems[1]
        else:
            card_text_box_elem = card_text_box_elems[0]

        card_text_p_elems = card_text_box_elem.find_elements_by_tag_name('p')

        for card_text_p_elem in card_text_p_elems:
            spans = card_text_p_elem.find_elements_by_tag_name('span')
            for span in spans:
                span_classes = span.get_attribute('class')
                for span_class in span_classes.split():
                    if span_class in ICON_TO_TEXT:
                        text = ICON_TO_TEXT[span_class]
                        driver.execute_script(f"""arguments[0].innerText = '{text}'""", span)
                        driver.execute_script("""arguments[0].removeAttribute('class')""", span)
                        driver.execute_script("""arguments[0].removeAttribute('title')""", span)

        card_text = card_text_box_elem.get_attribute('innerHTML').strip()
    except:
        card_text = ""

    return card_text

def draw_text(img, text_type, text, top_left_pos, text_box_size, scale=5):
    if text_type == 'card_name':
        fontpath = "data/fonts/경기천년바탕_Bold.ttf"
        font = ImageFont.truetype(fontpath, 15 * scale)
    elif text_type == 'card_subname':
        fontpath = "data/fonts/경기천년바탕_Bold.ttf"
        font = ImageFont.truetype(fontpath, 9 * scale)
    elif text_type == 'card_trait':
        fontpath = "data/fonts/경기천년제목_Medium.ttf"
        font = ImageFont.truetype(fontpath, 11 * scale)
    
    draw = ImageDraw.Draw(img)
    text_size = font.getsize(text)
    text_x = ((text_box_size[0] - text_size[0]) / 2) + top_left_pos[0]
    text_y = ((text_box_size[1] - text_size[1]) / 2) + top_left_pos[1]
    draw.text((text_x, text_y),  text, font=font, anchor='la', fill=(0,0,0,0))

    return img


def draw_image_text(img, text, top_left_pos, text_box_size, font_size=20):
    text_img = card_text_to_img(text, text_box_size[0], text_box_size[1], font_size)
    img = put_text_on_img(img, text_img, top_left_pos, text_box_size)

    return img


def put_text_on_img(img, text_img, top_left_pos, text_box_size):
    text_area = [
        top_left_pos[0],                    # top-left x
        top_left_pos[1],                    # top-left y
        top_left_pos[0] + text_box_size[0], # bottom-right x
        top_left_pos[1] + text_box_size[1]  # bottom-right y
    ]

    img.paste(text_img, text_area, text_img)
    return img


def inpaint_image(img, top_left_pos, text_box_size):
    x0, y0 = top_left_pos
    dx, dy = text_box_size

    cv_img = np.array(img)
    if cv_img.shape[2] == 4:
        cv_img = cv_img[:, :, :-1]

    mask = np.zeros(cv_img.shape[:2], dtype="uint8")
    mask[y0:y0+dy, x0:x0+dx] = 1
    cv_img = cv2.inpaint(cv_img, mask, 20, cv2.INPAINT_TELEA)

    for y in range(y0, y0+dy):
        for x in range(x0, x0+dx):
            for c in range(cv_img.shape[2]):
                cv_img[y,x,c] = np.clip(cv_img[y,x,c], 200, 255)

    img = Image.fromarray(cv_img)

    return img


def card_text_to_img(text, width, height, font_size):
    options = {'width': width, 'height': height, 'transparent': '', 'enable-local-file-access': ''}
    # css = 'style.css'
    css = """
    <style>
        @font-face {
        font-family: arkham-icons; 
        src: url('file:///C:/Users/christopher/AppData/Local/Microsoft/Windows/Fonts/arkham-icons.otf') format('opentype');
        }

        @font-face {
            font-family: nanummj; 
            src: url('file:///C:/Users/christopher/AppData/Local/Microsoft/Windows/Fonts/NanumMyeongjo.ttf') format('truetype');
        }

        span { 
            font-family: 'arkham-icons', cursive; 
            font-size: """ + str(font_size) + """px;
        }

        p { 
            font-family: 'nanummj', cursive; 
            font-size: """ + str(font_size) + """px;
            margin: 0;
            word-break: keep-all;
        }
    </style>
    """
    imgkit.from_string(css + text, 'data/tmp/info.png', options=options)

    im = Image.open('data/tmp/info.png')

    return im
