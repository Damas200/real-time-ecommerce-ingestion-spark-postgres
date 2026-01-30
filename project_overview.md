# Project Overview
## Real-Time Data Ingestion Using Spark Structured Streaming & PostgreSQL

### Objective
This project implements a real-time data pipeline that simulates an e-commerce platform tracking user activity such as product views and purchases. The pipeline continuously ingests generated events, processes them using Apache Spark Structured Streaming, and stores the processed data in a PostgreSQL database.

### System Components
1. **Data Generator**
   - A Python script generates fake e-commerce events as CSV files.
   - Events include user actions (`view`, `purchase`), product information, prices, and timestamps.
   - Files are written continuously to a monitored directory.

2. **Spark Structured Streaming**
   - Spark monitors the CSV directory for newly arriving files.
   - Incoming data is parsed using an explicit schema.
   - Transformations are applied (type casting, filtering, derived columns).
   - Processed data is written to PostgreSQL in micro-batches.

3. **PostgreSQL Database**
   - Acts as the persistent sink for real-time events.
   - Optimized with indexes for analytical queries.
   - Stores clean, structured event data for downstream analysis.

### Data Flow
Events flow from generation → ingestion → processing → storage in near real time, demonstrating a production-style streaming architecture.

### Key Learning Outcomes
- Building a real-time ingestion pipeline
- Using Spark Structured Streaming with file-based sources
- Writing streaming data safely into a relational database
- Understanding fault tolerance and streaming checkpoints
