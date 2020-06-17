from invoke import task
PROD="prod"
STAGING="staging"
LOCAL="local"

def get_data_server(realm):
    path = None
    if realm == PROD:
        path = ''
    elif realm == STAGING:
        path = ''
    elif realm == LOCAL:
        path = "http://localhost:5000/point/insert"

    return path

@task
def create_new_sim(c, name):
    from dcsim.eplusmodel import EplusExperiment
    eplusmodel = EplusExperiment(name)
    eplusmodel.set_period(start=(1, 1), end=(31, 1))
    eplusmodel.set_a("heating setpoints", str(15))
    eplusmodel.set_a("cooling setpoints", str(18))
    print(f"Starting Simulation {name}")
    a = eplusmodel.run()
    print(f"Ending simulation {name}")


def get_sim_output_path(name):
    return f"{name}/eplusout.csv"

@task
def push_sim_data(c, name, realm, rate):
    from stream_ts_data import CSVLoad, VirtualLoad
    fname = get_sim_output_path(name)
    source = CSVLoad(fname)
    num_requests = source.size
    url = get_data_server(realm)
    load = VirtualLoad(source, url, int(rate), int(num_requests))
    load.run()
