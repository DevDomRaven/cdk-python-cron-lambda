
# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

Install pipenv if you've not got it.

```
$ pip3 install pipenv
```

Install dependencies.

```
$ pipenv install
```
At this point you can now synthesize the CloudFormation template for this code.

```
$ pipenv run cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `pipenv run cdk ls`          list all stacks in the app
 * `pipenv run cdk synth`       emits the synthesized CloudFormation template
 * `pipenv run cdk deploy`      deploy this stack to your default AWS account/region
 * `pipenv run cdk diff`        compare deployed stack with current state
 * `pipenv run cdk docs`        open CDK documentation

Enjoy!
