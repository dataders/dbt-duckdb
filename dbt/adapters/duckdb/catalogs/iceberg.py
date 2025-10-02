from typing import Optional, Dict, Any

from dbt.adapters.catalogs import CatalogIntegration, CatalogIntegrationConfig
from dbt.adapters.contracts.relation import RelationConfig

from dbt.adapters.duckdb.catalogs.relations import DuckDBIcebergRelation
from dbt.adapters.duckdb.catalogs.utils import catalog_name, storage_location
from dbt.adapters.duckdb.constants import (
    ICEBERG_CATALOG_TYPE, 
    ICEBERG_TABLE_FORMAT, 
    PARQUET_FILE_FORMAT,
    DuckDBIcebergParameters,
)


class DuckDBIcebergCatalogIntegration(CatalogIntegration):
    """DuckDB Iceberg catalog integration"""
    
    catalog_type = ICEBERG_CATALOG_TYPE
    table_format = ICEBERG_TABLE_FORMAT
    file_format = PARQUET_FILE_FORMAT
    allows_writes = True

    def __init__(self, config: CatalogIntegrationConfig) -> None:
        super().__init__(config)
        # Handle DuckDB-specific Iceberg properties
        self.catalog_config = config.adapter_properties.get(
            DuckDBIcebergParameters.catalog_config, {}
        )
        self.table_config = config.adapter_properties.get(
            DuckDBIcebergParameters.table_config, {}
        )

    def build_relation(self, model: RelationConfig) -> DuckDBIcebergRelation:
        """Build an Iceberg relation object for DuckDB"""
        return DuckDBIcebergRelation(
            catalog_type=self.catalog_type,
            catalog_name=self.catalog_name or "iceberg",
            table_format=self.table_format,
            file_format=self.file_format,
            external_volume=self.external_volume,
            storage_location=self._calculate_storage_location(model),
            catalog_config=self.catalog_config,
            table_config=self._get_table_config(model),
        )

    def _calculate_storage_location(self, model: RelationConfig) -> Optional[str]:
        """Calculate the storage location for the Iceberg table"""
        # Check if model has a specific storage location
        if model.config and model.config.get(DuckDBIcebergParameters.storage_location):
            return model.config[DuckDBIcebergParameters.storage_location]
        
        # Use external volume if available
        if self.external_volume:
            return f"{self.external_volume}/{model.schema}/{model.name}"
            
        # Use adapter properties storage location
        if DuckDBIcebergParameters.storage_location in self.catalog_config:
            base_location = self.catalog_config[DuckDBIcebergParameters.storage_location]
            return f"{base_location}/{model.schema}/{model.name}"
            
        return None

    def _get_table_config(self, model: RelationConfig) -> Dict[str, Any]:
        """Get table-specific configuration for Iceberg"""
        table_config = self.table_config.copy()
        
        # Add model-specific table config if provided
        if model.config and model.config.get(DuckDBIcebergParameters.table_config):
            table_config.update(model.config[DuckDBIcebergParameters.table_config])
            
        return table_config

