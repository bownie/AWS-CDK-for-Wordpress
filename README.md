
# WordPress Infrastructure on AWS CDK

This project defines a production-ready WordPress infrastructure on AWS using the AWS CDK Python framework. It provisions a scalable, secure multi-tier architecture with:

- **Application Load Balancer** - Distributes incoming traffic across EC2 instances
- **EC2 Web Servers** - Two t3.micro instances running nginx in private subnets
- **PostgreSQL Database** - RDS instance with automated backups, auto-scaling storage, and credentials managed via Secrets Manager
- **VPC with Multi-AZ** - Two availability zones with public/private subnet separation and NAT Gateway for secure outbound traffic

## Testing

This project includes a comprehensive test suite with **28 unit tests** covering all infrastructure components:
- VPC and networking configuration
- EC2 security groups and instance setup
- RDS database configuration and security
- Load balancer setup and targeting
- Resource tagging and integration tests

**All tests pass successfully.** Run tests with:
```bash
python -m pytest tests/unit/test_wordpress_infrastructure.py -v
```

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Setup

### Prerequisites
- Python 3.12+
- Node.js 22.12.0+ (for AWS CDK CLI)
- AWS credentials configured in your environment

### Installation

Create and activate the virtual environment:

```bash
# Create virtualenv
python3 -m venv .venv

# Activate virtualenv (macOS/Linux)
source .venv/bin/activate

# Or on Windows
.venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Deployment

Before deploying, verify the infrastructure is valid:

```bash
# Synthesize CloudFormation template
cdk synth

# Preview changes before deploying
cdk diff

# Deploy to AWS
cdk deploy
```

**Note:** The `cdk deploy` command will create real AWS resources in your account. This may incur charges. Verify resource configurations before deploying.

## Project Structure

```
wordpress_cdk_vscode/
├── app.py                          # CDK app entry point
├── wordpress_cdk_vscode_stack.py   # Main stack orchestration
├── network.py                      # VPC, subnets, NAT Gateway
├── ec2.py                          # EC2 instances and security groups
├── rds.py                          # PostgreSQL RDS instance
├── alb.py                          # Application Load Balancer
tests/unit/
└── test_wordpress_infrastructure.py # 28 comprehensive tests
```

## Useful Commands

```bash
cdk ls           # List all stacks in the app
cdk synth        # Emit the synthesized CloudFormation template
cdk deploy       # Deploy this stack to your AWS account/region
cdk diff         # Compare deployed stack with current state
cdk destroy      # Destroy all AWS resources (CAUTION)

# Testing
pytest tests/unit/ -v                    # Run all tests
pytest tests/unit/ -v -k test_ec2        # Run specific test pattern
python -m unittest discover tests/unit/  # Alternative test runner
```

## Post-Deployment

After successful deployment, the ALB DNS name will be displayed in the CloudFormation outputs. Use this to access your WordPress infrastructure through the load balancer.

The RDS credentials are automatically generated and stored in AWS Secrets Manager. Retrieve them with:
```bash
aws secretsmanager get-secret-value --secret-id <instance-id>/master
```

## License

This project is licensed under the MIT License.
