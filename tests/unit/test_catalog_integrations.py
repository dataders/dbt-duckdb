import unittest
from unittest.mock import Mock
from types import SimpleNamespace

from dbt.adapters.duckdb.catalogs import (
    DuckDBDefaultCatalogIntegration,
    DuckDBIcebergCatalogIntegration,
    DuckDBDeltaCatalogIntegration,
)
from dbt.adapters.duckdb.constants import (
    DEFAULT_CATALOG_TYPE,
    ICEBERG_CATALOG_TYPE,
    DELTA_CATALOG_TYPE,
    DEFAULT_TABLE_FORMAT,
    ICEBERG_TABLE_FORMAT,
    DELTA_TABLE_FORMAT,
    PARQUET_FILE_FORMAT,
)


class TestDuckDBDefaultCatalogIntegration(unittest.TestCase):
    def setUp(self):
        self.config = Mock()
        self.config.name = "test_default_catalog"
        self.config.catalog_type = DEFAULT_CATALOG_TYPE
        self.config.catalog_name = "main"
        self.config.table_format = DEFAULT_TABLE_FORMAT
        self.config.external_volume = None
        self.config.file_format = PARQUET_FILE_FORMAT
        self.config.adapter_properties = {}

    def test_integration_initialization(self):
        """Test default catalog integration initializes correctly"""
        integration = DuckDBDefaultCatalogIntegration(self.config)

        self.assertEqual(integration.name, "test_default_catalog")
        self.assertEqual(integration.catalog_type, DEFAULT_CATALOG_TYPE)
        self.assertEqual(integration.table_format, DEFAULT_TABLE_FORMAT)
        self.assertTrue(integration.allows_writes)

    def test_build_relation(self):
        """Test build_relation method for default catalog"""
        integration = DuckDBDefaultCatalogIntegration(self.config)

        model = Mock()
        model.schema = "test_schema"
        model.name = "test_model"
        model.config = {}

        relation = integration.build_relation(model)

        self.assertEqual(relation.catalog_type, DEFAULT_CATALOG_TYPE)
        self.assertEqual(relation.catalog_name, "main")
        self.assertEqual(relation.table_format, DEFAULT_TABLE_FORMAT)


class TestDuckDBIcebergCatalogIntegration(unittest.TestCase):
    def setUp(self):
        self.config = Mock()
        self.config.name = "test_iceberg_catalog"
        self.config.catalog_type = ICEBERG_CATALOG_TYPE
        self.config.catalog_name = "iceberg"
        self.config.table_format = ICEBERG_TABLE_FORMAT
        self.config.external_volume = "s3://test-bucket/"
        self.config.file_format = PARQUET_FILE_FORMAT
        self.config.adapter_properties = {
            "catalog_config": {"storage_location": "s3://test-bucket/warehouse/"},
            "table_config": {"format_version": "2"}
        }

    def test_integration_initialization(self):
        """Test Iceberg catalog integration initializes correctly"""
        integration = DuckDBIcebergCatalogIntegration(self.config)

        self.assertEqual(integration.name, "test_iceberg_catalog")
        self.assertEqual(integration.catalog_type, ICEBERG_CATALOG_TYPE)
        self.assertEqual(integration.table_format, ICEBERG_TABLE_FORMAT)
        self.assertTrue(integration.allows_writes)
        self.assertEqual(integration.catalog_config["storage_location"], "s3://test-bucket/warehouse/")

    def test_build_relation(self):
        """Test build_relation method for Iceberg catalog"""
        integration = DuckDBIcebergCatalogIntegration(self.config)

        model = Mock()
        model.schema = "test_schema"
        model.name = "test_model"
        model.config = {}

        relation = integration.build_relation(model)

        self.assertEqual(relation.catalog_type, ICEBERG_CATALOG_TYPE)
        self.assertEqual(relation.table_format, ICEBERG_TABLE_FORMAT)
        self.assertIn("s3://test-bucket/", relation.storage_location)

    def test_calculate_storage_location_with_external_volume(self):
        """Test storage location calculation with external volume"""
        integration = DuckDBIcebergCatalogIntegration(self.config)

        model = Mock()
        model.schema = "test_schema"
        model.name = "test_model"
        model.config = {}

        location = integration._calculate_storage_location(model)
        expected = "s3://test-bucket/test_schema/test_model"
        self.assertEqual(location, expected)

    def test_calculate_storage_location_with_model_config(self):
        """Test storage location calculation with model-specific config"""
        integration = DuckDBIcebergCatalogIntegration(self.config)

        model = Mock()
        model.schema = "test_schema"
        model.name = "test_model"
        model.config = {"storage_location": "s3://custom-bucket/custom/path"}

        location = integration._calculate_storage_location(model)
        self.assertEqual(location, "s3://custom-bucket/custom/path")


class TestDuckDBDeltaCatalogIntegration(unittest.TestCase):
    def setUp(self):
        self.config = Mock()
        self.config.name = "test_delta_catalog"
        self.config.catalog_type = DELTA_CATALOG_TYPE
        self.config.catalog_name = "delta"
        self.config.table_format = DELTA_TABLE_FORMAT
        self.config.external_volume = "s3://test-bucket/"
        self.config.file_format = PARQUET_FILE_FORMAT
        self.config.adapter_properties = {
            "delta_config": {"storage_location": "s3://test-bucket/delta/"}
        }

    def test_integration_initialization(self):
        """Test Delta catalog integration initializes correctly"""
        integration = DuckDBDeltaCatalogIntegration(self.config)

        self.assertEqual(integration.name, "test_delta_catalog")
        self.assertEqual(integration.catalog_type, DELTA_CATALOG_TYPE)
        self.assertEqual(integration.table_format, DELTA_TABLE_FORMAT)
        self.assertTrue(integration.allows_writes)

    def test_build_relation(self):
        """Test build_relation method for Delta catalog"""
        integration = DuckDBDeltaCatalogIntegration(self.config)

        model = Mock()
        model.schema = "test_schema"
        model.name = "test_model"
        model.config = {}

        relation = integration.build_relation(model)

        self.assertEqual(relation.catalog_type, DELTA_CATALOG_TYPE)
        self.assertEqual(relation.table_format, DELTA_TABLE_FORMAT)
        self.assertIn("s3://test-bucket/", relation.storage_location)


if __name__ == "__main__":
    unittest.main()

