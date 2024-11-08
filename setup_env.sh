#!/bin/bash

# Prompt user for each environment variable with default values
read -p "Enter SECRET_KEY (default: django-insecure-9gs&uv-7-)7o*^b^nsd5soe#pxvh!6%x1wzr3w#4zt420u+lv8): " SECRET_KEY
SECRET_KEY=${SECRET_KEY:-"django-insecure-9gs&uv-7-)7o*^b^nsd5soe#pxvh!6%x1wzr3w#4zt420u+lv8"}

read -p "Enable DEBUG mode? (True/False, default: True): " DEBUG
DEBUG=${DEBUG:-"True"}

read -p "Enter database name (default: booksDB): " DB_NAME
DB_NAME=${DB_NAME:-"booksDB"}

read -p "Enter database user (default: booksUser): " DB_USER
DB_USER=${DB_USER:-"booksUser"}

read -p "Enter database password (default: hbff$4i3ds2): " DB_PASSWORD
DB_PASSWORD=${DB_PASSWORD:-"hbff$4i3ds2"}

# Write variables to .env file
echo "Writing to .env file..."
cat <<EOL > .env
SECRET_KEY="$SECRET_KEY"
DEBUG=$DEBUG
DB_NAME="$DB_NAME"
DB_USER="$DB_USER"
DB_PASSWORD="$DB_PASSWORD"
EOL

echo ".env file created successfully!"
