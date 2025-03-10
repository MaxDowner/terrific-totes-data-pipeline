resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../lambda_requirements.txt -t ${path.module}/../layer_dependencies/python"
  }

  triggers = {
    always_run = timestamp()
  }
}

data "archive_file" "layer_code" {
  type        = "zip"
  output_path = "${path.module}/../deployment_files/ingestion_dependencies_layer.zip"
  source_dir  = "${path.module}/../layer_dependencies"
  depends_on  = [null_resource.create_dependencies]
}

resource "aws_lambda_layer_version" "dependencies" {
  layer_name       = "IngestiDependency"
  s3_bucket        = aws_s3_object.lambda_layer.bucket
  s3_key           = aws_s3_object.lambda_layer.key
  depends_on       = [data.archive_file.layer_code, aws_s3_object.lambda_layer]
  source_code_hash = data.archive_file.layer_code.output_base64sha256
}
