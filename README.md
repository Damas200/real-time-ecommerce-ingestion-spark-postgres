
# Real-Time E-Commerce Event Ingestion Pipeline

##  Project Overview

This project implements a **real-time data ingestion pipeline** using **Apache Spark Structured Streaming** and **PostgreSQL**.  
It simulates an e-commerce platform that continuously generates user activity events (such as product views and purchases), processes them in real time, and stores them in a relational database for analytics.

The project was developed as part of **Module Lab 2: Real-Time Data Ingestion Using Spark Structured Streaming & PostgreSQL** and demonstrates practical data engineering skills used in real-world systems.

---

##  Objectives

By completing this project, we achieve the following:

- Simulate continuous streaming data using Python
- Ingest CSV-based streaming data with Spark Structured Streaming
- Perform real-time data transformation and validation
- Persist processed data into PostgreSQL
- Ensure fault tolerance using checkpointing
- Validate correctness and performance of the pipeline

---

##  Tools & Technologies

- **Python 3.12**
- **Apache Spark 3.5.x (Structured Streaming)**
- **PostgreSQL 16**
- **Pandas**
- **Faker**
- **SQL**
- **WSL2 / Linux Environment**

---

## 📂 Project Structure

```text
Real-Time E-Commerce Event Ingestion Pipeline/
│
├── README.md
├── generate_events.py
├── spark_streaming_to_postgres.py
├── postgres_setup.sql
├── postgres_connection_details.txt
├── requirements.txt
├── user_guide.md
├── test_cases.md
│
├── data/
│   └── events/
│
├── checkpoints/
└── venv/
````

---

##  Pipeline Description

### 1️⃣ Data Generation

A Python script (`generate_events.py`) continuously generates fake e-commerce events and writes them as CSV files into a monitored directory.
Each event includes:

* User ID
* Event type (view / purchase)
* Product details
* Price
* Timestamp

Files are written atomically to ensure Spark-safe ingestion.

---

### Spark Structured Streaming

The Spark job (`spark_streaming_to_postgres.py`) performs the following:

* Monitors the CSV directory for new files
* Applies a predefined schema
* Converts timestamps and derives additional columns (e.g., event_hour)
* Filters invalid records
* Writes processed data to PostgreSQL using `foreachBatch`
* Uses checkpointing for fault tolerance

---

### PostgreSQL Storage

Processed events are stored in PostgreSQL:

* Database: `spark_db`
* Table: `user_events`
* Indexed for query performance
* Supports real-time analytics and validation

---

##  Key Features

* Real-time ingestion using Spark Structured Streaming
* Fault tolerance via checkpointing
* Idempotent file-based streaming
* Efficient batch inserts into PostgreSQL
* Production-style directory and configuration setup

---

## Testing & Validation

All system components were manually tested, including:

* CSV generation correctness
* Spark file detection
* Data transformation accuracy
* Database insertion validation
* Fault recovery after restart
* Stability under continuous load

Detailed test cases are documented in **`test_cases.md`**.

---

##  How to Run the Project

Please follow the detailed step-by-step instructions in:

 **`user_guide.md`**


##  Conclusion

This project demonstrates a complete, fault-tolerant, real-time data pipeline using modern data engineering tools.
It reflects industry best practices and provides hands-on experience with streaming systems, data transformation, and database integration.

---
