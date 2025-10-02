from typing import Optional, Dict, Any

from dbt.adapters.catalogs import CatalogIntegration, CatalogIntegrationConfig
from dbt.adapters.contracts.relation import RelationConfig

from dbt.adapters.duckdb.catalogs.relations import DuckDBDeltaRelation
from dbt.adapters.duckdb.catalogs.utils import catalog_name, storage_location
from dbt.adapters.duckdb.constants import (
    DELTA_CATALOG_TYPE, 
    DELTA_TABLE_FORMAT, 
    PARQUET_FILE_FORMAT,
    DuckDBDeltaParameters,
)


class DuckDBDeltaCatalogIntegration(CatalogIntegration):
    """DuckDB Delta catalog integration"""
    
    catalog_type = DELTA_CATALOG_TYPE
    table_format = DELTA_TABLE_FORMAT
    file_format = PARQUET_FILE_FORMAT
    allows_writes = True

    def __init__(self, config: CatalogIntegrationConfig) -> None:
        super().__init__(config)
        # Handle DuckDB-specific Delta properties
        self.delta_config = config.adapter_properties.get(
            DuckDBDeltaParameters.delta_config, {}
        )

    def build_relation(self, model: RelationConfig) -> DuckDBDeltaRelation:
        """Build a Delta relation object for DuckDB"""
        return DuckDBDeltaRelation(
            catalog_type=self.catalog_type,
            catalog_name=self.catalog_name or "delta",
            table_format=self.table_format,
            file_format=self.file_format,
            external_volume=self.external_volume,
            storage_location=self._calculate_storage_location(model),
            delta_config=self._get_delta_config(model),
        )

    def _calculate_storage_location(self, model: RelationConfig) -> Optional[str]:
        """Calculate the storage location for the Delta table"""
        # Check if model has a specific storage location
        if model.config and model.config.get(DuckDBDeltaParameters.storage_location):
            return model.config[DuckDBDeltaParameters.storage_location]
        
        # Use external volume if available
        if self.external_volume:
            return f"{self.external_volume}/{model.schema}/{model.name}"
            
        # Use adapter properties storage location
        if DuckDBDeltaParameters.storage_location in self.delta_config:
            base_location = self.delta_config[DuckDBDeltaParameters.storage_location]
            return f"{base_location}/{model.schema}/{model.name}"
            
        return None

    def _get_delta_config(self, model: RelationConfig) -> Dict[str, Any]:
        """Get table-specific configuration for Delta"""
        delta_config = self.delta_config.copy()
        
        # Add model-specific delta config if provided
        if model.config and model.config.get(DuckDBDeltaParameters.delta_config):
            delta_config.update(model.config[DuckDBDeltaParameters.delta_config])
            
        return delta_config

