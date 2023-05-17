#!/bin/bash
yum update -y
yum install -y python3

# Install required Python packages
pip3 install --upgrade pip
pip3 install aiohttp boto3 discord.py google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests

# Create a directory for the Discord bot
mkdir /opt/discord-bot

# Copy the bot.py script from the local machine to the instance
cat > /opt/discord-bot/bot.py <<"EOT"
${bot_script}
EOT

# Create a systemd service for the Discord bot
cat <<EOF > /etc/systemd/system/discord-bot.service
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/opt/discord-bot
ExecStart=/usr/bin/python3 /opt/discord-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the Discord bot service
systemctl enable discord-bot
systemctl start discord-bot
