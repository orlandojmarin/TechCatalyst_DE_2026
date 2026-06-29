# Day 5: Data Architectures and Pipeline Design
# Score 100

## Q1: A stakeholder says, "Tell ops which neighborhoods need more cars at 5pm on weekdays." What should the data engineer define first?
- [ ] The dashboard color palette and chart order
- [x] A data spec before choosing tools
- [ ] The exact compute engine for every future transformation
- [ ] The final SQL query before sources and consumers are confirmed
::time=30

## Q2: Which choice is a non-functional requirement?
- [ ] Ingest monthly TLC Parquet files
- [ ] Join trips to the taxi zone lookup table
- [ ] Publish borough-level metrics to a dashboard
- [x] Safe recovery from failed loads
::time=25

## Q3: In a medallion architecture, why should the bronze layer remain raw and immutable?
- [x] It preserves raw input for rebuilds
- [ ] It makes dashboards faster because raw data is pre-aggregated
- [ ] It removes the need for silver and gold layers
- [ ] It guarantees that source systems never change column names
::time=30

## Q4: A team wants both nightly accuracy and second-level fraud alerts, but they would need to maintain duplicated logic. Which pattern are they describing?
- [ ] Medallion architecture
- [ ] Kappa architecture
- [x] Lambda architecture
- [ ] Reverse ETL
::time=25

## Q5: In Lab B, every arrow in the architecture diagram should be labeled mainly to show...
- [ ] which team member drew that part of the diagram
- [ ] whether the service icon came from GCP or AWS
- [x] what data moves, in what format, and how often
- [ ] how many slides will explain that component
::time=25

## Q6: Which statement best distinguishes orchestration from transformation code?
- [ ] Orchestration replaces the need for data quality checks
- [x] Orchestration schedules tasks, dependencies, retries, and alerts
- [ ] Orchestration cleans records, joins dimensions, and aggregates trips
- [ ] Orchestration stores raw Parquet files in the bronze layer
::time=30

## Q7: A monthly TLC Parquet file has an unexpected column type. Where should the design catch this first?
- [ ] In the BI dashboard after users complain
- [ ] Only after gold aggregates have been published
- [ ] In the final readout, because schema drift is not a pipeline issue
- [x] At a quality or contract gate near the bronze-to-silver boundary
::time=35

## Q8: Which design choice is the best default for Week 1's NYC Taxi pipeline?
- [ ] Stream every historical taxi record as if it arrived live
- [ ] Skip object storage and load only dashboard-ready tables
- [x] Batch plus medallion, unless freshness requires streaming
- [ ] Use graph storage because trip records connect pickup and dropoff locations
::time=35

## Q9: Which question most directly drives the choice between batch and streaming?
- [ ] Which provider has the nicer architecture icon set?
- [ ] Can the diagram fit on one slide?
- [ ] Does the source file use Parquet or CSV?
- [x] How fresh does the consumer need the data to be?
::time=25

## Q10: Which output belongs in the gold or serving layer?
- [ ] Raw TLC files exactly as downloaded
- [ ] Rejected records kept for investigation
- [x] Borough-hour metrics for analysts
- [ ] A temporary staging file with unvalidated columns
::time=25

## Q11: What is Reverse ETL?
- [x] Trusted outputs back into operations
- [ ] Transforming raw files before they enter object storage
- [ ] Replaying an event log from the beginning
- [ ] Copying dashboard screenshots into a design narrative
::time=25

## Q12: During the readout, a reviewer asks, "What would you cut to ship in one week?" What architecture skill are they testing?
- [ ] Whether the team memorized every cloud service name
- [x] Scoping trade-offs against the business goal
- [ ] Whether the diagram uses enough icons
- [ ] Whether the team can avoid writing requirements
::time=30

## Q13: A team copies a cloud reference architecture exactly, even though the taxi use case has different freshness, cost, and PII needs. What is the main problem?
- [x] They copied boxes without adapting to requirements
- [ ] They should have used only AWS references
- [ ] They used a published architecture without checking requirements
- [ ] They mentioned non-functional requirements too early
::time=30

## Q14: Which data spec field is most likely to reveal whether the team has chosen the right row-level meaning?
- [ ] Sources
- [x] Grain
- [ ] Cost drivers
- [ ] Stakeholders
::time=25

## Q15: If a dashboard reads directly from bronze raw files, what is the biggest design concern?
- [ ] Bronze data is usually too polished for analysts
- [ ] Bronze data cannot be stored in object storage
- [ ] Bronze data is always more expensive than gold data for every query
- [x] Raw data can have drift, duplicates, and quality issues
::time=30

## Q16: Which diagram placement best shows PII handling?
- [x] Where sensitive fields are masked, removed, or governed
- [ ] Only in the title or file name of the architecture diagram
- [ ] As a note after the dashboard, once all consumers already have access
- [ ] Hidden in the narrative but not shown on the diagram
::time=30
