#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib.request
import csv
import collections

    
class Queue:
    def __init__(self):
        self.items = []
    def is_empty(self): 
        return self.items == []
    def enqueue(self, item): 
        self.items.insert(0,item)
    def dequeue(self): 
        return self.items.pop()
    def size(self): 
        return len(self.items)

class Server():
    def __init__(self):
        self.currentRequest = None
        self.currenttime = 0
        self.timeRemaining = 0
    def tick(self):
        if self.currentRequest != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentRequest = None
    def busy(self):
        if self.currentRequest != None:
            return True
        else:
            return False
    def startNext(self,newRequest):
        self.currentRequest = newRequest
        self.timeRemaining = newRequest.getTime()

class Request():
    def __init__(self,time, ptime):
        self.timestamp = time
        self.ptime = ptime
    def getStamp(self):
        return self.timestamp
    def getTime(self):
        return self.ptime
    def waitTime(self, currenttime):
        return currenttime - self.timestamp

def simulateOneServer(file):
    server = Server()
    server_queue = Queue()
    waiting_times = []
    for sec in range(max(file.keys())):
        if file[sec]:
            for x in file[sec]:
                request = Request(sec,x)
                server_queue.enqueue(request)
        if (not server.busy()) and (not server_queue.is_empty()):
            next_request = server_queue.dequeue() 
            waiting_times.append(next_request.wait_time(sec)) 
            server.start_next(next_request)
        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average wait time is %6.2f seconds." %(average_wait))

def simulateManyServers(file, servers):
    server_list = []
    server_queue = Queue()
    waiting_times = []
    for x in range(servers):
        server_list.append(Server())
        waiting_times.append([])
    for sec in range(max(file.keys())):
        if file[sec]:
            for x in file[sec]:
                request = Request(sec,x)
                server_queue.enqueue(request)
        for serv in range(len(server_list)):
            if (not server_list[serv].busy()) and (not server_queue.is_empty()):
                next_request = server_queue.dequeue() 
                waiting_times[serv].append(next_request.wait_time(sec)) 
                server_list[serv].start_next(next_request)
            server_list[serv].tick()
    avg_wait = []
    requests = []
    for x in range(servers):
        avg_wait.append(sum(waiting_times[x]) / len(waiting_times[x]))
        requests.append(request_queue.size())
    print("Average wait time is %6.2f seconds." %(sum(avg_wait)/len(avg_wait)))


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--url', type=str, required=True)
    parse.add_argument('--servers', nargs='?', type=int, default=1)
    args = parse.parse_args()
    
    url = urllib.request.urlopen(args.url).read()
    file = csv.reader(url.decode('utf-8').splitlines())
    result = collections.defaultdict(list)
    for row in file:
        result[int(row[0])].append(int(row[2]))
    servers = int(args.servers)
    if servers == 1:
        simulateOneServer(result)     
    else:
        simulateManyServers(result, servers)

if __name__  == '__main__':
    main()
