data "archive_file" "lambda_3_load" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/warehouse_lambda.py"
  output_path      = "${path.module}/../deployment_files/loading_function.zip"
}

resource "aws_cloudwatch_log_group" "loading_group" {
  name = "/aws/lambda/loading_lambda_handler"
}

## this lambda uses the same dependencies layer as lambda 1, but a utils_2 layer for its utility functions
resource "aws_lambda_function" "loading_lambda_handler_resource" {
  filename         = data.archive_file.lambda_3_load.output_path
  function_name    = var.lambda_3_name
  runtime          = var.python_runtime
  role             = aws_iam_role.lambda_3_load_role.arn
  handler          = "warehouse_lambda.warehouse_lambda_handler"
  timeout          = 200
  source_code_hash = data.archive_file.lambda_3_load.output_base64sha256
  layers = [aws_lambda_layer_version.dependencies.arn, aws_lambda_layer_version.util_layer.arn, aws_lambda_layer_version.util_layer_2.arn, "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:16", aws_lambda_layer_version.pyarrow_dependencies.arn]
  depends_on = [
    aws_iam_role_policy_attachment.lambda_3_load_cw_policy_attachment,
    aws_cloudwatch_log_group.loading_group,
  ]
}


