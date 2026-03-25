import unittest
from aws_cdk import assertions as assertions_module
from aws_cdk import aws_ec2 as ec2, aws_rds as rds
from aws_cdk import App, Stack

from wordpress_cdk_vscode.wordpress_cdk_vscode_stack import WordpressCdkVscodeStack


class TestWordpressInfrastructure(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.stack = WordpressCdkVscodeStack(self.app, "WordpressCdkVscodeStack")
        self.template = assertions_module.Template.from_stack(self.stack)

    # ============ VPC & Network Tests ============
    def test_vpc_created(self):
        """Verify VPC is created with correct CIDR block."""
        self.template.has_resource_properties(
            "AWS::EC2::VPC",
            {
                "CidrBlock": "10.0.0.0/16",
                "EnableDnsHostnames": True,
                "EnableDnsSupport": True,
            },
        )

    def test_vpc_has_public_subnets(self):
        """Verify public subnets are created in VPC."""
        self.template.resource_count_is("AWS::EC2::Subnet", 4)  # 2 public + 2 private

    def test_nat_gateway_created(self):
        """Verify NAT Gateway is created for private subnets."""
        self.template.has_resource_properties(
            "AWS::EC2::NatGateway",
            {},
        )

    def test_internet_gateway_created(self):
        """Verify Internet Gateway is attached to VPC."""
        self.template.has_resource_properties(
            "AWS::EC2::InternetGateway",
            {},
        )

    # ============ EC2 Security Group Tests ============
    def test_ec2_security_group_created(self):
        """Verify EC2 security group is created."""
        self.template.has_resource_properties(
            "AWS::EC2::SecurityGroup",
            {
                "GroupDescription": "Allow HTTP and SSH",
            },
        )

    def test_ec2_security_group_allows_http(self):
        """Verify EC2 security group allows HTTP (port 80)."""
        self.template.has_resource_properties(
            "AWS::EC2::SecurityGroup",
            {
                "SecurityGroupIngress": assertions_module.Match.array_with(
                    [
                        assertions_module.Match.object_like(
                            {
                                "FromPort": 80,
                                "ToPort": 80,
                                "IpProtocol": "tcp",
                                "CidrIp": "0.0.0.0/0",
                            }
                        )
                    ]
                )
            },
        )

    def test_ec2_security_group_allows_ssh(self):
        """Verify EC2 security group allows SSH (port 22)."""
        self.template.has_resource_properties(
            "AWS::EC2::SecurityGroup",
            {
                "SecurityGroupIngress": assertions_module.Match.array_with(
                    [
                        assertions_module.Match.object_like(
                            {
                                "FromPort": 22,
                                "ToPort": 22,
                                "IpProtocol": "tcp",
                                "CidrIp": "0.0.0.0/0",
                            }
                        )
                    ]
                )
            },
        )

    # ============ EC2 Instance Tests ============
    def test_ec2_instances_created(self):
        """Verify 2 EC2 instances are created."""
        self.template.resource_count_is("AWS::EC2::Instance", 2)

    def test_ec2_instance_type(self):
        """Verify EC2 instances are t3.micro."""
        self.template.has_resource_properties(
            "AWS::EC2::Instance",
            {
                "InstanceType": "t3.micro",
            },
        )

    def test_ec2_instance_runs_nginx(self):
        """Verify EC2 instances include nginx in user data."""
        self.template.has_resource_properties(
            "AWS::EC2::Instance",
            {
                "UserData": {
                    "Fn::Base64": assertions_module.Match.string_like_regexp(
                        ".*nginx.*"
                    ),
                },
            },
        )

    def test_ec2_instances_in_private_subnets(self):
        """Verify EC2 instances are launched in private subnets."""
        # Instances should not have public IPs
        self.template.has_resource_properties(
            "AWS::EC2::Instance",
            {
                "AssociatePublicIpAddress": assertions_module.Match.absent(),
            },
        )

    def test_ec2_iam_instance_profile_created(self):
        """Verify IAM instance profiles are created for EC2 instances."""
        self.template.resource_count_is("AWS::IAM::InstanceProfile", 2)

    # ============ RDS Tests ============
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

    # ============ Load Balancer Tests ============
    def test_alb_created(self):
        """Verify Application Load Balancer is created."""
        self.template.has_resource_properties(
            "AWS::ElasticLoadBalancingV2::LoadBalancer",
            {
                "Type": "application",
                "Scheme": "internet-facing",
            },
        )

    def test_alb_listener_created(self):
        """Verify ALB listener on port 80 is created."""
        self.template.has_resource_properties(
            "AWS::ElasticLoadBalancingV2::Listener",
            {
                "Port": 80,
                "Protocol": "HTTP",
            },
        )

    def test_alb_target_group_created(self):
        """Verify ALB target group is created."""
        self.template.has_resource_properties(
            "AWS::ElasticLoadBalancingV2::TargetGroup",
            {
                "Port": 80,
                "Protocol": "HTTP",
                "TargetType": "instance",
            },
        )

    def test_alb_targets_are_ec2_instances(self):
        """Verify ALB target group includes EC2 instances."""
        self.template.has_resource_properties(
            "AWS::ElasticLoadBalancingV2::TargetGroup",
            {
                "Targets": assertions_module.Match.array_with(
                    [
                        assertions_module.Match.object_like({"Id": assertions_module.Match.any_value()}),
                        assertions_module.Match.object_like({"Id": assertions_module.Match.any_value()}),
                    ]
                )
            },
        )

    def test_alb_security_group_created(self):
        """Verify ALB security group is created."""
        self.template.has_resource_properties(
            "AWS::EC2::SecurityGroup",
            {
                "GroupDescription": assertions_module.Match.string_like_regexp(
                    ".*ELB.*"
                ),
            },
        )

    def test_alb_security_group_allows_http(self):
        """Verify ALB security group allows HTTP (port 80)."""
        self.template.has_resource_properties(
            "AWS::EC2::SecurityGroup",
            {
                "SecurityGroupIngress": assertions_module.Match.array_with(
                    [
                        assertions_module.Match.object_like(
                            {
                                "FromPort": 80,
                                "ToPort": 80,
                                "IpProtocol": "tcp",
                            }
                        )
                    ]
                )
            },
        )

    # ============ Integration Tests ============
    def test_all_resources_tagged(self):
        """Verify resources have appropriate tags."""
        self.template.has_resource_properties(
            "AWS::EC2::Instance",
            {
                "Tags": assertions_module.Match.array_with(
                    [
                        assertions_module.Match.object_like(
                            {
                                "Key": "Name",
                                "Value": assertions_module.Match.string_like_regexp(
                                    ".*WebServer.*"
                                ),
                            }
                        )
                    ]
                )
            },
        )


if __name__ == "__main__":
    unittest.main()
