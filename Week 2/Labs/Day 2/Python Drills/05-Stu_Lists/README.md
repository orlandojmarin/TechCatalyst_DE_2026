# The Claim Queue

In this activity, you will work with lists to manage a queue of claim ids. You
will create a list, slice it, append to it, change items by index, and remove
items.

## Background

An adjuster starts the day with a queue of open claims to work. Through the day
the queue changes: new claims arrive, one claim gets reopened, others close out.
You will model that queue as a Python list and update it as the day goes on.

## Instructions

Copy `Unsolved/Core/claim_queue_core.py` to your project and complete the following steps.

1. Create the day's claim queue:

    * CLM-1001
    * CLM-1002
    * CLM-1003
    * CLM-1004
    * CLM-1005
    * CLM-1006
    * CLM-1007

2. Find the first two claims in the queue.

3. Find every claim except the first two.

4. Find _every other_ claim, starting from the second claim.

5. A new claim arrives. Append `CLM-1008` to the queue.

6. `CLM-1004` is reopened. Change it to `CLM-1004-REOPEN`.

7. Determine the total number of claims in the queue.

## Challenge

As the adjuster works the queue, help them update it.

* Find where `CLM-1004-REOPEN` sits in the queue by its index.

* `CLM-1006` just closed. Remove it from the queue by value.

* `CLM-1001` was transferred to another adjuster. Remove it by its index.

* The adjuster picks up the last claim in the queue, so remove the last item.

## Stretch: tuples

A tuple is an immutable record (it cannot be changed after creation). Tuples are
great for fixed records and for unpacking.

```python
claim = ("CLM-1", "auto", 5000.0)   # a fixed record
cid, ptype, reserve = claim          # unpacking into three variables
print(cid, ptype, reserve)

# unpack inside a loop
for cid, reserve in [("CLM-1", 5000), ("CLM-2", 3000)]:
    print(cid, reserve)
```

Try `claim[0] = "X"` and read the `TypeError`: tuples are immutable, which is the
whole point when you want a record that should not change.
