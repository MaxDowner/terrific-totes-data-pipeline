resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../lambda_requirements.txt -t ${path.module}/../layer_dependencies/python"
  }

  triggers = {
    always_run = timestamp()
    # dependencies = filemd5("${path.module}/../lambda_requirements.txt")
  }
}

data "archive_file" "layer_code" {
  type        = "zip"
  output_path = "${path.module}/../packages/layer/layer.zip"
  source_dir  = "${path.module}/../layer_dependencies"
  depends_on = [null_resource.create_dependencies]
}

resource "aws_lambda_layer_version" "dependencies" {
  layer_name = "Dependency"
  s3_bucket  = aws_s3_object.lambda_layer.bucket
  s3_key     = aws_s3_object.lambda_layer.key
  depends_on = [data.archive_file.layer_code, aws_s3_object.lambda_layer]
}

# data "archive_file" "layer" {
#   type = "zip"
#   output_file_mode = "0666"
#   output_path = "${path.module}/../layer.zip"
#   source_dir = "${path.module}/../src/util/"
# }

# resource "aws_lambda_layer_version" "ingestion_lambda_layer_resource" {
#   layer_name          = "ingestion_lambda_layer"
#   compatible_runtimes = [var.python_runtime]
#   s3_key = "ingestion/layer.zip"
#   s3_bucket           = aws_s3_bucket.ingestion_code_bucket.bucket
#   depends_on = [data.archive_file.layer, aws_s3_object.layer_code]
# }

