resource "null_resource" "create_utils" {
  provisioner "local-exec" {
    command = "cp -r ${path.module}/../src/util -t ${path.module}/../packages/python/src \n rm -rf ${path.module}/../packages/python/src/util/__pycache__"
  }
  triggers = {always_run = timestamp()}
}


data "archive_file" "util" {
    type = "zip"
    output_path = "${path.module}/../deployment_files/ingestion_util_layer.zip"
    source_dir = "${path.module}/../packages/"
    depends_on = [ null_resource.create_utils ]
}

resource "aws_lambda_layer_version" "util_layer" {
  layer_name          = "util_layer"
  compatible_runtimes = [var.python_runtime]
  s3_key              = aws_s3_object.utility_layer.key
  s3_bucket           = aws_s3_bucket.ingestion_code_bucket.bucket
  depends_on = [aws_s3_bucket.ingestion_code_bucket]
  source_code_hash = filebase64sha256(data.archive_file.util.output_path)
}


