
# WordPress Infrastructure on AWS CDK

This project defines a production-ready WordPress infrastructure on AWS using the AWS CDK Python framework. It provisions a scalable, secure multi-tier architecture with:

- **Application Load Balancer** - Distributes incoming traffic across EC2 instances
- **EC2 Web Servers** - Two t3.micro instances running nginx in private subnets
- **PostgreSQL Database** - RDS instance with automated backups, auto-scaling storage, and credentials managed via Secrets Manager
- **VPC with Multi-AZ** - Two availability zones with public/private subnet separation and NAT Gateway for secure outbound traffic

## Testing

This project includes a comprehensive modular test suite with **28 unit tests** organized by infrastructure component:

- **test_network.py** (4 tests) - VPC, subnets, NAT Gateway, Internet Gateway
- **test_ec2.py** (9 tests) - EC2 instances, security groups, IAM roles, nginx configuration
- **test_rds.py** (9 tests) - PostgreSQL database, storage, backups, security, Secrets Manager
- **test_alb.py** (6 tests) - Application Load Balancer, listener, target groups, health checks

**All tests pass successfully.** Run tests with:
```bash
# Run all tests
pytest tests/unit/ -v

# Run tests for a specific component
pytest tests/unit/test_ec2.py -v
pytest tests/unit/test_rds.py -v
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

## AWS Configuration

Before deploying, you need to configure AWS credentials and set your target region.

### Option 1: AWS CLI Configuration (Recommended)

Install the AWS CLI if you haven't already:
```bash
# macOS with Homebrew
brew install awscli

# Or visit https://aws.amazon.com/cli/
```

Configure your AWS credentials:
```bash
aws configure
```

You'll be prompted to enter:
- **AWS Access Key ID** - Get this from AWS IAM Console (Security Credentials)
- **AWS Secret Access Key** - Provided when creating access keys
- **Default region name** - e.g., `us-east-1` (where to deploy resources)
- **Default output format** - Leave blank or use `json`

This creates/updates `~/.aws/credentials` and `~/.aws/config` files.

### Option 2: Environment Variables

Set AWS credentials via environment variables:
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Option 3: IAM Role (for EC2/Lambda)

If running CDK from an AWS EC2 instance or Lambda, attach an IAM role with permissions:
- `ec2:*` (EC2 management)
- `rds:*` (RDS management)
- `elasticloadbalancing:*` (Load Balancer)
- `ec2:*` (VPC/networking)
- `iam:CreateRole`, `iam:PutRolePolicy`, etc. (IAM permissions)

### Verify Configuration

Test your AWS configuration:
```bash
# Check your identity
aws sts get-caller-identity

# Should output:
# {
#     "UserId": "...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

## Deployment

### Prerequisites for Deployment
- AWS credentials configured (see [AWS Configuration](#aws-configuration) section above)
- IAM user/role with permissions for: EC2, RDS, ElasticLoadBalancing, VPC, IAM, Secrets Manager, CloudFormation
- AWS account with appropriate limits (default is usually sufficient)

### Deploy Steps

Before deploying, verify the infrastructure is valid:

```bash
# List all stacks
cdk ls

# Synthesize CloudFormation template
cdk synth

# Preview changes before deploying (no resources created yet)
cdk diff

# Deploy to AWS (creates real resources)
cdk deploy

# When prompted, review the security changes and type 'y' to confirm
```

**Important Notes:**
- The `cdk deploy` command creates real AWS resources in your account and **will incur charges**
- Review the CloudFormation changes displayed by `cdk diff` before deploying
- Start in a development account first to test
- Use `cdk destroy` to clean up resources when done (be cautious - this deletes data)

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
├── test_network.py                 # 4 tests for VPC and networking
├── test_ec2.py                     # 9 tests for EC2 instances
├── test_rds.py                     # 9 tests for RDS database
└── test_alb.py                     # 6 tests for load balancer
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

## Continuous Integration

This repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically runs on every push and pull request:

**Workflow triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Workflow steps:**
1. Sets up Python 3.12 environment
2. Installs project dependencies
3. Runs all 28 unit tests with pytest
4. Verifies CDK template synthesis

All tests must pass before merging to main. Check the **Actions** tab on GitHub to view workflow runs and test results.

## Post-Deployment

After successful deployment, the ALB DNS name will be displayed in the CloudFormation outputs. Use this to access your WordPress infrastructure through the load balancer.

The RDS credentials are automatically generated and stored in AWS Secrets Manager. Retrieve them with:
```bash
aws secretsmanager get-secret-value --secret-id <instance-id>/master
```

## License

This project is licensed under the MIT License.
