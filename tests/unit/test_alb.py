import unittest
from aws_cdk import assertions as assertions_module
from aws_cdk import App

from wordpress_cdk_vscode.wordpress_cdk_vscode_stack import WordpressCdkVscodeStack


class TestALBStack(unittest.TestCase):
    """Test Application Load Balancer configuration."""

    def setUp(self):
        self.app = App()
        self.stack = WordpressCdkVscodeStack(self.app, "WordpressCdkVscodeStack")
        self.template = assertions_module.Template.from_stack(self.stack)

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


if __name__ == "__main__":
    unittest.main()
