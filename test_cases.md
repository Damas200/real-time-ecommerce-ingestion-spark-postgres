
## Overview

This document outlines the manual test cases used to validate the **Real-Time E-Commerce Event Ingestion Pipeline** implemented using **Apache Spark Structured Streaming** and **PostgreSQL**.

The objective is to ensure:
- Correct real-time ingestion
- Accurate data transformation
- Reliable fault tolerance
- Stable performance under continuous load


## Test Environment

- **Operating System:** Ubuntu (WSL2)
- **Python Version:** 3.12
- **Apache Spark:** 3.5.x (Local Mode)
- **PostgreSQL:** 16.x
- **Database Name:** `spark_db`
- **Target Table:** `user_events`


## Test Case 1: CSV Event Generation

### Description
Verify that the Python data generator creates valid CSV files containing simulated e-commerce events.

### Steps
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ````

2. Run the data generator:

   ```bash
   python generate_events.py
   ```
3. Observe the `data/events/` directory.

### Expected Outcome

* New CSV files are created continuously.
* Each file contains the following columns:

  * `event_id`
  * `user_id`
  * `event_type`
  * `product_id`
  * `product_name`
  * `price`
  * `event_timestamp`
  * `event_type` values are only `view` or `purchase`.

### Actual Outcome

 As expected



## Test Case 2: Spark Streaming File Detection

### Description

Verify that Spark Structured Streaming detects and processes newly created CSV files.

### Steps

1. Start the Spark streaming job:

   ```bash
   /opt/spark/bin/spark-submit \
     --packages org.postgresql:postgresql:42.7.3 \
     spark_streaming_to_postgres.py
   ```
2. While Spark is running, generate CSV files using `generate_events.py`.

### Expected Outcome

* Spark automatically detects new files.
* Micro-batches are triggered successfully.
* No schema or file access errors occur.

### Actual Outcome

As expected


## Test Case 3: Data Transformation Validation

### Description

Ensure Spark correctly transforms incoming data before writing to PostgreSQL.

### Transformations Verified

* Timestamp parsing (`event_timestamp`)
* Derived column creation (`event_hour`)
* Filtering invalid timestamps
* Filtering valid event types (`view`, `purchase`)

### Steps

1. Allow Spark to process several batches.
2. Query PostgreSQL:

   ```sql
   SELECT event_type, event_hour FROM user_events LIMIT 10;
   ```

### Expected Outcome

* `event_hour` correctly matches the timestamp hour.
* No NULL timestamps.
* Only valid event types exist.

### Actual Outcome

 As expected



## Test Case 4: PostgreSQL Data Insertion

### Description

Verify that streaming data is correctly written to PostgreSQL in real time.

### Steps

1. Connect to PostgreSQL:

   ```bash
   psql -U postgres
   ```
2. Switch to the project database:

   ```sql
   \c spark_db;
   ```
3. Count records:

   ```sql
   SELECT COUNT(*) FROM user_events;
   ```

### Expected Outcome

* Row count increases as new events are processed.
* No duplicate records caused by reprocessing.

### Actual Outcome

 As expected



## Test Case 5: Fault Tolerance and Checkpoint Recovery

### Description

Ensure Spark resumes correctly after failure using checkpointing.

### Steps

1. Stop Spark streaming using `Ctrl + C`.
2. Generate new CSV files while Spark is stopped.
3. Restart Spark streaming.
4. Query PostgreSQL for newly ingested records.

### Expected Outcome

* Spark resumes from the last checkpoint.
* Previously processed files are not reprocessed.
* New files are ingested successfully.

### Actual Outcome

 As expected



## Test Case 6: Performance Under Continuous Load

### Description

Evaluate system stability during continuous data ingestion.

### Steps

1. Run `generate_events.py` continuously for several minutes.
2. Monitor Spark UI at:

   ```
   http://localhost:4040
   ```
3. Observe PostgreSQL insert activity.

### Expected Outcome

* Stable micro-batch execution times.
* No memory or executor failures.
* Continuous database inserts without errors.

### Actual Outcome

 As expected




## Test Summary

All test cases passed successfully.

The system demonstrates:

* Real-time data ingestion
* Accurate transformation
* Reliable fault tolerance
* Stable performance under sustained load



