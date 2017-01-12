# Clover Orders Seeder

This script is intended to be used by developers to seed a Clover Sandbox account, assisting with your third party application development and testing. It creates orders and makes in-full, credit card payments for those orders using the Clover REST APIs. These orders are based on the pre-existing inventory of the merchant. Items are selected randomly, and each order consists of one item.

### General Usage

- Open the file in a text editor and configure the script on lines 5-9.
- Ensure that your merchant has at least 1 inventory item.
- To ensure payments are made in full, turn off all default taxes.  
`Clover Dashboard -> Setup > Taxes > Tax rates`
- Download the virtualenv packages with `pip install -r requirements.txt`
- Execute the script by running `python orders_seeder.py`

### Additional Information

The script consumes the following Clover API endpoints:  
- GET `v3/merchants/{MID}/items` to fetch a merchant's inventory
- POST `v3/merchants/{MID}/orders` to instantiate and/or update an open order  
- POST `v3/merchants/{MID}/orders/{orderID}/line_items` to add a line item to an order
- [Developer Pay API](https://docs.clover.com/build/developer-pay-api/):
    - GET `v2/merchant/{MID}/pay/key` to fetch a merchant's developer pay secrets
    - POST `v2/merchant/{MID}/pay` to process the payment

For development and testing questions, please reference [our docs](https://docs.clover.com/), our [public developer form](https://devask.clover.com/), or email us privately at [dev@clover.com](dev@clover.com).
