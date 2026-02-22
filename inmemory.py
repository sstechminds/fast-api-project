import logging

import duckdb
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Info message")

# Connect to an in-memory DuckDB database (default)
# The data will be lost when the program ends
con = duckdb.connect()
# # Connect to a persistent database file (e.g., 'my_data.db')
# # DuckDB will create the file if it doesn't exist
# con = duckdb.connect(database="my_data.db")

# The result can also be fetched as Python objects
results = con.sql("SELECT 42 AS answer").fetchall()
print(results)

# Create a sample Pandas DataFrame
df = pd.DataFrame({'a': [1, 2, 3], 'b': [10, 20, 30]})
# Query the DataFrame directly using SQL.
# DuckDB automatically finds the 'df' variable in the Python scope.
result_df = duckdb.sql("SELECT a, b*2 AS b2 FROM df WHERE a > 1").df()
print(result_df)

# Directly querying a Parquet file hosted online
# Note: For local files, replace the URL with the local file path
query = """
SELECT station_name, count(*) AS num_services
FROM 'https://blobs.duckdb.org/train_services.parquet'
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 3
"""
duckdb.sql(query).show()