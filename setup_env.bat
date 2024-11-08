@echo off
setlocal

REM Prompt user for each environment variable with default values
set /p SECRET_KEY="Enter SECRET_KEY (default: django-insecure-9gs&uv-7-)7o*^b^nsd5soe#pxvh!6%%x1wzr3w#4zt420u+lv8): "
if "%SECRET_KEY%"=="" set SECRET_KEY=django-insecure-9gs&uv-7-)7o*^b^nsd5soe#pxvh!6%%x1wzr3w#4zt420u+lv8

set /p DEBUG="Enable DEBUG mode? (True/False, default: True): "
if "%DEBUG%"=="" set DEBUG=True

set /p DB_NAME="Enter database name (default: booksDB): "
if "%DB_NAME%"=="" set DB_NAME=booksDB

set /p DB_USER="Enter database user (default: booksUser): "
if "%DB_USER%"=="" set DB_USER=booksUser

set /p DB_PASSWORD="Enter database password (default: hbff$4i3ds2): "
if "%DB_PASSWORD%"=="" set DB_PASSWORD=hbff$4i3ds2

REM Write variables to .env file
echo Writing to .env file...
(
    echo SECRET_KEY="%SECRET_KEY%"
    echo DEBUG=%DEBUG%
    echo DB_NAME="%DB_NAME%"
    echo DB_USER="%DB_USER%"
    echo DB_PASSWORD="%DB_PASSWORD%"
) > .env

echo .env file created successfully!
