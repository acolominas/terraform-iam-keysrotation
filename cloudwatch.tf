resource "aws_cloudwatch_event_rule" "this" {
  schedule_expression = var.lambda_schedule_expression
}

resource "aws_cloudwatch_event_target" "this" {
  rule = aws_cloudwatch_event_rule.this.name
  arn = aws_lambda_function.this.arn
}

resource "aws_lambda_permission" "this" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.this.arn
}
