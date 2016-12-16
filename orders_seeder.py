import requests
import json
from random import randint
import sys
from time import sleep
from Crypto.PublicKey import RSA
from base64 import b64encode

#######################################
############ GENERAL USAGE ############
#######################################
"""
This script creates orders and payments to those orders based on
the pre-existing inventory of a merchant. Items are selected randomly
and each order consists of just one item.

To ensure payments are made in full, turn off all default taxes.
    -> Setup > Taxes > Tax rates and toggle accordingly
"""

#######################################
######### BEGIN SCRIPT CONFIG #########
#######################################

MID = ""
API_TOKEN = ""
NUM_ORDERS = 777
ENVIRONMENT = "https://sandbox.dev.clover.com/"

#######################################
########## END SCRIPT CONFIG ##########
#######################################

######################################
########## OTHER CONSTANTS ###########
######################################
cardNumber = '4761739001010010'
expMonth = 12
expYear = 2018
CVV = None
######################################
######################################

itemIds = []
url = ENVIRONMENT + "v3/merchants/" + MID + "/items"
headers = {'Authorization': 'Bearer ' + API_TOKEN}
response = requests.get(url, headers=headers)
if (response.status_code != 200):
    print "Something went wrong fetching this merchant's items"
    sys.exit()

elements = json.loads(response.content)[u'elements']

for i in xrange(0, len(elements)):
    itemIds.append(str(elements[i][u'id']))

num_items = len(itemIds)
# for general usage
for i in xrange(0, NUM_ORDERS):
# for i in xrange(0, 1):
# for testing
    sleep(0.4)
    rand_item_index = randint(0, num_items - 1)
    url = ENVIRONMENT + "v3/merchants/" + MID + "/orders"
    response = requests.post(url, headers=headers, json={"state": "open"})
    if (response.status_code != 200):
        print "Something went wrong creating an order"
        sys.exit()
    orderId = response.json()[u'id']
    sleep(0.4)
    url = ENVIRONMENT + "v3/merchants/" + MID + "/orders/" + orderId + "/line_items"
    payload = { "item": { "id": itemIds[rand_item_index] } }
    response = requests.post(url, headers=headers, json=payload)
    if (response.status_code != 200):
        print "Something went wrong adding a line item to the order"
        sys.exit()

    price = response.json()[u'price']

    ########## BEGIN PAYMENT ##########
    # Getting secrets to encrypt cc info
    sleep(0.4)
    url = ENVIRONMENT + "v2/merchant/" + MID + '/pay/key'
    headers = {"Authorization": "Bearer " + API_TOKEN}
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        print "Something went wrong adding a line item to the order"
        sys.exit()
    response = response.json()

    modulus = long(response['modulus'])
    exponent = long(response['exponent'])
    prefix = long(response['prefix'])

    RSAkey = RSA.construct((modulus, exponent))

    publickey = RSAkey.publickey()
    encrypted = publickey.encrypt(cardNumber, prefix)
    cardEncrypted = b64encode(encrypted[0])

    post_data = {
        "orderId": orderId,
        "currency": "usd",
        "amount": long(price),
        "expMonth": expMonth,
        "cvv": CVV,
        "expYear": expYear,
        "cardEncrypted": cardEncrypted,
        "last4": cardNumber[-4:],
        "first6": cardNumber[0:6]
    }

    posturl = ENVIRONMENT + "v2/merchant/" + MID + '/pay'
    sleep(0.4)
    response = requests.post(
        posturl,
        headers = headers,
        data= post_data
        )
    if response.status_code != 200:
        print "Something went wrong during developer pay"
        sys.exit()

    url = ENVIRONMENT + "v3/merchants/" + MID + "/orders/" + orderId
    payload = {"total": long(price)}
    sleep(0.4)
    response = requests.post(url=url, headers=headers, json=payload)

    print str((float(i) / NUM_ORDERS) * 100) + "% complete"
