#!/bin/bash
set -e

# Enable RabbitMQ management plugin
rabbitmq-plugins enable rabbitmq_management

# Start RabbitMQ server in the background
rabbitmq-server start
sleep 20

# Configure RabbitMQ
rabbitmqctl add_user specialized_celery_user specialized!123
rabbitmqctl set_user_tags specialized_celery_user administrator
rabbitmqctl add_vhost myvhost
rabbitmqctl set_permissions -p myvhost specialized_celery_user '.*' '.*' '.*'

# Restart RabbitMQ server
rabbitmqctl stop
rabbitmq-server -detached

# Execute the command passed as arguments
exec "$@"