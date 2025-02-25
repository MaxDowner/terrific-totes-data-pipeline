resource "aws_cloudwatch_event_rule" "scheduler" {
  # timings need changing to 15 min for actual lambda func!!!!!
  name = "lambda_scheduler"
  description = "triggers lambda func every minute"
  schedule_expression = "rate(1 minute)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
    rule = aws_cloudwatch_event_rule.scheduler.name
    arn = aws_lambda_function.toy_handler.arn
}
