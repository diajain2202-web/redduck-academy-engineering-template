# Solution

## Language

<!-- Keep only the language you completed. Delete the others so a single value is left, e.g. language: "python" -->
language: "python"

## The attack

The attacker starts with 0 points and the victim with 100. The attacker calls
`transfer("attacker", "victim", -50)`. Although the call appears to transfer from attacker to
victim, subtracting a negative amount credits the attacker and adding it debits the victim. The
ending balances are attacker: 50 and victim: 50.

## Why it works at the design level

The API lets the caller choose any signed integer as an amount, while the implementation assumes
that amount is nonnegative. Its insufficient-funds check (`available < amount`) only protects
against spending too much when the amount is positive; a negative amount passes and reverses the
meaning of both balance updates. This is a mismatch between the public operation's accepted
values and its intended invariant, not a missing authorization check.

## Patch or elimination?

Rejecting amounts less than or equal to zero at the transfer boundary would patch this attack with
a runtime guard, but would leave signed values expressible and require the guard to remain
correct on every path. A stronger design makes the transfer operation accept only a validated
positive-amount type, constructed at the boundary, so negative amounts cannot be passed to the
ledger operation at all. That removes the condition that gives this attack its leverage instead
of relying only on checking it.
