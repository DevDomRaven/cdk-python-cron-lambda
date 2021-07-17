from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
import aws_cdk.aws_lambda as lambda_
from aws_cdk.aws_lambda_python import PythonFunction
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import LambdaFunction

class LambdaDeployStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = PythonFunction(self, "MyFunction",
            entry="./lambda_deploy/functions/", # required
            handler="handler", # optional, defaults to 'handler'
            runtime=lambda_.Runtime.PYTHON_3_8
        )
        lambda_target = LambdaFunction(function)

        Rule(self, "ScheduleRule",
            schedule=Schedule.cron(minute="0", hour="1"),
            targets=[lambda_target]
        )