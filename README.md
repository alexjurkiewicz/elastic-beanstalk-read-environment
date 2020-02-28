# Read Elastic Beanstalk Environment Data

A GitHub Action to read data about an AWS Elastic Beanstalk environment.

## Example

```yaml
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-west-2
- id: env_status
  uses: alexjurkiewicz/elastic-beanstalk-read-environment@master
  with:
    application_name: My App
    environment_name: production
- run: |
    ver="${{ steps.env_status.output.version }}"
    Currently deployed version: $ver
    if [[ $ver != ${{ github.sha }} ]] ; then
      echo "Not running the latest code."
      exit 1
    fi
```

## Inputs

You can select the environment to load data about in two ways:

1. Exact `environment_id` match
2. Exact `environment_name` match (optionally with `application_name`)

| Input | Required? | Description |
| --- | --- | --- |
| environment_id | No | Return data on this environment (eg `e-abcd1234yz`). |
| environment_name | No | Return data on environment with this exact name. If you have environments with the name in multiple applications, also specify `application_name`. |
| application_name | No | Restrict `environment_name` matches to this application. |

### Environment Variables

You need to provide AWS credentials via the [`aws-actions/configure-aws-credentials` action](https://github.com/aws-actions/configure-aws-credentials).

## Outputs

| Output | Description |
| --- | --- |
| name | Environment name. |
| id | Environment ID (eg `e-abcd1234yz`). |
| application | Application the environment exists in. |
| version | Currently deployed application version label. |
