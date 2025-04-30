broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Worker settings
worker_pool = 'solo'  # Use solo pool for Windows
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1
worker_max_memory_per_child = 250000  # 250MB memory limit

# Task routes
task_routes = {
    'project.tasks.process_video': 'video-processing',
    'project.tasks.extract_frames': 'video-processing'
}

# Task annotations
task_annotations = {
    'project.tasks.process_video': {
        'rate_limit': '1/m'  # Limit to 1 task per minute
    },
    'project.tasks.extract_frames': {
        'rate_limit': '1/m'  # Limit to 1 task per minute
    }
}
