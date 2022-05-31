# Arkham-LCG-translation-assistant

## Environments tested
- OS: Windows 10, macOS Monterey (M1)
- Python version: 3.9

## Installation
1. Set up python (using [anaconda](https://www.anaconda.com/products/distribution) is strongly recommended) and install requirements
    ```
    pip install -r requirements.txt
    ```
2. You may need to install `wkhtmltopdf` to use `imgkit`. See more details [here](https://pypi.org/project/imgkit/).
3. Install [Chrome](https://www.google.com/chrome/) and Download [chromedriver](https://chromedriver.chromium.org/downloads) that matches your [Chrome version](chrome://settings/help)

## How to use
1. Run following scripts
    ```
    python src/main.py
    ```
2. Type in Card ID and type `Enter`  
    The Card ID can be obtained from [arkhamdb.com](https://arkhamdb.com/)  
    For example, if you want to translate `Discipline`, you may obtain following URL.
    ```
    https://arkhamdb.com/card/08011a
    ```
    Here, `08011a` is the Card ID
3. For card name, card subname, and card trait, do followings
    1. Click `Drag & Insert` button
    2. On image left, drag area to insert text
4. For card text, do followings
    1. Type in font size (integer) of text to generate (33 is generally good)
    2. Click `Drag & Generate` button
    3. On image left, drag area to insert text
    4. You may see the generated text with specified area size and font size below
    5. If you like the generated text, click `Insert` button.  
        Otherwise, finetune by changing font size or text and redo from 4.2.
5. After all texts you want is inserted, click `Save` button.
6. For some cards with backside(e.g. 08011a), click `Do Backside` button to translate backside of the card.

## Arguments
```
usage: main.py [-h] [--chromedriver CHROMEDRIVER] [--image_scale IMAGE_SCALE] [--save_original_size]

optional arguments:
  -h, --help            show this help message and exit
  --chromedriver CHROMEDRIVER
                        Path to chromedriver
  --image_scale IMAGE_SCALE
                        Ratio to scale up/down image from original (300 * 420)
  --save_original_size  Whether to save image in original size (300 * 420)
```

## Customization
For some cards, the translation may not be supplied by Arkham DB.  
In this case, you can translate it by yourself.  
Type texts in the text box beneath the font size box.  
You can also insert icons by clicking the icons below.

## Licenses
- Images: all card images are downloaded from [Arkham DB](https://arkhamdb.com/)
- Chromedriver: https://chromedriver.chromium.org/downloads
- Fonts
    - arkham-icons: https://arkhamdb.com/bundles/app/fonts/arkham-icons.otf?
    - Namum fonts: https://hangeul.naver.com/2021/fonts/nanum
    - 경기천년 fonts: https://www.gg.go.kr/contents/contents.do?ciIdx=679&menuId=2457