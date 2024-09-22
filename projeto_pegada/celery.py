import os
from celery import Celery

# Defina as configurações padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_pegada.settings')

app = Celery('projeto_pegada')

# Leia as configurações de Celery a partir de settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubra automaticamente as tarefas definidas no app
app.autodiscover_tasks()
