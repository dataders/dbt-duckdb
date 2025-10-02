# catalog support for DuckDB

## questions

- what's benefit does a dbt-duckdb user get from catalog integrations? most stuff seems stuffed into databases a la Snowflake's catalog-linked databases.

## stuff i've noticed that's "different"

### manual invocations of `ATTACH`

unlike Cloud data warehouses, configs aren't persisted and need to be re-run because they're 

```
INSTALL ducklake;
LOAD ducklake;
ATTACH 'ducklake:metadata.ducklake' AS my_ducklake (DATA_PATH 'data_files');
USE my_ducklake;
```


### Attaching databases from `profiles.yml`

[README's Attaching Additional Databases](./README.md#attaching-additional-databases)


## Docs


- [Iceberg REST](https://duckdb.org/docs/stable/core_extensions/iceberg/iceberg_rest_catalogs.html)
- [Ducklake](https://duckdb.org/docs/stable/core_extensions/ducklake)