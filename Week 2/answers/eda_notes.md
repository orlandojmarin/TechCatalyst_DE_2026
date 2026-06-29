# Mini EDA Notes

## File Profile

- Files I found: `data/orders_sample.csv`, `data/returns_2026-06.csv`, `data/clickstream_2026-06.jsonl`, `logs/pipeline.log`, `notes/.secret_flag`, `scripts/run_etl.sh`
- Largest direct folder: notes and data (both 16K)
- One file I want to inspect: `data/orders_sample.csv`

## Orders Profile

- Total lines: 16
- Data rows: 15
- Columns: order_id, store, amount, region
- One row-level observation: amounts vary a lot, from as low as 12.75 to over 200

## Store Profile

- Unique store count: 5
- Store codes observed: NORTH, SOUTH, EAST, WEST, CENTRAL
- Most common store count pattern: all stores have exactly 3 orders each (evenly distributed)

## Amount Check

- Orders at or above 100: 2 (O1008 at $120.00 and O1012 at $210.00)
- Why this might matter to an analyst: large orders could need separate approval workflows, fraud checks, or could indicate bulk/wholesale purchases worth investigating for revenue trends.

## Log Profile

- Error line count: 10
- Most common error: "connection timeout to source api" (4 occurrences)
- Last log timestamp: 2026-06-28T06:20:00
- Did the job appear to finish? No it doesn't appear to have finished due to the erros.

## Questions I Would Ask Next

- Data question: Why are all 5 store regions equally represented (3 orders each)? Is this expected, or could some orders be missing due to the pipeline errors?
- Operations question: The source API timed out 4 times over ~20 minutes. Is there a retry limit, and should the pipeline fail fast instead of continuing when the API is unreachable?
- Question for the business stakeholder: Do orders above $100 (like O1008 and O1012) require a different approval or fulfillment process, and should we flag them automatically?
