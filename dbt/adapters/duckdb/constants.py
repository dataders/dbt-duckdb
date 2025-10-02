from types import SimpleNamespace

TEMP_SCHEMA_NAME = "temp_schema_name"
DEFAULT_TEMP_SCHEMA_NAME = "dbt_temp"

# Catalog integration constants
ICEBERG_CATALOG_TYPE = "iceberg"
DELTA_CATALOG_TYPE = "delta"
DEFAULT_CATALOG_TYPE = "default"

# Table format constants
ICEBERG_TABLE_FORMAT = "iceberg"
DELTA_TABLE_FORMAT = "delta"
DEFAULT_TABLE_FORMAT = "default"

# File format constants
PARQUET_FILE_FORMAT = "parquet"
CSV_FILE_FORMAT = "csv"
JSON_FILE_FORMAT = "json"
DEFAULT_FILE_FORMAT = "parquet"

# Default catalog integrations
DEFAULT_DUCKDB_CATALOG = SimpleNamespace(
    name="default",
    catalog_type=DEFAULT_CATALOG_TYPE,
    catalog_name="main",
    table_format=DEFAULT_TABLE_FORMAT,
    external_volume=None,
    file_format=DEFAULT_FILE_FORMAT,
    adapter_properties={},
)

DEFAULT_ICEBERG_CATALOG = SimpleNamespace(
    name="iceberg",
    catalog_type=ICEBERG_CATALOG_TYPE,
    catalog_name="iceberg",
    table_format=ICEBERG_TABLE_FORMAT,
    external_volume=None,
    file_format=PARQUET_FILE_FORMAT,
    adapter_properties={},
)

DEFAULT_DELTA_CATALOG = SimpleNamespace(
    name="delta",
    catalog_type=DELTA_CATALOG_TYPE,
    catalog_name="delta",
    table_format=DELTA_TABLE_FORMAT,
    external_volume=None,
    file_format=PARQUET_FILE_FORMAT,
    adapter_properties={},
)

# DuckDB-specific parameter names for catalog integrations
DuckDBIcebergParameters = SimpleNamespace(
    storage_location="storage_location",
    catalog_config="catalog_config",
    table_config="table_config",
)

DuckDBDeltaParameters = SimpleNamespace(
    storage_location="storage_location",
    delta_config="delta_config",
)
