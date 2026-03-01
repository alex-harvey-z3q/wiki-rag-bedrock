resource "aws_db_subnet_group" "db" {
  name       = "${local.project}-dbsubnets"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_security_group" "ecs_tasks" {
  name   = "${local.project}-ecs-sg"
  vpc_id = aws_vpc.this.id

  # Allow ALB -> API tasks on 8000
  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds" {
  name        = "${local.project}-rds-sg"
  description = "RDS access from ECS"
  vpc_id      = aws_vpc.this.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres" {
  identifier              = "${local.project}-pg"
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = "db.t4g.micro"
  allocated_storage       = 20
  db_subnet_group_name    = aws_db_subnet_group.db.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  username                = local.db_username
  password                = local.db_password
  publicly_accessible     = false
  skip_final_snapshot     = true
  deletion_protection     = false
  backup_retention_period = 0
}
