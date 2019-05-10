#######################################
######### BEGIN SCRIPT CONFIG #########
#######################################

MID = ""
API_TOKEN = ""
NUM_ORDERS = 50
ENVIRONMENT = "https://sandbox.dev.clover.com/" # or https://api.clover.com/ or https://eu.clover.com/

#######################################
########## END SCRIPT CONFIG ##########
#######################################

######################################
########## OTHER CONSTANTS ###########
######################################
cardNumber = "6011361000006668"
expMonth = 12
expYear = 2020
CVV = None
######################################
######################################

import requests
import json
from random import randint
import sys
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode

# Fetch all items from a merchant
itemIds = []
url = ENVIRONMENT + "v3/merchants/" + MID + "/items"
headers = {"Authorization": "Bearer " + API_TOKEN}
response = requests.get(url, headers=headers)
if (response.status_code != 200):
    print("Something went wrong fetching this merchant's items")
    sys.exit()

elements = json.loads(response.content)[u"elements"]

for i in range(0, len(elements)):
    itemIds.append(str(elements[i][u"id"]))

num_items = len(itemIds)
if (num_items == 0):
    print("This merchant has no inventory. Create items and then re-run this script.")
    sys.exit()

# Fetch developer pay secrets from GET /v2/merchant/{mId}/pay/key
url = ENVIRONMENT + "v2/merchant/" + MID + "/pay/key"
headers = {"Authorization": "Bearer " + API_TOKEN}
response = requests.get(url, headers = headers)
if response.status_code != 200:
    print("Something went wrong fetching Developer Pay API secrets")
    sys.exit()
response = response.json()

modulus = int(response["modulus"])
exponent = int(response["exponent"])
prefix = str(response["prefix"])

RSAkey = RSA.construct((modulus, exponent))

# helper function
def print_progress(i):
    print((str((float(i) / NUM_ORDERS) * 100)) + "% complete")

for i in range(0, NUM_ORDERS):
    sleep(0.1)
    rand_item_index = randint(0, num_items - 1)
    url = ENVIRONMENT + "v3/merchants/" + MID + "/orders"
    response = requests.post(url, headers=headers, json={"state": "open"})
    if (response.status_code != 200):
        print("Something went wrong creating an order")
        sys.exit()
    orderId = response.json()[u"id"]
    sleep(0.1)
    url = ENVIRONMENT + "v3/merchants/" + MID + "/orders/" + orderId + "/line_items"
    payload = { "item": { "id": itemIds[rand_item_index] } }
    response = requests.post(url, headers=headers, json=payload)
    if (response.status_code != 200):
        print("Something went wrong adding a line item to the order")
        sys.exit()

    price = response.json()[u"price"]

    ########## BEGIN PAYMENT ##########
    # create a cipher from the RSA key and use it to encrypt the card number, prepended with the prefix from GET /v2/merchant/{mId}/pay/key
    cipher = PKCS1_OAEP.new(RSAkey)
    # encode str to byte (https://eli.thegreenplace.net/2012/01/30/the-bytesstr-dichotomy-in-python-3)
    encrypted = cipher.encrypt((prefix + cardNumber).encode())

    # Base64 encode the resulting encrypted data into a string to use as the cardEncrypted' property.
    cardEncrypted = b64encode(encrypted)

    post_data = {
        "orderId": orderId,
        "currency": "usd",
        "amount": int(price),
        "expMonth": expMonth,
        "cvv": CVV,
        "expYear": expYear,
        "cardEncrypted": cardEncrypted,
        "last4": cardNumber[-4:],
        "first6": cardNumber[0:6]
    }

    posturl = ENVIRONMENT + "v2/merchant/" + MID + "/pay"
    sleep(0.1)
    response = requests.post(
        posturl,
        headers = headers,
        data= post_data
        )
    if response.status_code != 200:
        print("Something went wrong during developer pay")
        sys.exit()

    url = ENVIRONMENT + "v3/merchants/" + MID + "/orders/" + orderId
    payload = {"total": int(price)}
    sleep(0.1)
    response = requests.post(url=url, headers=headers, json=payload)
    if response.status_code != 200:
        print("Something went wrong updating order total")
        sys.exit()

    print_progress(i)
