## do we need a new trust policy for the second/third lambdas?? 

# data "aws_iam_policy_document" "trust_policy" {
#   statement {
#     effect = "Allow"
#     principals {
#       type        = "Service"
#       identifiers = ["lambda.amazonaws.com"]
#     }
#     actions = ["sts:AssumeRole"]
#   }
# }

## will assume_role_policy refer to all lambdas as a whole or specific ones?

resource "aws_iam_role" "lambda_2_role" {
  name_prefix        = "role-${var.lambda_2_name}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

# data "aws_iam_policy_document" "s3_data_policy_doc" {
#   statement {
#     actions = ["s3:*",
#                 "s3-object-lambda:*"
#     ]
#     resources = ["*"]
#   }
# }

# Create
resource "aws_iam_policy" "s3_processing_write_policy" {
  name_prefix = "s3-policy-${var.lambda_2_name}-write"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_2_s3_processing_write_policy_attachment" {
  role       = aws_iam_role.lambda_2_role.name
  policy_arn = aws_iam_policy.s3_processing_write_policy.arn
}



