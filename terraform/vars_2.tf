variable "processed_data_bucket_prefix" {
  type    = string
  default = "processed-data-"
}

variable "processing_code_bucket_prefix" {
  type    = string
  default = "processing-code-"
}

variable "lambda_2_name" {
  type    = string
  default = "processing_lambda_handler"
}



