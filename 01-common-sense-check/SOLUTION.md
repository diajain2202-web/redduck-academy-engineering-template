# Solution

## Language

language: "typescript"

## The flaw

The checkout trusted each item's `price` from the order request instead of looking
up the price in the catalog.

An attacker could exploit it like this:

1. Select the blue T-shirt, whose catalog price is 2,000 cents.
2. Send an order for one T-shirt with `price: 1` in the request.
3. Checkout calculates and stores a total of 1 cent, and the attacker pays far
   less than the listed price.

## The fix

The request no longer accepts a price. It contains only the product ID and
quantity. Checkout rejects unknown product IDs, then builds the stored order
items using the matching catalog prices and computes the total from those
server-controlled values. It also rejects invalid quantities and totals that
cannot be represented safely.

## Patch or elimination?

This removes the condition that made the attack possible: clients cannot supply
an item price to be trusted in the first place. Merely checking a supplied price
would leave an unnecessary value in the API and rely on every path validating it
correctly. Deriving it from the catalog makes the catalog the single source of
truth.
