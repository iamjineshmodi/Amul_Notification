import requests
import json
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

# API endpoint URL
url = "https://shop.amul.com/api/1/entity/ms.products"

# Query parameters
params = {
    "fields[name]": 1,
    "fields[brand]": 1,
    "fields[available]": 1,
    "fields[inventory_quantity]": 1,
    "fields[net_quantity]": 1,
    "fields[variants]": 1,
    "fields[lp_seller_ids]": 1,
    "filters[0][field]": "categories",
    "filters[0][value][0]": "protein",
    "filters[0][operator]": "in",
    "filters[0][original]": 1,
    "substore": "66505ff8c8f2d6e221b9180c"
}

# Request headers
headers = {
    "Host": "shop.amul.com",
    "Cookie": "jsessionid=s%3Ac77ma5eLLm%2BiI3INtfoLeJ7x.ePXgBjsO%2FI6TqCorOd8Q%2BiINaS7I8o%2F1SJPK14BV2WY; __cf_bm=Jg10G_VIUUMuk3VPOVOx9j01SJhx2.D0rZql2CU1obQ-1747378623-1.0.1.1-6gxZbABiBLVxJ7Wi6UE_WWH7EwWTNrkoau7nVrsVjATpEgYdBjml0JRU0T4LrXSQKdHhfS1x5fkbz8nVcfa5Swd2ZBTAtfRRGMVyP0_iwSg; *fbp=fb.1.1747378640289.704574872682371498; *ga=GA1.1.312855089.1747378655; *ga*E69VZ8HPCN=GS2.1.s1747378654$o1$g1$t1747379505$j60$l0$h876166667",
    "Sec-Ch-Ua-Platform": "macOS",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"99\", \"Chromium\";v=\"136\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Frontend": "1",
    "Tid": "1747379505241:837:6427f7bbd7473939ffbf3d4715a96d3f94d923a36464eb857bd396eb67663e76",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Base_url": "https://shop.amul.com/en/browse/protein",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://shop.amul.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "If-None-Match": "W/\"-240578986\"",
    "Priority": "u=1, i"
}

try:
    # Make the GET request
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        # as (id, name, available, inventory_quantity)
        products = []
        for i in range(len(data["data"])):
            tuple1 = (data["data"][i]["_id"], data["data"][i]["name"], data["data"][i]["available"], data["data"][i]["inventory_quantity"])
            products.append(tuple1)

        # print(products)
        # positive cases:
            # amul protein lassi available, amul protein paneer, or (optional whey powder available as well)

        # Check if Amul protein lassi is available
        lassi_available = False
        for product in products:
            product_id, name, available, inventory = product
            if ("lassi" in name.lower() or "buttermilk" in name.lower()) and available == 1 and inventory > 0:
                lassi_available = True
        #         print(f"Amul protein lassi is available: {name} (Inventory: {inventory})")
        
        # if not lassi_available:
        #     print("Amul protein lassi is not available")
        

        # Check if Amul protein paneer is available
        paneer_available = False
        for product in products:
            product_id, name, available, inventory = product
            if "paneer" in name.lower() and available == 1 and inventory > 0:
                paneer_available = True
                # print(f"Amul protein paneer is available: {name} (Inventory: {inventory})")
            
        # if not paneer_available:
        #     print("Amul protein paneer is not available")


        # Check if Amul protein whey is available
        whey_available = False
        for product in products:
            product_id, name, available, inventory = product
            if "whey" in name.lower() and available == 1 and inventory > 0:
                whey_available = True
                # print(f"Amul protein whey is available: {name} (Inventory: {inventory})")
            
        # if not whey_available:
        #     print("Amul protein whey is not available")

        if sum([paneer_available, lassi_available, whey_available]) >= 2:
            print("yes possible, now sending message to phone")
            # sending message using twilio api
            #  ******************************
            command = (
                f"curl 'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json' -X POST "
                f"--data-urlencode 'To={RECIPIENT_PHONE_NUMBER}' "
                f"--data-urlencode 'From={TWILIO_PHONE_NUMBER}' "
                "--data-urlencode 'Body=yes, Protein product is available now at Amul website' "
                f"-u {TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}"
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            #  ******************************

    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")