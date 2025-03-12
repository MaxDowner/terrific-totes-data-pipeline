resource "aws_iam_role" "lambda_3_load_role" {
  name_prefix        = "role-${var.lambda_3_name}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

# Create policy for s3 write - transform/process stage
resource "aws_iam_policy" "s3_loading_read_policy" {
  name_prefix = "s3-policy-${var.lambda_3_name}-read"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}

# Attach above policy
resource "aws_iam_role_policy_attachment" "lambda_3_s3_processing_write_policy_attachment" {
  role       = aws_iam_role.lambda_3_load_role.name
  policy_arn = aws_iam_policy.s3_loading_read_policy.arn
}

# Create cloudwatch policy for lambda 2
resource "aws_iam_policy" "cw_policy_3_load" {
  name_prefix = "cw-policy-3-log"
  policy      = data.aws_iam_policy_document.cw_document.json
}

# Attach above policy
resource "aws_iam_role_policy_attachment" "lambda_3_load_cw_policy_attachment" {
  role       = aws_iam_role.lambda_3_load_role.name
  policy_arn = aws_iam_policy.cw_policy_3_load.arn
}

#  Attatch secret manager role
resource "aws_iam_role_policy_attachment" "lambda_load_secrets_policy_attachment" {
  #TODO: attach the secrets policy to the lambda role
  role       = aws_iam_role.lambda_3_load_role.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}



