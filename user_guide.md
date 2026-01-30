
# User Guide

## Real-Time Data Ingestion Using Spark Structured Streaming & PostgreSQL


## 1. Overview

This guide explains how to run the **Real-Time E-Commerce Event Ingestion Pipeline**.
The system simulates user activity on an e-commerce platform, streams event data using **Apache Spark Structured Streaming**, and stores processed events in **PostgreSQL** in real time.

The pipeline consists of:

1. A **data generator** that continuously produces CSV event files
2. A **Spark Structured Streaming job** that reads and processes those files
3. A **PostgreSQL database** that stores the processed data

---

## 2. Prerequisites

Ensure the following are installed on your system:

* Ubuntu / WSL2 (recommended)
* Python **3.12+**
* Apache Spark **3.5+**
* Java **11**
* PostgreSQL **16**
* Git (optional)

Verify installations:

```bash
python3 --version
java -version
/opt/spark/bin/spark-submit --version
psql --version
```

---

## 3. Project Structure

Ensure your project directory looks like this:

```text
Real-Time E-Commerce Event Ingestion Pipeline/
│
├── generate_events.py
│   └── Python script that continuously generates fake e-commerce events
│       as CSV files (views & purchases).
│
├── spark_streaming_to_postgres.py
│   └── Spark Structured Streaming job that reads CSV files in real time,
│       processes them, and writes data into PostgreSQL.
│
├── postgres_setup.sql
│   └── SQL script to create the database, user, table, and indexes.
│
├── postgres_connection_details.txt
│   └── Database connection configuration (host, port, user, password).
│
├── requirements.txt
│   └── Python dependencies for the data generator (pandas, faker).
│
├── user_guide.md
│   └── Step-by-step instructions on how to run and verify the project.
│
├── project_overview.md
│   └── High-level explanation of the system architecture, components,
│       and data flow.
│
├── test_cases.md
│   └── Manual test plan with test scenarios, steps, expected and actual results.
│
├── performance_metrics.md
│   └── Performance analysis including latency, throughput, batch time,
│       and Spark UI observations.
│
├── system_architecture.png
│   └── Diagram showing data flow:
│       Data Generator → CSV Folder → Spark Streaming → PostgreSQL
│
├── data/
│   └── events/
│       └── Streaming input directory where CSV event files are generated
│           in real time.
│
├── checkpoints/
│   └── Spark Structured Streaming checkpoint directory used for
│       fault tolerance and recovery.
│
├── venv/
│   └── Python virtual environment used by the data generator.
│
└── README.md
    └── (Optional but recommended) Short summary and project entry point.

```


## 4. PostgreSQL Setup

### 4.1 Start PostgreSQL

```bash
sudo service postgresql start
```

Check status:

```bash
sudo service postgresql status
```

### 4.2 Create Database and Table

Log into PostgreSQL:

```bash
sudo -u postgres psql
```

Run the setup script:

```sql
\i postgres_setup.sql
```

Verify database:

```sql
\c spark_db;
\d user_events;
```

Exit PostgreSQL:

```sql
\q
```


## 5. Python Environment Setup (Required for Data Generator)

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

## 6. Running the Pipeline

The pipeline requires **two terminals running simultaneously**.

---

### 6.1 Terminal 1 – Start Spark Streaming Job

From the project root directory:

```bash
/opt/spark/bin/spark-submit \
  --packages org.postgresql:postgresql:42.7.3 \
  spark_streaming_to_postgres.py
```

Expected behavior:

* Spark starts successfully
* Spark UI available at:
  **[http://localhost:4040](http://localhost:4040)**
* Streaming job waits for incoming CSV files

⚠️ **Do not stop this process while testing**

---

### 6.2 Terminal 2 – Start Data Generator

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the data generator:

```bash
python generate_events.py
```

Expected output:

```text
Event generator started...
Written file: data/events/events_XXXXXXXX.csv
Written file: data/events/events_XXXXXXXX.csv
...
```

New CSV files will appear every few seconds in:

```text
data/events/
```

## 7. Verify Data in PostgreSQL

Log into PostgreSQL:

```bash
psql -U spark_user -d spark_db
```

Check inserted records:

```sql
SELECT COUNT(*) FROM user_events;
```

View recent events:

```sql
SELECT * 
FROM user_events
ORDER BY event_timestamp DESC
LIMIT 10;
```

If rows are returned, the pipeline is working correctly ✅

Exit:

```sql
\q
```

---

## 8. Stopping the Pipeline

1. Stop the data generator:

   * Press **CTRL + C** in Terminal 2

2. Stop the Spark streaming job:

   * Press **CTRL + C** in Terminal 1

Spark will safely shut down using checkpoint recovery.

---

## 9. Troubleshooting

### Spark does not process new files

* Ensure CSV files are **newly created**
* Spark Structured Streaming does not reprocess existing files

### PostgreSQL connection error

* Verify credentials in `spark_streaming_to_postgres.py`
* Ensure PostgreSQL is running
* Check port `5432` is open

### Python module not found

* Ensure virtual environment is activated
* Reinstall dependencies:

```bash
pip install -r requirements.txt
```

## 10. Notes & Best Practices

* Spark checkpointing ensures **fault tolerance**
* CSV files act as a simulation of streaming ingestion
* `foreachBatch` enables efficient JDBC writes
* In production, credentials should be stored as environment variables


## 11. Conclusion

You have successfully run a **real-time data ingestion pipeline** using:

* Python for data simulation
* Apache Spark Structured Streaming for real-time processing
* PostgreSQL for persistent storage

This project demonstrates core concepts used in real-world data engineering systems.




