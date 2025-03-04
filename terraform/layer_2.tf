## will we need a different requirements file for lambda 2? thinking not?

#-------------

# resource "null_resource" "create_dependencies" {
#   provisioner "local-exec" {
#     command = "pip install -r ${path.module}/../lambda_requirements.txt -t ${path.module}/../layer_dependencies/python"
#   }

#   triggers = {
#     always_run = timestamp()
#   }
# }

data "archive_file" "lambda_2_layer_code" {
  type        = "zip"
  output_path = "${path.module}/../deployment_files/processing_dependencies_layer.zip"
  source_dir  = "${path.module}/../layer_dependencies"
  depends_on  = [null_resource.create_dependencies]
}

resource "aws_lambda_layer_version" "dependencies" {
  layer_name       = "ProcessingDependency"
  s3_bucket        = aws_s3_object.lambda_2_layer.bucket
  s3_key           = aws_s3_object.lambda_2_layer.key
  depends_on       = [data.archive_file.lambda_2_layer_code, aws_s3_object.lambda_2_layer]
  source_code_hash = data.archive_file.lambda_2_layer_code.output_base64sha256
}