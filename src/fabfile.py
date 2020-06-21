from fabric import task
from fabric import Connection
from invoke import sudo, run as local

@task()
def hello(ctx, name='World'):
    print(f"Hello {name}")
    
@task()
def start_gunicorn(ctx, env='local'):
    pip_install_requirements = 'pip install -r requirements.txt'
    gunicorn_start = 'gunicorn -c gunicorn_config.py wsgi:application'
    # start_venv = 'source ../venv/bin/activate'
    # import sys
    # if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
    #     local(start_venv)
    if env == 'local':
        local(pip_install_requirements)
        local(gunicorn_start)
    if env == 'prod':
        c = Connection('host')
        c.run(pip_install_requirements)
        c.run(gunicorn_start)
        
@task()
def install_influxdb(ctx):
    check_influx_db_version = "dpkg -l | grep -i influxdb | awk {'print $3'}"
    check_influx_db_version_out = local(check_influx_db_version, hide = 'both')
    if check_influx_db_version_out and check_influx_db_version_out.stdout:
        print(f"InfluxDb version :{check_influx_db_version_out.stdout} "
              f"already exists. So doing nothing")
    else:
        influxdb_version = "influxdb_1.8.0_amd64.deb"
        download_influx_db = "wget https://dl.influxdata.com/influxdb/releases/"+influxdb_version
        local(download_influx_db)
        run_installation = "sudo dpkg -i "+influxdb_version
        sudo(run_installation)
        remove_installation_file = "rm "+influxdb_version
        local(remove_installation_file)
        print (f"Removed the file {influxdb_version}")
    download_influx_db = ''
    