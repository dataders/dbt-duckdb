from typing import Optional

from dbt.adapters.contracts.relation import RelationConfig
from dbt.adapters.catalogs import CATALOG_INTEGRATION_MODEL_CONFIG_NAME

from dbt.adapters.duckdb.constants import (
    DEFAULT_DUCKDB_CATALOG,
    DuckDBIcebergParameters,
    DuckDBDeltaParameters,
)


def catalog_name(model: RelationConfig) -> Optional[str]:
    """Extract catalog name from model configuration"""
    if not hasattr(model, "config") or not model.config:
        return None

    # Check for the standard catalog_name config
    if catalog := model.config.get(CATALOG_INTEGRATION_MODEL_CONFIG_NAME):
        return catalog

    # Handle legacy 'catalog' config key for backward compatibility
    if catalog := model.config.get("catalog"):
        return catalog

    # Default to the default DuckDB catalog
    return DEFAULT_DUCKDB_CATALOG.name


def storage_location(model: RelationConfig) -> Optional[str]:
    """Extract storage location from model configuration"""
    if not hasattr(model, "config") or not model.config:
        return None

    # Check for Iceberg storage location
    if location := model.config.get(DuckDBIcebergParameters.storage_location):
        return location

    # Check for Delta storage location
    if location := model.config.get(DuckDBDeltaParameters.storage_location):
        return location

    # Check for generic storage_location
    if location := model.config.get("storage_location"):
        return location

    return None


def get_catalog_config(model: RelationConfig, config_key: str) -> Optional[dict]:
    """Extract catalog-specific configuration from model"""
    if not hasattr(model, "config") or not model.config:
        return None

    return model.config.get(config_key)

