from typing import Optional

from dbt.adapters.catalogs import CatalogIntegration, CatalogIntegrationConfig
from dbt.adapters.contracts.relation import RelationConfig

from dbt.adapters.duckdb.catalogs.relations import DuckDBCatalogRelation
from dbt.adapters.duckdb.catalogs.utils import catalog_name, storage_location
from dbt.adapters.duckdb.constants import DEFAULT_CATALOG_TYPE, DEFAULT_TABLE_FORMAT, DEFAULT_FILE_FORMAT


class DuckDBDefaultCatalogIntegration(CatalogIntegration):
    """Default DuckDB catalog integration for standard DuckDB tables"""
    
    catalog_type = DEFAULT_CATALOG_TYPE
    table_format = DEFAULT_TABLE_FORMAT
    file_format = DEFAULT_FILE_FORMAT
    allows_writes = True

    def __init__(self, config: CatalogIntegrationConfig) -> None:
        super().__init__(config)

    def build_relation(self, model: RelationConfig) -> DuckDBCatalogRelation:
        """Build a relation object for the default DuckDB catalog"""
        return DuckDBCatalogRelation(
            catalog_type=self.catalog_type,
            catalog_name=self.catalog_name or "main",
            table_format=self.table_format,
            file_format=self.file_format,
            external_volume=self.external_volume,
            storage_location=storage_location(model),
        )

