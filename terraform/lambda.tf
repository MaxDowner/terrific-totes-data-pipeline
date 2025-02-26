data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/util/toy.py"
  output_path      = "${path.module}/../function.zip"
}

resource "aws_cloudwatch_log_group" "ingest_group" {
  name = "/aws/lambda/toy_handler"
}

resource "aws_lambda_function" "toy_handler" {
  filename = data.archive_file.lambda.output_path
  function_name = var.lambda_name
  runtime = var.python_runtime
  role = aws_iam_role.lambda_role.arn
  handler = "toy.lambda_handler"
  timeout =  200 
  #TODO: Connect the layer which is outlined above
  layers = [aws_lambda_layer_version.toy_layer.arn]
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
  function_name = aws_lambda_function.toy_handler.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.scheduler.arn
  source_account = data.aws_caller_identity.current.account_id
}

data "archive_file" "layer" {
  type = "zip"
  output_file_mode = "0666"
  source_dir = "${path.module}/../src/util/"
  output_path = "${path.module}/../layer.zip"
}

resource "aws_lambda_layer_version" "toy_layer" {
  layer_name          = "toy_layer"
  compatible_runtimes = [var.python_runtime]
  s3_key = "toy/layer.zip"
  s3_bucket           = aws_s3_bucket.ingestion_code_bucket.bucket
  depends_on = [data.archive_file.layer, aws_s3_object.layer_code]
}

