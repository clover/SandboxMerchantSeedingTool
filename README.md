# Clover Orders Seeder

This script is intended to be used to seed a Clover Sandbox account to assist with third party Clover application development and testing. It creates orders and makes in-full, credit card payments for those orders. These orders are based on the pre-existing inventory of the merchant. Items are selected randomly, and each order consists of one item.



To ensure payments are made in full, turn off all default taxes.  
`Clover Dashboard -> Setup > Taxes > Tax rates`

The script consumes the following Clover API endpoints:  
- GET `v3/merchants/{MID}/items` to fetch a merchant's inventory
- POST `v3/merchants/{MID}/orders` to instantiate and/or update an open order  
- POST `v3/merchants/{MID}/orders/{orderID}/line_items` to add a line item to an order
- [Developer Pay API](https://docs.clover.com/build/developer-pay-api/):
    - GET `v2/merchant/{MID}/pay/key` to fetch a merchant's developer pay secrets
    - POST `v2/merchant/{MID}/pay` to process the payment
