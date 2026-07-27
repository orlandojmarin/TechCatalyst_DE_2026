# Week 5 Day 5: Apache NiFi Student Resources

> **AI allowed, review required.** You may use an AI assistant to explain a NiFi message, but verify the answer against the processor configuration and official documentation. Never paste credentials into an AI tool.

Use the activity first. These resources are for understanding a concept more deeply or investigating an error.

## Core Documentation

| Resource | Why it is useful |
|---|---|
| [Apache NiFi Getting Started](https://nifi.apache.org/nifi-docs/getting-started.html) | Introduces the canvas, processors, queues, status indicators, and component statistics |
| [Apache NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html) | Explains FlowFiles, relationships, controller services, ports, provenance, and processor behavior |
| [`FetchS3Object` 2.10.0](https://nifi.apache.org/components/org.apache.nifi.processors.aws.s3.FetchS3Object/) | Defines how NiFi retrieves one named S3 object into FlowFile content |
| [`ListS3` 2.10.0](https://nifi.apache.org/components/org.apache.nifi.processors.aws.s3.ListS3/) | Shows how a flow can discover multiple S3 objects before fetching them |
| [`QueryRecord` 2.10.0](https://nifi.apache.org/components/org.apache.nifi.processors.standard.QueryRecord/) | Explains record readers, record writers, SQL queries, and dynamic relationships |
| [`PutDatabaseRecord` 2.10.0](https://nifi.apache.org/components/org.apache.nifi.processors.standard.PutDatabaseRecord/) | Documents record-based database inserts and its success, retry, and failure routes |
| [Snowflake loading considerations](https://docs.snowflake.com/en/user-guide/data-load-considerations-load) | Explains how Snowflake load metadata helps `COPY INTO` avoid loading the same file again |
| [Snowflake Openflow overview](https://docs.snowflake.com/en/user-guide/data-integration/openflow/about) | Connects the Apache NiFi concepts in this activity to Snowflake’s managed integration service |

## A Compact Mental Model

A **FlowFile** is the unit moving through NiFi. It has:

- content, such as the CSV bytes
- attributes, such as a filename, object key, or record count

A **processor** performs one focused action. A processor routes its result through a named **relationship**, such as `success`, `failure`, or `clean`.

A **connection** links one relationship to another component. It also contains a queue. The queue decouples the two processors, so an upstream processor can finish even if the downstream processor is temporarily stopped.

A **controller service** supplies a reusable capability. It does not move FlowFiles. In this activity:

- an AWS credentials service defines public S3 access
- a CSV reader defines how text becomes records
- a CSV writer defines how records become text
- a database connection pool manages Snowflake JDBC connections

**Input Ports** and **Output Ports** form interfaces around Process Groups. They are useful when a large canvas is divided into reusable sections. This activity uses a flat root canvas, so it does not need ports.

## What the S3 Processor Transfers

`FetchS3Object` retrieves the exact bucket and object key configured on the processor. It does not scan or download every object in the bucket.

In this activity, it transfers only a tested byte range containing the CSV header and 1,000 complete rows. It writes those bytes into the FlowFile content. `QueryRecord`, not `FetchS3Object`, parses and transforms the CSV.

A multi-object flow commonly uses `ListS3` to discover keys and `FetchS3Object` to retrieve each object. Large flows also need back pressure, partitioning, monitoring, and an explicit duplicate-control design.

## Reading a Processor Box

The default `5 min` values describe a rolling reporting window:

| Metric | Meaning |
|---|---|
| **In** | FlowFiles and content bytes pulled from incoming queues |
| **Read/Write** | FlowFile content bytes read from and written to NiFi’s Content Repository |
| **Out** | FlowFiles and content bytes transferred to connected outgoing queues |
| **Tasks/Time** | Processor executions and their combined execution time |

These values measure different things. A processor can receive one zero-byte FlowFile, download data from S3, and write hundreds of kilobytes of new FlowFile content. Its **In** and **Write** values would therefore differ.

## Why the Second Run Creates Duplicates

The tutorial flow retrieves the same object range and performs plain database `INSERT` operations every time the trigger runs. It has no record that the source was already loaded.

Snowflake and Databricks `COPY INTO` are file-loading commands with file-tracking behavior. They normally skip files already recorded as loaded. NiFi can also support an idempotent design, but the flow designer must add it. Common options include:

- a control table keyed by object path, version, or checksum
- staging followed by a key-based `MERGE`
- a unique constraint or another stable business-key check

This distinction is important: an orchestration tool gives you building blocks, while the pipeline design determines the delivery guarantee.

## Lab Deliverable Checklist

| Check | Complete |
|---|:---:|
| NiFi 2.10.0 opens and the four controller services are enabled | ☐ |
| The five processors are valid and connected | ☐ |
| The first run produces 1,000 Snowflake rows | ☐ |
| The second run produces 2,000 Snowflake rows | ☐ |
| The notes explain why the flow is not idempotent | ☐ |
| The notes compare the behavior with `COPY INTO` | ☐ |
| One provenance event is captured and explained | ☐ |
| The notes compare standalone NiFi with Snowflake Openflow | ☐ |
| No credentials appear in the notes or screenshots | ☐ |
| NiFi and the disposable Ubuntu host are stopped | ☐ |
