from aws_cdk import Stack
from constructs import Construct

class WordpressCdkVscodeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        from .network import NetworkStack
        from .ec2 import EC2Stack
        from .rds import RDSStack
        from .alb import ALBStack

        # Create VPC
        network = NetworkStack(self, "NetworkStack")

        # Create EC2 instances
        ec2_stack = EC2Stack(self, "EC2Stack", vpc=network.vpc)

        # Create RDS instance
        RDSStack(self, "RDSStack", vpc=network.vpc)

        # Create ALB
        ALBStack(self, "ALBStack", vpc=network.vpc, instances=ec2_stack.instances)
