resource "aws_cloudwatch_log_metric_filter" "error_3_load_metric" {
  name           = "ErrorCount"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/loading_lambda_handler"
  depends_on     = [aws_cloudwatch_log_group.loading_group]

  metric_transformation {
    name      = "ErrorCount"
    namespace = "ErrorNamespace"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "metric_3_load_alarm" {
  alarm_name          = "error_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.error_3_load_metric.name
  period              = 60
  threshold           = 1
  namespace           = "ErrorNamespace"
  alarm_description   = "This metric monitors loading Lambda execution logs for any mention of the word ERROR"
  statistic           = "SampleCount"
  alarm_actions       = [aws_sns_topic.errorsOverTheLimit_loading.arn]
}

resource "aws_sns_topic" "errorsOverTheLimit_loading" {
  name = "ErrorsOverTheLimitLoading"
}
resource "aws_sns_topic_subscription" "lambda_3_load_error_email" {
  topic_arn = aws_sns_topic.errorsOverTheLimit_loading.arn
  protocol  = "email"
  endpoint  = var.email
}