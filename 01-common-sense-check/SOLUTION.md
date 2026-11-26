# Solution

## Language

language: "python"

## The flaw

The checkout trusted each item's `price` from the order request instead of looking
up the price in the catalog. A shopper can change a request before it reaches the
service:

1. Select one blue T-shirt, listed in the catalog for 2,000 cents.
2. Change the submitted item to `{"productId": "sku-blue-tshirt", "quantity": 1, "price": 1}`.
3. Checkout multiplies the submitted quantity by the submitted price, stores a
   total of 1 cent, and lets the shopper pay less than the listed price.

## The fix

The request contains only the product ID and quantity. Checkout rejects
unknown product IDs and invalid quantities, then builds new stored order items
using the matching catalog prices and computes the total from those
server-controlled values.

## Patch or elimination?

This removes the condition that made the attack possible: a client-supplied
price is no longer part of the accepted request or used in the calculation.
Deriving prices from the catalog makes it the single source of truth, rather
than patching the attack by checking a price the client should never control.
