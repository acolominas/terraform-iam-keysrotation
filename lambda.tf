data "archive_file" "this" {
  type        = "zip"
  source_file = "${path.module}/source/iam-keys-rotation.py"
  output_path = "${path.module}/files/iam-keys-rotation.zip"
}

resource "aws_lambda_function" "this" {
  function_name    = "lambda-iam-keys-rotation"
  description      = "A function to rotate IAM keys"
  handler          = "iam-keys-rotation.lambda_handler"
  runtime          = "python3.9"
  filename         = "${path.module}/files/iam-keys-rotation.zip"
  role             = aws_iam_role.this.arn
  source_code_hash = data.archive_file.this.output_base64sha256


  environment {
    variables = {
      USERS = "drone-prd-ci,drone-stg-ci"
      DAYS  = "90"
    }
  }
}
