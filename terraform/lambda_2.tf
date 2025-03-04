data "archive_file" "lambda_2" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/processing_lambda.py"
  output_path      = "${path.module}/../deployment_files/processing_function.zip"
}

resource "aws_cloudwatch_log_group" "processing_group" {
  name = "/aws/lambda/processing_lambda_handler"
}

resource "aws_lambda_function" "processing_lambda_handler_resource" {
  filename         = data.archive_file.lambda_2.output_path
  function_name    = var.lambda_2_name
  runtime          = var.python_runtime
  role             = aws_iam_role.lambda_2_role.arn
  handler          = "processing_lambda.processing_lambda_handler"
  timeout          = 200
  source_code_hash = data.archive_file.lambda_2.output_base64sha256
  #TODO: layers section??
  layers = [aws_lambda_layer_version.dependencies.arn, aws_lambda_layer_version.util_layer.arn]
  depends_on = [
    aws_iam_role_policy_attachment.lambda_2_cw_policy_attachment,
    aws_cloudwatch_log_group.processing_group,
  ]
  #   logging_config {
  #     log_group = [aws_cloudwatch_log_group.processing_group]
  #     }
}

