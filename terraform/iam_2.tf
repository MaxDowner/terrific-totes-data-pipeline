resource "aws_iam_role" "lambda_2_role" {
  name_prefix        = "role-${var.lambda_2_name}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

# Create policy for s3 write - transform/process stage
resource "aws_iam_policy" "s3_processing_write_policy" {
  name_prefix = "s3-policy-${var.lambda_2_name}-write"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}

# Attach above policy
resource "aws_iam_role_policy_attachment" "lambda_2_s3_processing_write_policy_attachment" {
  role       = aws_iam_role.lambda_2_role.name
  policy_arn = aws_iam_policy.s3_processing_write_policy.arn
}

# Create cloudwatch policy for lambda 2
resource "aws_iam_policy" "cw_policy_2" {
  name_prefix = "cw-policy-2-log"
  policy      = data.aws_iam_policy_document.cw_document.json
}

# Attach above policy
resource "aws_iam_role_policy_attachment" "lambda_2_cw_policy_attachment" {
  role       = aws_iam_role.lambda_2_role.name
  policy_arn = aws_iam_policy.cw_policy_2.arn
}





