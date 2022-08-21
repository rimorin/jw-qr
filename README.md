# QR Generator for JW.ORG

![Screenshot 2022-08-17 at 4 14 29 PM](https://user-images.githubusercontent.com/40650158/185069239-52e93e3f-71bc-4eed-a713-6288060c6dcf.png)

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
   - Click on generate to generate QR template in word document based on the image and title of the article.

## Technologies Used

   - BeautifulSoup - Web scraper
   - Pillow - Image Manipulation
   - Gunicorn - Http Server
   - Docx - MS Word Generator
   - Css-loader - https://github.com/raphaelfabeni/css-loader#install 
