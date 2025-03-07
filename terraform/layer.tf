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


# for Pyarrow layer

resource "null_resource" "pyarrow_create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../pyarrow_requirements.txt -t ${path.module}/../pyarrow_layer_dependencies/python"
  }

  triggers = {
    always_run = timestamp()
  }
}

data "archive_file" "pyarrow_layer_code" {
  type        = "zip"
  output_path = "${path.module}/../deployment_files/pyarrow_dependencies_layer.zip"
  source_dir  = "${path.module}/../pyarrow_layer_dependencies"
  depends_on  = [null_resource.pyarrow_create_dependencies]
}

resource "aws_lambda_layer_version" "pyarrow_dependencies" {
  layer_name       = "PyarrowDependency"
  s3_bucket        = aws_s3_object.pyarrow_code.bucket
  s3_key           = aws_s3_object.pyarrow_code.key
  depends_on       = [data.archive_file.pyarrow_layer_code, aws_s3_object.pyarrow_code]
  source_code_hash = data.archive_file.pyarrow_layer_code.output_base64sha256
}

resource "aws_s3_object" "pyarrow_code" {
  bucket = aws_s3_bucket.ingestion_code_bucket.bucket
  key    = "lambda_pyarrow/function.zip"
  # etag = filemd5(data.archive_file.lambda.output_path) 
  source     = data.archive_file.pyarrow_layer_code.output_path
  depends_on = [data.archive_file.pyarrow_layer_code]
}
