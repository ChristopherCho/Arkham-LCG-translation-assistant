# Arkham-LCG-translation-assistant

## Environments tested
- Windows 10

## How to use
1. Set up python (using [anaconda](https://www.anaconda.com/products/distribution) is strongly recommended) and install requirements
    ```
    pip install -r requirements.txt
    ```
2. You may need to install `wkhtmltopdf` to use `imgkit`. See more details [here](https://pypi.org/project/imgkit/).
3. Run following scripts
    ```
    python src/main.py
    ```
4. Type in Card ID and type `Enter`  
    The Card ID can be obtained from [arkhamdb.com](https://arkhamdb.com/)  
    For example, if you want to translate `Discipline`, you may obtain following URL.
    ```
    https://arkhamdb.com/card/08011a
    ```
    Here, `08011a` is the Card ID
5. For card name, card subname, and card trait, do followings
    1. Click `Drag & Insert` button
    2. On image left, drag area to insert text
6. For card text, do followings
    1. Type in font size (integer) of text to generate (33 is generally good)
    2. Click `Drag & Generate` button
    3. On image left, drag area to insert text
    4. You may see the generated text with specified area size and font size below
    5. If you like the generated text, click `Insert` button. Otherwise, re-do all from 1.
7. After all texts you want is inserted, click `Save` button.
8. For some cards with backside(e.g. 08011a), click `Do Backside` button to translate backside of the card.