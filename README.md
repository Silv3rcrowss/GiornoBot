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


--------------------

# User Guide

This Discord bot offers a variety of features that help users perform specific tasks within a Discord server. Here's a guide on how to use the bot and its available commands.

### Available Commands

#### 1. ?img

- **Usage**: `?img <image_name>`

This command searches for a specified image in a Google Drive folder and sends it to the channel. Replace `<image_name>` with the name of the image you want to search for. The bot supports the following image formats: JPG, JPEG, PNG, GIF, BMP, and WEBP.

- **Example**: `?img Tdrycs`

#### 2. ?chocolatine

- **Usage**: `?chocolatine`

This command randomly selects a member with the 'Breakfast' role and posts a message mentioning that they will bring breakfast. No arguments are required for this command.

- **Example**: `?chocolatine`

#### 3. ?oliviades

- **Usage**: `?oliviades`

This command posts a random citation message from a specific channel. No arguments are required for this command. The channel from which the bot will fetch citation messages should be pre-configured in the code.

- **Example**: `?oliviades`

### Using the Commands

To use any of the commands, simply type the command with the appropriate arguments (if any) in a text channel where the bot is present. The bot will process the command and respond accordingly.