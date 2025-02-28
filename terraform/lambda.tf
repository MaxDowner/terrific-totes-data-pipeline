data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/ingestion_lambda.py"
  output_path      = "${path.module}/../ingestion_function.zip"
}

resource "aws_cloudwatch_log_group" "ingest_group" {
  name = "/aws/lambda/ingestion_lambda_handler"
}

resource "aws_lambda_function" "ingestion_lambda_handler_resource" {
  filename = data.archive_file.lambda.output_path
  function_name = var.lambda_name
  runtime = var.python_runtime
  role = aws_iam_role.lambda_role.arn
  handler = "ingestion_lambda.ingestion_lambda_handler"
  timeout =  200 
  #TODO: Connect the layer which is outlined above
  layers = [aws_lambda_layer_version.ingestion_lambda_layer_resource.arn]
  depends_on = [
    aws_iam_role_policy_attachment.lambda_cw_policy_attachment,
    aws_cloudwatch_log_group.ingest_group,
  ]
#   logging_config {
#     log_group = [aws_cloudwatch_log_group.ingest_group]
#     }
}
#------------------------------------------

resource "aws_lambda_permission" "allow_scheduler" {
  statement_id = "AllowExecutionFromCloudWatch"  
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingestion_lambda_handler_resource.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.scheduler.arn
  source_account = data.aws_caller_identity.current.account_id
}

