data "aws_iam_policy_document" "ecs_task_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${local.project}-task-exec"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume.json
}

resource "aws_iam_role_policy_attachment" "task_exec" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_iam_policy_document" "task_exec_secrets_doc" {
  statement {
    sid     = "AllowReadAppSecrets"
    effect  = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
    ]
    resources = [data.aws_secretsmanager_secret.app.arn]
  }
}

resource "aws_iam_role_policy" "task_exec_secrets" {
  name   = "${local.project}-task-exec-secrets"
  role   = aws_iam_role.task_execution.id
  policy = data.aws_iam_policy_document.task_exec_secrets_doc.json
}

resource "aws_iam_role" "task_role" {
  name               = "${local.project}-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume.json
}

data "aws_iam_policy_document" "task_policy_doc" {
  statement {
    actions = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
    resources = [
      aws_s3_bucket.raw.arn,
      "${aws_s3_bucket.raw.arn}/*",
      aws_s3_bucket.parsed.arn,
      "${aws_s3_bucket.parsed.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "task_policy" {
  name   = "${local.project}-task-policy"
  policy = data.aws_iam_policy_document.task_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "task_policy_attach" {
  role       = aws_iam_role.task_role.name
  policy_arn = aws_iam_policy.task_policy.arn
}
