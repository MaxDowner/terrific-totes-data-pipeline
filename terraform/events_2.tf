resource "aws_cloudwatch_event_rule" "s3_event_rule" {
  name                = "processing_lambda_s3_rule"
  description         = "executes lambda on s3 update"
  event_pattern       = jsonencode({"source": ["aws.s3"],
                        "detail-type": ["Object Created"]})
}



