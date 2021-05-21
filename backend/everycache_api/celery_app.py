from everycache_api.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("everycache_api.tasks.example",)
