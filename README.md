# QR Generator for JW.ORG

![Screenshot 2023-01-10 at 1 49 53 PM](https://user-images.githubusercontent.com/40650158/211471794-8de9fb5a-5c0a-4f04-bc43-8047a032c100.png)

![design_1](https://user-images.githubusercontent.com/40650158/185069369-e9720bd5-f49c-4e9f-aab8-85100e128546.jpg)

![Screenshot 2022-08-17 at 4 16 08 PM](https://user-images.githubusercontent.com/40650158/185069592-8efe559a-af8e-412c-849c-2e779001b787.png)


## Setup Instructions:

   1. Create virtual environment by running `python3 -m venv .venv`
   2. Activate virtual environment by running `source .venv/bin/activate`
   3. Install dependencies `pip install -r requirements.txt`
   4. Run server by running `gunicorn index:app`

## How to use:

   - Copy article from JW.org into your device clipboard.
   - Click on paste.
   - If you would like a sample letter to be generated, click on the `include sample letter?` checkbox.
   - Click on generate to generate QR template in word document based on the image and title of the article.

## Technologies Used

   - BeautifulSoup - Web scraper
   - Pillow - Image Manipulation
   - Gunicorn - Http Server
   - Docx - MS Word Generator
   - Css-loader - https://github.com/raphaelfabeni/css-loader#install
   - OpenAI Davinci Model
