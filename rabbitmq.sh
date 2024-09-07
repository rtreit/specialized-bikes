#!/bin/bash

# Start RabbitMQ server
service rabbitmq-server start

# Wait for RabbitMQ to start
sleep 10

# Create RabbitMQ user and set permissions
rabbitmqctl add_user specialized_celery_user specialized!123
rabbitmqctl set_user_tags celery_user administrator
rabbitmqctl add_vhost myvhost
rabbitmqctl set_permissions -p myvhost celery_user ".*" ".*" ".*"

# Stop RabbitMQ server
service rabbitmq-server stop