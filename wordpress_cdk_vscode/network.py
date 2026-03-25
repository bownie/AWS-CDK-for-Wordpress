from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class NetworkStack(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc = ec2.Vpc(
            self, "WordpressVpc",
            max_azs=2,
            nat_gateways=1
        )
