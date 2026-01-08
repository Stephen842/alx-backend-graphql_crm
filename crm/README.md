## CRM Celery Report Setup

### Requirements
- Redis installed and running
- Python dependencies installed

### Setup Steps
1. Install dependencies:
   pip install -r requirements.txt

2. Run migrations:
   python manage.py migrate

3. Start Redis:
   redis-server

4. Start Celery worker:
   celery -A crm worker -l info

5. Start Celery Beat:
   celery -A crm beat -l info

6. Verify report logs:
   cat /tmp/crm_report_log.txt
