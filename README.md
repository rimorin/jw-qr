# QR Generator for JW.ORG

View it live here: [jwqr.live](https://jwqr.live)

<img width="285" alt="Screenshot 2022-06-16 at 1 25 38 PM" src="https://user-images.githubusercontent.com/40650158/173997681-3edaf4c8-bb9e-4ef9-9206-09e7ff307fcf.png">

![jw-qr-ayqgb3rr4a-uc a run app](https://user-images.githubusercontent.com/40650158/163501990-a45af048-6dad-409d-a0d4-41b0a11da874.jpeg)

<img width="485" alt="Screenshot 2022-04-15 at 11 40 08 PM" src="https://user-images.githubusercontent.com/40650158/163591059-79740754-0385-40b3-9f3e-1f3a727faefc.png">

## Setup Instructions:

   1. Create virtual environment by running `python3 -m venv .venv`
   2. Activate virtual environment by running `source .venv/bin/activate`
   3. Install dependencies `pip install -r requirements.txt`
   4. Run server by running `gunicorn index:app`

## How to use:

   - Copy article from JW.org into your device clipboard
   - Click on paste
   - Click on generate to generate QR template in word document based on the image and title of the article

## Technologies Used

   - BeautifulSoup - Web scraper
   - Pillow - Image Manipulation
   - Gunicorn - Http Server
   - Docx - MS Word Generator 
