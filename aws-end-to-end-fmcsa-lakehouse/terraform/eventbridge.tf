resource "aws_cloudwatch_event_rule" "monthly_fmcsa_ingestion" {
  name                = "monthly-fmcsa-ingestion"
  schedule_expression = "cron(0 6 15 * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.monthly_fmcsa_ingestion.name
  arn  = aws_lambda_function.fmcsa_ingestion.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fmcsa_ingestion.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monthly_fmcsa_ingestion.arn
}
