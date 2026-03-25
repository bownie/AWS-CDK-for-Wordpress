import aws_cdk as core
import aws_cdk.assertions as assertions

from wordpress_cdk_vscode.wordpress_cdk_vscode_stack import WordpressCdkVscodeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in wordpress_cdk_vscode/wordpress_cdk_vscode_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WordpressCdkVscodeStack(app, "wordpress-cdk-vscode")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
