# Solution

Answer all three problems. For each one, give your verdict, state the exact constraint in words, and
explain your reasoning. When you claim a bypass, show how it makes the constraint irrelevant.

## Problem 1

**Verdict:** bypass exists

**The exact constraint:** The obvious design assumes each dashboard request must read every
record to calculate the total.

**Reasoning:** The dashboard needs the correct total, but it does not inherently need to
recalculate it from the underlying records every time it is displayed. The total can be kept
as derived state and updated when the source records change.

**How it removes the constraint:** Maintain an aggregate alongside the records. On each insert,
update, or delete, atomically adjust the aggregate by the corresponding change in value. The
dashboard reads that aggregate rather than scanning the records, so displaying the total no
longer requires reading all one hundred thousand records. An initial build or repair may scan
the records, but routine dashboard reads do not.

## Problem 2

**Verdict:** no bypass exists

**The exact constraint:** The only evidence available to the sender is messages over a channel
that may silently drop any message, including confirmations.

**Reasoning:** This limitation is intrinsic to the requested outcome: the sender must know the
recipient received the message. If the sender gets no acknowledgement, its observations are
identical in two cases: the original message was dropped, or it arrived and the acknowledgement
was dropped. Retrying cannot distinguish those cases, because every retry and acknowledgement
may also be dropped. No finite exchange over this channel can guarantee the sender's certainty.

**Why there is no bypass:** A reliable independent observation, such as a separate trusted
channel or shared system that records recipient receipt, would change the premise. Without such
an observation, certainty about receipt cannot be obtained. More retries may increase the
chance of delivery, but do not remove the constraint or establish certainty.

## Problem 3

**Verdict:** bypass exists

**The exact constraint:** The obvious design assumes it must detect and block a second click
before the first charge completes.

**Reasoning:** The required outcome is at most one charge for one intended payment, not
necessarily one request or one click. Multiple requests can be made safe by making them
represent the same payment operation.

**How it removes the constraint:** Assign a stable idempotency key to the payment intent before
submission and reuse that same key for every click, retry, and concurrent request representing
that intent. The payment backend (and payment provider, if used) atomically records the key with
the charge and returns the original result for later requests using it. The system therefore
does not need to catch the second click in time: even if both requests arrive together, they
cannot create two charges for the same key. The key must be shared by duplicate submissions,
not newly generated for each click.
