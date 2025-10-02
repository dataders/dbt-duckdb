from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class DuckDBCatalogRelation:
    """Base catalog relation class for DuckDB catalog integrations"""
    catalog_type: str
    catalog_name: Optional[str]
    table_format: Optional[str]
    file_format: Optional[str]
    external_volume: Optional[str]
    storage_location: Optional[str] = None

    @property
    def ddl_properties(self) -> Dict[str, Any]:
        """Return properties for DDL generation"""
        properties = {}
        
        if self.table_format and self.table_format != "default":
            properties["table_format"] = self.table_format
            
        if self.file_format and self.file_format != "default":
            properties["file_format"] = self.file_format
            
        if self.storage_location:
            properties["location"] = self.storage_location
            
        return properties


@dataclass
class DuckDBIcebergRelation(DuckDBCatalogRelation):
    """Iceberg-specific catalog relation for DuckDB"""
    catalog_config: Optional[Dict[str, Any]] = None
    table_config: Optional[Dict[str, Any]] = None

    @property
    def ddl_properties(self) -> Dict[str, Any]:
        """Return Iceberg-specific properties for DDL generation"""
        properties = super().ddl_properties
        
        # Add Iceberg-specific properties
        if self.catalog_config:
            properties.update(self.catalog_config)
            
        if self.table_config:
            properties.update(self.table_config)
            
        return properties


@dataclass
class DuckDBDeltaRelation(DuckDBCatalogRelation):
    """Delta-specific catalog relation for DuckDB"""
    delta_config: Optional[Dict[str, Any]] = None

    @property
    def ddl_properties(self) -> Dict[str, Any]:
        """Return Delta-specific properties for DDL generation"""
        properties = super().ddl_properties
        
        # Add Delta-specific properties
        if self.delta_config:
            properties.update(self.delta_config)
            
        return properties

