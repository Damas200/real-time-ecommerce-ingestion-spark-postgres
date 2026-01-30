# System Architecture

## Architecture Diagram (Textual)

+----------------------+
|  Data Generator      |
|  (Python + Faker)    |
+----------+-----------+
           |
           v
+----------------------+
|  CSV Event Directory |
|  data/events/        |
+----------+-----------+
           |
           v
+------------------------------+
| Spark Structured Streaming   |
| - Schema enforcement         |
| - Filtering & enrichment     |
| - Micro-batch processing     |
+----------+-------------------+
           |
           v
+------------------------------+
| PostgreSQL Database          |
| - user_events table          |
| - Indexed for analytics      |
+------------------------------+

## Data Flow Description

1. The **Data Generator** continuously creates fake e-commerce events.
2. Events are written as **CSV files** into the `data/events/` directory.
3. **Spark Structured Streaming** monitors the directory and processes new files.
4. Cleaned and enriched events are written into **PostgreSQL** in real time.

