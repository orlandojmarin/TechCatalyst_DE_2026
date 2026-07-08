# Week 2 Day 3 Exit Ticket
# Score 100

## Q1: Which pair of Requests options should every call in today's API work include?
- [ ] `stream=True` and `verify=False`
- [x] `params=...` and `timeout=10`
- [ ] `auth=...` and `cookies=...`
- [ ] `files=...` and `headers=...`
::time=20

## Q2: Why should you call `raise_for_status()` after an API request?
- [ ] It converts CSV rows into dictionaries.
- [ ] It automatically retries every failed request.
- [ ] It removes duplicate records from the response.
- [x] It turns HTTP failure responses into exceptions the script can handle.
::time=25

## Q3: What is the safest reason to include `max_pages` in a pagination loop?
- [x] It prevents runaway loops and accidental huge downloads.
- [ ] It makes every API response come back faster.
- [ ] It guarantees the results contain no missing records.
- [ ] It removes the need to check the response status.
::time=25

## Q4: Why does fetching 8 cities with `asyncio.gather` usually finish faster than a plain `for` loop of the same requests?
- [ ] It splits the work across several CPU cores at once.
- [ ] It caches each response so repeated calls return instantly.
- [x] It overlaps the network waiting across all the requests.
- [ ] It skips any request that is taking too long to return.
::time=30

## Q5: What does an SDK like `boto3` or `google-genai` mainly add over calling the raw HTTP API yourself?
- [ ] Access to capabilities the underlying HTTP API cannot provide at all.
- [x] It handles auth, request signing, retries, and pagination for you.
- [ ] It makes an otherwise paid service free to use.
- [ ] It removes the need for an internet connection entirely.
::time=30
