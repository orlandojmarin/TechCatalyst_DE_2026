# Reading: How to Think About Apache NiFi

Apache NiFi is a visual system for moving and transforming data between systems. It is useful when a team wants to see the route data takes, observe what is waiting, handle different outcomes, reuse connection settings, and trace what happened to an individual piece of data.

NiFi can look complicated because it makes operational decisions visible. A short script can hide connection handling, retries, queues, scheduling, and logging inside code. NiFi gives each concern a place on the canvas or in configuration.

## The Unit of Movement: FlowFile

A FlowFile is NiFi’s unit of work. It contains:

- **content**, the payload bytes, such as CSV text
- **attributes**, small pieces of metadata, such as a filename or S3 object key

The FlowFile is not the same thing as a file stored in S3. A processor may create it empty, fill its content from S3, transform its content, and finally use that content to insert records into a database.

## Processors and Relationships

A processor is the verb of a NiFi flow: one prebuilt, focused action. Examples include fetching an S3 object, parsing records, running a query, writing to a database, or logging attributes. NiFi ships hundreds of them (the processor selector in NiFi 2.10.0 lists about 292), each supplied by an installed extension bundle. You do not write processors; you search for the ones your flow needs, the way you would search a library for a function, and configure them.

After running, a processor routes a FlowFile through a named relationship. Common relationships include:

- `success`, the action completed
- `failure`, the action could not complete
- `retry`, the action might work later

`QueryRecord` also creates a relationship for each query property that you add. In the activity, the property named `clean` creates a relationship named `clean`.

Every relationship must be connected to another component or intentionally auto-terminated. This rule forces the flow designer to decide what happens to every outcome.

## Connections, Queues, and Back Pressure

A connection is both a route and a queue. If a downstream processor stops, incoming FlowFiles wait in the queue instead of disappearing.

Queues make processors independent. They also make congestion visible. In a production flow, back pressure limits how much data a queue may hold. When the limit is reached, NiFi slows the upstream work so one slow destination does not overwhelm the system.

## Controller Services

A processor *does* something to a FlowFile. A controller service does not touch FlowFiles at all. It provides a reusable capability that a processor borrows while it runs. Picture the processors as workers on a line and the controller services as the shared tools and credentials on the wall that any worker can pick up.

Keeping this configuration separate buys three things: several processors can share one tested setup, an operator can update a shared resource (such as a database password) in one place, and an expensive resource (such as a pool of open connections) is built once instead of rebuilt inside every processor.

NiFi has many kinds of controller service. The activity uses four, and each is a different category, not four copies of one thing:

| Category | Reusable responsibility |
|---|---|
| Credentials provider | How the S3 processor authenticates |
| Record reader | How raw CSV bytes become rows with named fields |
| Record writer | How records are turned back into CSV bytes |
| Connection pool | How the database processor connects to Snowflake |

A record reader and a record writer are worth pausing on. On its own, fetched content is just a block of bytes. A record reader parses those bytes into rows and gives each column a name (a schema), so a processor can address a field by name instead of counting commas. A record writer is the mirror image: it serializes the records back into bytes for the next processor. This reader-then-writer pair is why NiFi is format-flexible. The same processor logic works whether the data is CSV, JSON, or Avro, because you change the format by swapping a service, not by rewriting the flow.

## Process Groups and Ports

A Process Group is a container for part of a flow. Teams use groups to reduce visual clutter and create reusable sections.

Input and Output Ports define how FlowFiles enter or leave a Process Group. They do no work on the data. If a Process Group is a room that holds part of a flow, the ports are its labeled doors: an Input Port is where FlowFiles enter and an Output Port is where they leave. The tutorial uses one small flat flow, so it does not need ports.

## Fetching from S3

`FetchS3Object` retrieves one exact object named by its bucket and object key. It does not list or download the whole bucket. If configured with a byte range, it transfers only that range. The activity uses a tested range containing the header and 1,000 complete CSV records.

For many objects, a flow can use `ListS3` to discover keys and then `FetchS3Object` to retrieve them. Large datasets require intentional partitioning, queue limits, and monitoring.

## Observability

NiFi exposes several layers of evidence:

- **processor statistics** show recent counts, bytes, tasks, and time
- **queues** show FlowFiles waiting between components
- **bulletins** show recent warnings and errors
- **provenance** records the history of FlowFile events

Read the processor statistics like a speedometer, not an odometer: they report recent activity inside a rolling window (normally five minutes), not a lifetime total. **In** and **Out** count FlowFiles moving through queues. **Read/Write** measures FlowFile content I/O in NiFi’s Content Repository. **Tasks/Time** reports executions and their combined processing time. These lines measure different things, so a processor can receive one zero-byte FlowFile, download content from S3, and write hundreds of kilobytes, making **In** and **Write** differ.

## Idempotency Is a Design Choice

An operation is idempotent when retrying it produces the same final result instead of adding another copy.

The tutorial flow is intentionally not idempotent. Every trigger fetches the same S3 bytes and performs another set of database inserts. A second run therefore changes the table from 1,000 to 2,000 rows.

Snowflake and Databricks `COPY INTO` normally remember loaded files and skip them on later runs. A production NiFi design must add its own strategy, such as a load-control table, staging plus `MERGE`, or a stable unique key.

## Questions to Carry into the Lab

As you build, keep asking:

1. What is inside the FlowFile at this point?
2. Which processor acts next?
3. Which controller service gives that processor its reusable configuration?
4. Which relationship will the FlowFile follow?
5. Where will it wait if the next processor is stopped?
6. What evidence will prove that the action succeeded?
7. What happens if the same input arrives again?
