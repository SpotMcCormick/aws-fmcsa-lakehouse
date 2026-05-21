resource "aws_lambda_function" "fmcsa_ingestion" {
  function_name = "fmcsa-ingestion-lambda"

  role = aws_iam_role.lambda_role.arn

  handler = "app.lambda_handler"
  runtime = "python3.12"

  filename         = "../lambda/function.zip"
  source_code_hash = filebase64sha256("../lambda/function.zip")

  timeout     = 60
  memory_size = 512
}
