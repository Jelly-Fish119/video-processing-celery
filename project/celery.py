from celery import Celery

app = Celery('project',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['project.tasks']
             )

# Optional configuration, see the application user guide.

app.config_from_object('project.celeryconfig')

if __name__ == '__main__':
    app.start()