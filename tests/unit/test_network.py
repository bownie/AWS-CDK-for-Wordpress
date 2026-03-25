import unittest
from aws_cdk import assertions as assertions_module
from aws_cdk import App

from wordpress_cdk_vscode.wordpress_cdk_vscode_stack import WordpressCdkVscodeStack


class TestNetworkStack(unittest.TestCase):
    """Test VPC and networking infrastructure."""

    def setUp(self):
        self.app = App()
        self.stack = WordpressCdkVscodeStack(self.app, "WordpressCdkVscodeStack")
        self.template = assertions_module.Template.from_stack(self.stack)

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


if __name__ == "__main__":
    unittest.main()
