from aws_cdk import aws_rds as rds, aws_ec2 as ec2, Duration
from constructs import Construct

class RDSStack(Construct):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.db = rds.DatabaseInstance(
            self, "WordpressPostgres",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15_4
            ),
            vpc=vpc,
            multi_az=False,
            allocated_storage=20,
            max_allocated_storage=100,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            credentials=rds.Credentials.from_generated_secret("postgres"),
            publicly_accessible=False,
            removal_policy=None,
            backup_retention=Duration.days(7)
        )
