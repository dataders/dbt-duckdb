# DuckDB Catalog Integration Support

This document describes how to use catalog integrations with the dbt-duckdb adapter.

## Overview

The dbt-duckdb adapter now supports catalog integrations, allowing you to materialize dbt models into external catalogs that operate with different table formats like Iceberg and Delta. This provides a warehouse-agnostic interface for managing datasets in object storage.

## Supported Catalog Types

### 1. Default DuckDB Catalog (`default`)
- **Table Format**: `default`
- **File Format**: `parquet`
- **Use Case**: Standard DuckDB tables

### 2. Iceberg Catalog (`iceberg`)
- **Table Format**: `iceberg`
- **File Format**: `parquet`
- **Use Case**: Apache Iceberg tables with DuckDB's Iceberg extension

### 3. Delta Catalog (`delta`)
- **Table Format**: `delta`
- **File Format**: `parquet`
- **Use Case**: Delta Lake tables with DuckDB's Delta extension

## Configuration

### 1. Create `catalogs.yml`

Create a `catalogs.yml` file in your dbt project root:

```yaml
catalogs:
  # Iceberg catalog configuration
  - name: my_iceberg_catalog
    active_write_integration: iceberg_integration
    write_integrations:
      - name: iceberg_integration
        catalog_type: iceberg
        catalog_name: iceberg_catalog
        table_format: iceberg
        external_volume: s3://my-bucket/warehouse/
        file_format: parquet
        adapter_properties:
          catalog_config:
            storage_location: s3://my-bucket/iceberg/
          table_config:
            format_version: "2"

  # Delta catalog configuration
  - name: my_delta_catalog
    active_write_integration: delta_integration
    write_integrations:
      - name: delta_integration
        catalog_type: delta
        catalog_name: delta_catalog
        table_format: delta
        external_volume: s3://my-bucket/warehouse/
        file_format: parquet
        adapter_properties:
          delta_config:
            storage_location: s3://my-bucket/delta/
```

### 2. Configure Models

Reference catalogs in your model configurations:

#### Iceberg Table
```sql
{{
  config(
    materialized='table',
    catalog_name='my_iceberg_catalog'
  )
}}

select * from my_source_table
```

#### Delta Table
```sql
{{
  config(
    materialized='table',
    catalog_name='my_delta_catalog'
  )
}}

select * from my_source_table
```

#### Model with Custom Storage Location
```sql
{{
  config(
    materialized='table',
    catalog_name='my_iceberg_catalog',
    storage_location='s3://my-bucket/custom/path/',
    table_config={'format_version': '2'}
  )
}}

select * from my_source_table
```

## Adapter Properties

### Iceberg Catalog Properties

- **`catalog_config`**: Configuration for the Iceberg catalog
  - `storage_location`: Base storage location for Iceberg tables
- **`table_config`**: Table-specific Iceberg configuration
  - `format_version`: Iceberg table format version

### Delta Catalog Properties

- **`delta_config`**: Configuration for the Delta catalog
  - `storage_location`: Base storage location for Delta tables

## Model Configuration Options

### Storage Location

You can specify storage locations at different levels:

1. **Model Level**: `storage_location` in model config (highest priority)
2. **External Volume**: `external_volume` in catalog configuration
3. **Adapter Properties**: `storage_location` in adapter properties (lowest priority)

### Table Configuration

For Iceberg tables, you can specify table-specific configuration:

```sql
{{
  config(
    materialized='table',
    catalog_name='my_iceberg_catalog',
    table_config={
      'format_version': '2',
      'write_order': 'sorted'
    }
  )
}}
```

## Prerequisites

### Iceberg Support
To use Iceberg catalogs, ensure you have:
1. DuckDB with Iceberg extension installed
2. Proper S3/cloud storage credentials configured
3. Iceberg catalog service (if using REST catalog)

### Delta Support
To use Delta catalogs, ensure you have:
1. DuckDB with Delta extension installed
2. Proper S3/cloud storage credentials configured

## Examples

### Basic Iceberg Setup

```yaml
# catalogs.yml
catalogs:
  - name: iceberg_prod
    active_write_integration: iceberg_rest
    write_integrations:
      - name: iceberg_rest
        catalog_type: iceberg
        catalog_name: production
        table_format: iceberg
        external_volume: s3://prod-data-lake/
        adapter_properties:
          catalog_config:
            storage_location: s3://prod-data-lake/iceberg/
```

```sql
-- models/my_iceberg_table.sql
{{
  config(
    materialized='table',
    catalog_name='iceberg_prod'
  )
}}

select 
  id,
  name,
  created_at
from {{ ref('raw_data') }}
```

### Multi-Catalog Project

```yaml
# catalogs.yml
catalogs:
  - name: bronze_iceberg
    active_write_integration: bronze_integration
    write_integrations:
      - name: bronze_integration
        catalog_type: iceberg
        catalog_name: bronze
        table_format: iceberg
        external_volume: s3://datalake/bronze/

  - name: silver_delta
    active_write_integration: silver_integration
    write_integrations:
      - name: silver_integration
        catalog_type: delta
        catalog_name: silver
        table_format: delta
        external_volume: s3://datalake/silver/

  - name: gold_iceberg
    active_write_integration: gold_integration
    write_integrations:
      - name: gold_integration
        catalog_type: iceberg
        catalog_name: gold
        table_format: iceberg
        external_volume: s3://datalake/gold/
```

This setup allows you to create a medallion architecture with different table formats at each layer.

## Troubleshooting

### Common Issues

1. **Missing Extensions**: Ensure DuckDB has the required extensions (iceberg, delta) installed
2. **Storage Permissions**: Verify S3/cloud storage credentials and permissions
3. **Catalog Configuration**: Check that catalog services are properly configured and accessible

### Debug Mode

Enable debug logging to see catalog integration details:

```bash
dbt run --debug
```

This will show how catalog configurations are being processed and applied to your models.

