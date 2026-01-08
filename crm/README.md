## CRM Celery Report Setup

### Setup Steps

1. Install Redis:
   sudo apt install redis
   # or brew install redis

2. Install Python dependencies:
   pip install -r requirements.txt

3. Run migrations:
   python manage.py migrate

4. Start Redis:
   redis-server

5. Start Celery worker:
   celery -A crm worker -l info

6. Start Celery Beat:
   celery -A crm beat -l info

7. Verify report logs:
   cat /tmp/crm_report_log.txt
