resource "aws_cloudwatch_event_rule" "scheduler" {
  # timings need changing to 15 min for actual lambda func!!!!!
  name = "lambda_scheduler"
  description = "triggers lambda func every 2 minutes"
  schedule_expression = "rate(2 minutes)"
}

