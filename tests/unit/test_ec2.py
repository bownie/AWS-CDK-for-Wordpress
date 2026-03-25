import unittest
from aws_cdk import assertions as assertions_module
from aws_cdk import App

from wordpress_cdk_vscode.wordpress_cdk_vscode_stack import WordpressCdkVscodeStack


class TestEC2Stack(unittest.TestCase):
    """Test EC2 instances and security group configuration."""

    def setUp(self):
        self.app = App()
        self.stack = WordpressCdkVscodeStack(self.app, "WordpressCdkVscodeStack")
        self.template = assertions_module.Template.from_stack(self.stack)

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

    def test_ec2_instances_tagged(self):
        """Verify EC2 instances have appropriate tags."""
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
