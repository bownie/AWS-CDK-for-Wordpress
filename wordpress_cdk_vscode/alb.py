from aws_cdk import aws_elasticloadbalancingv2 as elbv2, aws_elasticloadbalancingv2_targets as targets
from constructs import Construct

class ALBStack(Construct):
    def __init__(self, scope: Construct, id: str, vpc, instances, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.alb = elbv2.ApplicationLoadBalancer(
            self, "WordpressALB",
            vpc=vpc,
            internet_facing=True
        )
        listener = self.alb.add_listener("Listener", port=80, open=True)
        listener.add_targets(
            "WebTargets",
            port=80,
            targets=[targets.InstanceTarget(instance) for instance in instances]
        )
