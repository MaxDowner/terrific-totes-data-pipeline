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

resource "aws_cloudwatch_log_metric_filter" "error_metric" {
  name           = "ErrorCount"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/toy_handler"

  metric_transformation {
    name      = "ErrorCount"
    namespace = "ErrorNamespace"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "metric_alarm" {
  alarm_name                = "error_alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 2
  metric_name               = aws_cloudwatch_log_metric_filter.error_metric.name
  period                    = 900
  threshold                 = 1
  namespace = "ErrorNamespace"
  alarm_description         = "This metric monitors Lambda execution logs for any mention of the word ERROR"
  statistic                 = "SampleCount"
  alarm_actions = [aws_sns_topic.errorsOverTheLimit.arn]
}

resource "aws_sns_topic" "errorsOverTheLimit" {
  name = "ErrorsOverTheLimit"
}
resource "aws_sns_topic_subscription" "lambda_error_email" {
  topic_arn = aws_sns_topic.errorsOverTheLimit.arn
  protocol  = "email"
  endpoint  = "terrific.totes.05.coad@gmail.com"
}
