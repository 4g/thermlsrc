from fabric import task
from fabric import Connection
from invoke import run as local
@task()
def hello(ctx, name='World'):
    print(f"Hello {name}")
    
@task()
def start_gunicorn(ctx, env='local'):
    pip_install_requirements = 'pip install -r requirements.txt'
    gunicorn_start = 'gunicorn -c gunicorn_config.py wsgi:application'
    if env == 'local':
        local(pip_install_requirements)
        local(gunicorn_start)
    if env == 'prod':
        c = Connection('host')
        c.run(pip_install_requirements)
        c.run(gunicorn_start)