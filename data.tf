data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "template_file" "lambda-policy" {
  template = file("${path.module}/templates/lambda-policy.json.tpl")

  vars = {
    aws_region = data.aws_caller_identity.current.account_id
    account_id = data.aws_region.current.name
  }
}
