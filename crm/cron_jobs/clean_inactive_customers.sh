#!/bin/bash

# Absolute paths (important for cron)
PROJECT_DIR="/Users/mac/MyFolder/project.py/alx_backend_graphql_crm"
PYTHON="/Users/mac/MyFolder/project.py/venv/bin/python"
LOG_FILE="/tmp/customer_cleanup_log.txt"

cd "$PROJECT_DIR" || exit 1

DELETED_COUNT=$(
$PYTHON manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(order_date__gte=one_year_ago).values_list("customer_id", flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT" >> "$LOG_FILE"
