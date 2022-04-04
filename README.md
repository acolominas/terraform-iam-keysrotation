# terraform-iam-keysrotation

Lambda triggered every day that rotates IAM keys older than variable days passed.
Only keys that belongs to users passed in variable users are checked. The new ACCESS_KEY and SECRET_KEY are stored in AWS Secrets Manager


### AWS Services Involved

* AWS Lambda
* AWS Cloudwatch
* AWS IAM
* AWS Secrets Manager
