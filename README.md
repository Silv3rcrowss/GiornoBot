# GiornoBot - Artificial General Stupidity (AGS pour les intimes)

GiornoBot is a Discord bot that allows users to search for images in a specified Google Drive folder, randomly select a member to bring breakfast, and post a random citation message from a specific channel. This repository provides the bot implementation and Terraform configuration for deploying GiornoBot on an Amazon Web Services (AWS) EC2 instance.

## Features

- Search for images in a specified Google Drive folder by using the `?img` command.
- Randomly select a member with the 'Breakfast' role to bring breakfast by using the `?chocolatine` command.
- Post a random citation message from a specific channel by using the `?oliviades` command.

## Prerequisites

1. Install [Terraform](https://www.terraform.io/downloads.html) on your local machine.
2. Install [AWS CLI](https://aws.amazon.com/cli/) and configure it with your AWS credentials.

## Deployment Steps

1. Clone the GiornoBot repository to your local machine.
2. Navigate to the cloned repository and open the Terraform configuration file (main.tf).
3. Update the Google Drive folder ID and the citation messages channel ID in the bot.py file.
4. Run `terraform init` to initialize the Terraform working directory.
5. Run `terraform apply` to deploy the GiornoBot on an AWS EC2 instance.
6. After the deployment is complete, you'll receive the public IP address of the instance as output.

## Usage

- Invite GiornoBot to your Discord server using the bot's token.
- Use the commands `?img`, `?chocolatine`, and `?oliviades` to interact with the bot.

## Repository Structure

- `bot.py`: The main implementation of the GiornoBot Discord bot.
- `main.tf`: The Terraform configuration file for deploying the bot on an AWS EC2 instance.
- `user_data.tpl`: The user data template file for initializing the EC2 instance with the bot.
- `README.md`: The documentation for the project.
