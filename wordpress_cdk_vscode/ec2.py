from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class EC2Stack(Construct):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Security group for EC2
        self.sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=vpc,
            description="Allow HTTP and SSH",
            allow_all_outbound=True
        )
        self.sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")
        self.sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        # Launch Template for Nginx/WordPress
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "sudo yum update -y",
            "sudo yum install -y nginx",
            "sudo systemctl enable nginx",
            "sudo systemctl start nginx"
        )
        self.instances = []
        for i in range(2):
            instance = ec2.Instance(
                self, f"WebServer{i+1}",
                instance_type=ec2.InstanceType("t3.micro"),
                machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                vpc=vpc,
                security_group=self.sg,
                user_data=user_data
            )
            self.instances.append(instance)

