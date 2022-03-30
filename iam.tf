resource "aws_iam_role" "this" {
  name = "lambda-image-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "this" {
  name        = "lambda-iam-keys-rotation-policy"
  path        = "/"
  description = "Lambda Policy"

  policy = file("${path.module}/files/lambda-policy.json")
}

resource "aws_iam_policy_attachment" "this" {
  name       = "lambda-iam-keys-rotation"
  roles      = [aws_iam_role.this.name]
  policy_arn = aws_iam_policy.this.arn
}
