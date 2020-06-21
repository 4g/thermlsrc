import requests
import json
import argparse
import time
import pandas as pd

from random import randint
from datetime import datetime
from tqdm import tqdm

class RandomLoad:
    def __init__(self, num_sensors=100, maxval=100.0):
        self.maxval = maxval
        self.num_sensors = num_sensors
        self.state = {"sensor" + str(i):
                          randint(1, self.maxval) for i in
                      range(self.num_sensors)}
    
    def step(self):
        for i in self.state:
            if i != VirtualLoad.TIMESTAMP:
                self.state[i] += (randint(0,
                                          self.maxval) - self.maxval // 2) / (
                                         self.maxval / 4 + 0.1)


class CSVLoad:
    def __init__(self, csv_file):
        self.source = pd.read_csv(csv_file).to_dict(orient='records')
        self.index = 0
        self.step()
    
    def step(self):
        self.state = self.source[self.index]
        self.index += 1


class VirtualLoad:
    TIMESTAMP = "timestamp"
    
    def __init__(self,
        source,
        url="http://localhost:5000/point/insert",
        rate=100,
        num_requests=10000):
        """
        :param url: URL to which requests are sent
        :param rate: number of requests per second
        :param num_requests: total number of requests
        :param num_sensors: number of sensors in the json
        :param maxval: max sensor value
        """
        self.url = url
        self.rate = rate
        self.num_requests = num_requests
        self.state = None
        if source is None:
            source = RandomLoad()
        
        self.source = source
        self.step()
    
    def push(self):
        self.state[VirtualLoad.TIMESTAMP] = str(datetime.now())
        state_json = json.dumps(self.state)
        print(state_json)
        requests.post(url=self.url,
                      json=state_json)
    
    def step(self):
        self.source.step()
        self.state = self.source.state
    
    def run(self):
        for i in tqdm(range(self.num_requests), desc="Sending requests.."):
            self.step()
            self.push()
            time.sleep(1 / self.rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="url", required=True)
    parser.add_argument("-r", help="rate", required=False, default=100,
                        type=int)
    parser.add_argument("-n", help="num_requests", required=False,
                        default=10000, type=int)
    parser.add_argument("-s", help="num_sensors", required=False, default=100,
                        type=int)
    parser.add_argument("-m", help="maxval", required=False, default=100,
                        type=float)
    parser.add_argument("-c", help="csv file to stream", required=False)
    
    args = parser.parse_args()
    if args.c is not None:
        source = CSVLoad(args.c)
    else:
        source = RandomLoad()
    
    load = VirtualLoad(source=source,
                       url=args.u,
                       rate=args.r,
                       num_requests=args.n)
    load.run()
