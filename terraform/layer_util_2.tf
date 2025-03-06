## create processing utils resource - declare location of processing util files, and their target location, ready for zipping in the processing lambda

resource "null_resource" "create_utils_2" {
  provisioner "local-exec" {
    command = "cp -r ${path.module}/../src/util_2 -t ${path.module}/../packages_2/python/src \n rm -rf ${path.module}/../packages_2/python/src/util/__pycache__"
  }
  triggers = { always_run = timestamp() }
}

## declare source and output of processing util layer
data "archive_file" "util_2" {
  type        = "zip"
  output_path = "${path.module}/../deployment_files/processing_util_layer.zip"
  source_dir  = "${path.module}/../packages_2/"
  depends_on  = [null_resource.create_utils_2]
}

## info for processing utils layer code in s3 bucket
resource "aws_lambda_layer_version" "util_layer_2" {
  layer_name          = "util_layer_2"
  compatible_runtimes = [var.python_runtime]
  s3_key              = aws_s3_object.utility_layer_2.key
  s3_bucket           = aws_s3_bucket.processing_code_bucket.bucket
  depends_on          = [aws_s3_bucket.processing_code_bucket]
  source_code_hash    = data.archive_file.util_2.output_base64sha256
}
