resource "aws_cloudwatch_event_rule" "process_event" {
  name                = "process_event"
  description         = "processing event"
  event_pattern = jsonencode({"source": ["aws.s3"],
                         "detail-type": ["Object Created"]})
}

resource "aws_cloudwatch_event_target" "lambda_proc_target" {
  rule = aws_cloudwatch_event_rule.process_event.name
  arn  = aws_lambda_function.processing_lambda_handler_resource.arn
}

resource "aws_cloudwatch_log_metric_filter" "error_2_proc_metric" {
  name           = "ErrorCountProcess"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/processing_lambda_handler"
  depends_on     = [aws_cloudwatch_log_group.processing_group]

  metric_transformation {
    name      = "ErrorCountProcess"
    namespace = "ErrorNamespace"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "metric_2_proc_alarm" {
  alarm_name          = "error_alarm_process"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.error_2_proc_metric.name
  period              = 60
  threshold           = 1
  namespace           = "ErrorNamespace"
  alarm_description   = "This metric monitors process Lambda execution logs for any mention of the word ERROR"
  statistic           = "SampleCount"
  alarm_actions       = [aws_sns_topic.errorsOverTheLimit_processed.arn]
}

resource "aws_sns_topic" "errorsOverTheLimit_processed" {
  name = "ErrorsOverTheLimitProcessed"
}
resource "aws_sns_topic_subscription" "lambda_2_proc_error_email" {
  topic_arn = aws_sns_topic.errorsOverTheLimit_processed.arn
  protocol  = "email"
  endpoint  = var.email
}