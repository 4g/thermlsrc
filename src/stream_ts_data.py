import requests
from random import randint
import json
import argparse
import time

class VirtualLoad:
    def __init__(self,
                 url="http://localhost:8000/tsdb_push?",
                 rate=100,
                 num_requests=10000,
                 num_sensors=100,
                 maxval=100.0):
        """
        :param url: URL to which requests are sent
        :param rate: number of requests per second
        :param num_requests: total number of requests
        :param num_sensors: number of sensors in the json
        :param maxval: max sensor value
        """
        self.url = url
        self.rate = rate
        self.num_sensors = num_sensors
        self.maxval = maxval
        self.num_requests = num_requests
        self.state = {"sensor" + str(i) :
                          randint(1, self.maxval) for i in range(self.num_sensors)}

    def push(self):
        state_json = json.dumps(self.state)
        print (state_json)
        requests.post(url=self.url, json=state_json)

    def step(self):
        for i in self.state:
            self.state[i] += (randint(0, self.maxval) - self.maxval//2)/(self.maxval/4 + 0.1)

    def run(self):
        for i in range(self.num_requests):
            self.step()
            self.push()
            time.sleep(1/self.rate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="url", required=True)
    parser.add_argument("-r", help="rate", required=False, default=100, type=int)
    parser.add_argument("-n", help="num_requests", required=False, default=10000, type=int)
    parser.add_argument("-s", help="num_sensors", required=False, default=100, type=int)
    parser.add_argument("-m", help="maxval", required=False, default=100, type=float)

    args = parser.parse_args()
    load = VirtualLoad(url=args.u,
                       rate=args.r,
                       num_requests=args.n,
                       num_sensors=args.s,
                       maxval=args.m)
    load.run()