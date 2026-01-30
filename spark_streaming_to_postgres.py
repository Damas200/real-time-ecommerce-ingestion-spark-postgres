from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, to_timestamp
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, DoubleType
)

# ======================================
# Spark Session
# ======================================
spark = (
    SparkSession.builder
    .appName("Real-Time E-Commerce Event Ingestion")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ======================================
# Schema (REQUIRED for streaming CSV)
# ======================================
schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("event_type", StringType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("product_name", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("event_timestamp", StringType(), True),
])

# ======================================
# Read CSV Stream
# ======================================
input_path = "data/events"

raw_df = (
    spark.readStream
    .schema(schema)
    .option("header", "true")
    .option("maxFilesPerTrigger", 1)
    .csv(input_path)
)

# ======================================
# Transformations
# ======================================
events_df = (
    raw_df
    .withColumn(
        "event_timestamp",
        to_timestamp(col("event_timestamp"))
    )
    .withColumn(
        "event_hour",
        hour(col("event_timestamp"))
    )
    .filter(
        col("event_type").isin("view", "purchase")
    )
    .filter(
        col("event_timestamp").isNotNull()
    )
)

# ======================================
# PostgreSQL Config
# ======================================
DB_URL = "jdbc:postgresql://localhost:5432/spark_db"

DB_PROPERTIES = {
    "user": "spark_user",
    "password": "spark123",
    "driver": "org.postgresql.Driver"
}

# ======================================
# Write to PostgreSQL
# ======================================
def write_to_postgres(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    (
        batch_df.write
        .mode("append")
        .jdbc(
            url=DB_URL,
            table="user_events",
            properties=DB_PROPERTIES
        )
    )

# ======================================
# Start Streaming
# ======================================
query = (
    events_df.writeStream
    .foreachBatch(write_to_postgres)
    .outputMode("append")
    .option("checkpointLocation", "checkpoints/user_events")
    .start()
)

query.awaitTermination()
