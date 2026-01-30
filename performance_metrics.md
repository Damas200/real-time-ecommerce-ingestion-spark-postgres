# Performance Metrics Report

## Overview
This report evaluates the performance of the real-time data ingestion pipeline under local execution.



## Metrics Collected

### 1. Latency
- Definition: Time from CSV creation to database insertion
- Observed Latency: < 1 second
- Measurement Method: Timestamp comparison and Spark logs

### 2. Throughput
- Average Events per File: ~10
- Files per Minute: ~20
- Approximate Throughput: ~200 events/min

### 3. Micro-Batch Processing Time
- Average batch duration: 150–300 ms
- Observed via Spark UI (port 4040)



## Optimizations Applied
- Explicit schema to avoid inference overhead
- `foreachBatch` JDBC writes
- PostgreSQL indexing
- Controlled `maxFilesPerTrigger`



## Conclusion
The pipeline meets real-time processing expectations for a local environment and demonstrates scalable design principles suitable for production systems.
