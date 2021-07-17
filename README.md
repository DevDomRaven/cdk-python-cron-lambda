
# CDK Lambda Sample

## Pre-reqs

Make sure you've got awscli and you've configured your credentials.

https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

Edit the .env file and change the unique name to follow what ever you're using the lambda for.

```
UNIQUE_NAME=<Name of lambda>
```

## Install and Deploy

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

or deploy to your account 

```
$ pipenv run cdk bootstrap && pipenv run cdk deploy
```

## Useful commands

 * `pipenv run cdk ls`          list all stacks in the app
 * `pipenv run cdk synth`       emits the synthesized CloudFormation template
 * `pipenv run cdk deploy`      deploy this stack to your default AWS account/region
 * `pipenv run cdk diff`        compare deployed stack with current state
 * `pipenv run cdk docs`        open CDK documentation

Enjoy!
