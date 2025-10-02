import pytest
from dbt.tests.adapter.catalog_integrations.test_catalog_integration import (
    BaseCatalogIntegrationValidation
)
from dbt.tests.util import run_dbt, write_file


# Test models for catalog integration
MODEL_WITH_DEFAULT_CATALOG = """
{{ config(
    materialized='table'
) }}

select 1 as id, 'test' as name
"""

MODEL_WITH_ICEBERG_CATALOG = """
{{ config(
    materialized='table',
    catalog_name='test_iceberg_catalog'
) }}

select 1 as id, 'iceberg_test' as name
"""

MODEL_WITH_DELTA_CATALOG = """
{{ config(
    materialized='table',
    catalog_name='test_delta_catalog'
) }}

select 1 as id, 'delta_test' as name
"""

MODEL_WITH_ICEBERG_STORAGE_CONFIG = """
{{ config(
    materialized='table',
    catalog_name='test_iceberg_catalog',
    storage_location='s3://test-bucket/custom/path/',
    table_config={'format_version': '2'}
) }}

select 1 as id, 'iceberg_custom' as name
"""


class TestDuckDBCatalogIntegration(BaseCatalogIntegrationValidation):
    """Test catalog integration functionality for DuckDB adapter"""

    @pytest.fixture(scope="class")
    def catalogs(self):
        """Define catalog configurations for testing"""
        return {
            "catalogs": [
                {
                    "name": "test_iceberg_catalog",
                    "active_write_integration": "iceberg_integration",
                    "write_integrations": [
                        {
                            "name": "iceberg_integration",
                            "catalog_type": "iceberg",
                            "catalog_name": "iceberg",
                            "table_format": "iceberg",
                            "external_volume": "s3://test-bucket/",
                            "file_format": "parquet",
                            "adapter_properties": {
                                "catalog_config": {
                                    "storage_location": "s3://test-bucket/warehouse/"
                                },
                                "table_config": {
                                    "format_version": "2"
                                }
                            }
                        }
                    ]
                },
                {
                    "name": "test_delta_catalog",
                    "active_write_integration": "delta_integration",
                    "write_integrations": [
                        {
                            "name": "delta_integration",
                            "catalog_type": "delta",
                            "catalog_name": "delta",
                            "table_format": "delta",
                            "external_volume": "s3://test-bucket/",
                            "file_format": "parquet",
                            "adapter_properties": {
                                "delta_config": {
                                    "storage_location": "s3://test-bucket/delta/"
                                }
                            }
                        }
                    ]
                }
            ]
        }

    def test_default_catalog_creates_table(self, project):
        """Test that default catalog integration successfully creates tables"""
        write_file(MODEL_WITH_DEFAULT_CATALOG, project.project_root, "models", "test_default.sql")

        results = run_dbt(["run"])
        assert len(results) == 1
        assert results[0].status == "success"

    def test_iceberg_catalog_integration(self, project):
        """Test Iceberg catalog integration"""
        write_file(MODEL_WITH_ICEBERG_CATALOG, project.project_root, "models", "test_iceberg.sql")

        results = run_dbt(["run"])
        assert len(results) == 1
        assert results[0].status == "success"

    def test_delta_catalog_integration(self, project):
        """Test Delta catalog integration"""
        write_file(MODEL_WITH_DELTA_CATALOG, project.project_root, "models", "test_delta.sql")

        results = run_dbt(["run"])
        assert len(results) == 1
        assert results[0].status == "success"

    def test_iceberg_catalog_with_custom_properties(self, project):
        """Test Iceberg catalog integration with custom properties"""
        write_file(
            MODEL_WITH_ICEBERG_STORAGE_CONFIG, 
            project.project_root, 
            "models", 
            "test_iceberg_custom.sql"
        )

        results = run_dbt(["run"])
        assert len(results) == 1
        assert results[0].status == "success"

    def test_multiple_catalog_models(self, project):
        """Test running models with different catalog configurations"""
        write_file(MODEL_WITH_DEFAULT_CATALOG, project.project_root, "models", "test_default.sql")
        write_file(MODEL_WITH_ICEBERG_CATALOG, project.project_root, "models", "test_iceberg.sql")
        write_file(MODEL_WITH_DELTA_CATALOG, project.project_root, "models", "test_delta.sql")

        results = run_dbt(["run"])
        assert len(results) == 3
        for result in results:
            assert result.status == "success"

