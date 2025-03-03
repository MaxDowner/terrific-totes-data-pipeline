#-----------------
#Lambda IAM Role
#-----------------
# Define
data "aws_iam_policy_document" "trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# Create
resource "aws_iam_role" "lambda_role" {
  name_prefix        = "role-${var.lambda_name}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

# ------------------------------
# Lambda IAM Policy for S3 Write & Read
# ------------------------------

# Define
# data "aws_iam_policy_document" "s3_data_policy_doc" {
#   statement {
#     actions = ["s3:PutObject",
#       "s3:GetObject",
#       "s3:ListBucket",
#       "s3-object-lambda:*"
#     ]
#     resources = ["${aws_s3_bucket.ingestion_data_bucket.arn}","arn:aws:s3:::totes-s3-logs", "${aws_lambda_function.ingestion_lambda_handler_resource.arn}"]
#   }
# }


data "aws_iam_policy_document" "s3_data_policy_doc" {
  statement {
    actions = ["s3:*",
                "s3-object-lambda:*"
    ]
    resources = ["*"]
  }
}

# Create
resource "aws_iam_policy" "s3_write_policy" {
  name_prefix = "s3-policy-${var.lambda_name}-write"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_s3_write_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}

# ------------------------------
# Lambda IAM Policy for CloudWatch
# ------------------------------

# Define
data "aws_iam_policy_document" "cw_document" {
  statement {
    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]
    # resource subjust to greater specificity
    resources = ["arn:aws:logs:*:*:*"]
  }
}

# Create
resource "aws_iam_policy" "cw_policy" {
  #TODO: use the policy document defined above
  name_prefix = "cw-policy-log"
  policy      = data.aws_iam_policy_document.cw_document.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  #TODO: attach the cw policy to the lambda role
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}

# ------------------------------
# Lambda IAM Policy for Secrets Manager
# ------------------------------

# Define
data "aws_iam_policy_document" "secrets_manager_document" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    # resource subjust to greater specificity
    resources = ["*"]
  }
}

# Create
resource "aws_iam_policy" "secrets_manager_policy" {
  #TODO: use the policy document defined above
  name_prefix = "secrets-policy"
  policy      = data.aws_iam_policy_document.secrets_manager_document.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_secrets_policy_attachment" {
  #TODO: attach the secrets policy to the lambda role
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}
