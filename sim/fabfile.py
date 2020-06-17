def create_new_sim(name):
    eplusmodel = EplusExperiment("heating_cooling_setpoints")
    eplusmodel.set_period(start=(1, 1), end=(31, 12))
    eplusmodel.set_a("heating setpoints", str(15))
    eplusmodel.set_a("cooling setpoints", str(18))
    a = eplusmodel.run()

def push_sim_data(name):
    from stream_ts_data import CSVLoad
    
