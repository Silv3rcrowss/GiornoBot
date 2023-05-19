provider "aws" {
  region = "eu-west-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "discord-bot-vpc"
  }
}

resource "aws_subnet" "main" {
  cidr_block = "10.0.1.0/24"
  vpc_id     = aws_vpc.main.id
  tags = {
    Name = "discord-bot-subnet"
  }
}

resource "aws_security_group" "discord_bot_sg" {
  name        = "discord_bot_sg"
  description = "Security Group for the Discord bot"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "discord-bot-sg"
  }
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  owners = ["amazon"]
}

locals {
  bot_script = file("${path.module}/bot.py")
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro"

  subnet_id              = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.discord_bot_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.bot_profile.name
  user_data              = templatefile("user_data.tpl", { bot_script = local.bot_script })

  tags = {
    Name = "discord-bot"
  }
}


resource "aws_route" "internet_access" {
  route_table_id         = aws_route_table.main.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "discord-bot-igw"
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
}
resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

resource "aws_eip" "app_eip" {
  vpc      = true
  instance = aws_instance.app.id

  tags = {
    Name = "discord-bot-eip"
  }
}

# resource "aws_eip" "nat_gateway_eip" {
#   vpc = true
# }

# resource "aws_nat_gateway" "main" {
#   allocation_id = aws_eip.nat_gateway_eip.id
#   subnet_id     = aws_subnet.main.id
# }



resource "aws_iam_role" "bot_role" {
  name = "discord_bot_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "secrets_manager_policy" {
  name        = "discord_bot_secrets_manager"
  description = "Allow access to Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "secrets_manager_attachment" {
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
  role       = aws_iam_role.bot_role.name
}

resource "aws_iam_instance_profile" "bot_profile" {
  name = "discord_bot_profile"
  role = aws_iam_role.bot_role.name
}

output "public_ip" {
  value = aws_eip.app_eip.public_ip
}
