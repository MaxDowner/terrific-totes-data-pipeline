data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/util/toy.py"
  output_path      = "${path.module}/../function.zip"
}

resource "aws_lambda_function" "toy_handler" {
  filename = data.archive_file.lambda.output_path
  function_name = "toy"
  runtime = var.python_runtime
  role = aws_iam_role.lambda_role.arn
  handler = "toy.lambda_handler"
  timeout =  30
  #TODO: Connect the layer which is outlined above
}

resource "aws_lambda_permission" "allow_scheduler" {
  statement_id = "AllowExecutionFromCloudWatch"  
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.toy_handler.arn
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.scheduler.arn
  source_account = data.aws_caller_identity.current.account_id
}