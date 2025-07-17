#!/bin/bash
# Populates EB environment variables in a running environment from AWS Secrets Manager using AWS CLI.

# Usage: ./eb_set_env_from_secrets.sh <eb-env-name> <aws-secret-id>
envname=$1
secretid=$2

if [ -z "$envname" ] || [ -z "$secretid" ]; then
    echo "Usage: $0 <eb-env-name> <aws-secret-id>"
    exit 1
fi

SECRETS=$(aws secretsmanager get-secret-value --secret-id "$secretid" --region $AWS_DEFAULT_REGION | jq -r '.SecretString')
# Example expects keys MONGO_URI, JWT_SECRET

MONGO_URI=$(echo $SECRETS | jq -r '.MONGO_URI')
JWT_SECRET=$(echo $SECRETS | jq -r '.JWT_SECRET')
FLASK_ENV=production

aws elasticbeanstalk update-environment --environment-name "$envname" --option-settings \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=MONGO_URI,Value="$MONGO_URI" \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=JWT_SECRET,Value="$JWT_SECRET" \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=FLASK_ENV,Value="$FLASK_ENV"
