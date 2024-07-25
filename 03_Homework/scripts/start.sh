#!/bin/bash

PROJECT_NAME=mlops \
  MAGE_CODE_PATH=/home/src \
  SMTP_EMAIL=your_email \
  SMTP_PASSWORD=your_password \
  docker compose up
