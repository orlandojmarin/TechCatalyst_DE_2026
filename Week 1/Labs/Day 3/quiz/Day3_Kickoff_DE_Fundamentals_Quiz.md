# Day 3 Kickoff: Data Engineering Fundamentals : Pipeline Warm-Up
# Score 100

## Q1: In one sentence, a data engineer's main job is to…
- [x] Build and maintain systems that move and shape data so others can use it reliably
- [ ] Train deep learning models all day
- [ ] Design the company logo
- [ ] Answer the office Wi-Fi questions
::time=35

## Q2: Your team extracts raw data, dumps it into the warehouse first, and transforms it later inside the warehouse. What pattern is that?
- [ ] ETL : transform before loading
- [x] ELT : load first, transform later
- [ ] FTP : file transfer pirate
- [ ] LTE : load, then email
::time=35

## Q3: A retailer wants a real-time fraud alert the instant a card is swiped. Batch or streaming?
- [x] Streaming : process each event as it happens
- [ ] Batch : wait until midnight and run it all at once
- [ ] Neither : call the customer and ask
- [ ] Both, just to be safe
::time=35

## Q4: Which best describes a data lake compared to a data warehouse?
- [ ] A warehouse stores only images; a lake stores only numbers
- [x] A lake stores raw data in many formats; a warehouse stores cleaned, structured data for analytics
- [ ] They are identical, just different logos
- [ ] A lake is on-prem; a warehouse must be in the cloud
::time=35

## Q5: A CSV with neat rows and columns is an example of what kind of data?
- [x] Structured data
- [ ] Unstructured data
- [ ] Imaginary data
- [ ] Encrypted data
::time=35

## Q6: Your nightly pipeline failed at 3 a.m. and produced half-loaded tables. Which property would have let you safely re-run it without duplicating data?
- [ ] Volatility
- [ ] Verbosity
- [x] Idempotency
- [ ] Invisibility
::time=35

## Q7: Which workload is OLTP (transactional) rather than OLAP (analytical)?
- [x] An app inserting a single new customer order right now
- [ ] Summing total revenue across 5 years for a dashboard
- [ ] Counting unique visitors per region for a report
- [ ] Aggregating average basket size by month
::time=35

## Q8: People say "garbage in, garbage out." In a pipeline, what is the engineer's best defense?
- [ ] Hope the source data is perfect
- [x] Add data quality checks and validation along the way
- [ ] Delete any row that looks suspicious
- [ ] Email the analysts and wish them luck
::time=35

## Q9: What does a schema describe?
- [ ] The color theme of your dashboard
- [x] The structure of the data : its fields, types, and how they're organized
- [ ] How fast the network is
- [ ] The price of cloud storage
::time=35

## Q10: A "data pipeline" is best described as…
- [x] A series of steps that moves data from source to destination, transforming it along the way
- [ ] A single SQL query run once a year
- [ ] A physical pipe under the data center
- [ ] A spreadsheet emailed around the team
::time=35
