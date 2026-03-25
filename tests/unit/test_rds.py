import unittest
from aws_cdk import assertions as assertions_module
from aws_cdk import App

from wordpress_cdk_vscode.wordpress_cdk_vscode_stack import WordpressCdkVscodeStack


class TestRDSStack(unittest.TestCase):
    """Test RDS PostgreSQL database configuration."""

    def setUp(self):
        self.app = App()
        self.stack = WordpressCdkVscodeStack(self.app, "WordpressCdkVscodeStack")
        self.template = assertions_module.Template.from_stack(self.stack)

    def test_rds_instance_created(self):
        """Verify RDS PostgreSQL instance is created."""
        self.template.has_resource_properties(
            "AWS::RDS::DBInstance",
            {
                "Engine": "postgres",
                "EngineVersion": "15.4",
            },
        )

    def test_rds_instance_type(self):
        """Verify RDS instance is db.t2.micro."""
        self.template.has_resource_properties(
            "AWS::RDS::DBInstance",
            {
                "DBInstanceClass": "db.t2.micro",
            },
        )

    def test_rds_not_publicly_accessible(self):
        """Verify RDS is not publicly accessible."""
        self.template.has_resource_properties(
            "AWS::RDS::DBInstance",
            {
                "PubliclyAccessible": False,
            },
        )

    def test_rds_multi_az_disabled(self):
        """Verify RDS Multi-AZ is disabled for dev environment."""
        self.template.has_resource_properties(
            "AWS::RDS::DBInstance",
            {
                "MultiAZ": False,
            },
        )

    def test_rds_storage_allocation(self):
        """Verify RDS has correct storage allocation."""
        self.template.has_resource_properties(
            "AWS::RDS::DBInstance",
            {
                "AllocatedStorage": "20",
                "MaxAllocatedStorage": 100,
            },
        )

    def test_rds_backup_retention(self):
        """Verify RDS has backup retention enabled."""
        self.template.has_resource_properties(
            "AWS::RDS::DBInstance",
            {
                "BackupRetentionPeriod": assertions_module.Match.any_value(),
            },
        )

    def test_rds_credentials_in_secrets_manager(self):
        """Verify RDS credentials are stored in Secrets Manager."""
        self.template.has_resource_properties(
            "AWS::SecretsManager::Secret",
            {
                "GenerateSecretString": assertions_module.Match.object_like(
                    {
                        "SecretStringTemplate": assertions_module.Match.string_like_regexp(
                            ".*postgres.*"
                        )
                    }
                )
            },
        )

    def test_rds_subnet_group_created(self):
        """Verify RDS subnet group is created."""
        self.template.has_resource_properties(
            "AWS::RDS::DBSubnetGroup",
            {
                "DBSubnetGroupDescription": assertions_module.Match.string_like_regexp(
                    ".*Subnet.*"
                )
            },
        )

    def test_rds_security_group_created(self):
        """Verify RDS security group is created."""
        self.template.resource_count_is("AWS::EC2::SecurityGroup", 3)  # EC2 + ALB + RDS


if __name__ == "__main__":
    unittest.main()
