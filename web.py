#!/usr/bin/env python
# encoding: utf-8
from bottle import run, post, request
import requests
import os
import json

port = int(os.environ.get('PORT'))

@post('/septa')
def septa():
    t = request.forms.get('text')
    #default output if no input was received
    if t is None or t == "":
        #form next two trains to station closest to office string
        msg = "To Spring Mill\n--------------\n\n"
        r = requests.get('http://www3.septa.org/hackathon/NextToArrive/30th%20Street%20Station/Spring%20Mill/2')
        data = r.json()
        #if septa error, return that
        if 'error' in data:
            return data['error']
        for i in range(0, len(data)):
            if data[i]["orig_delay"] != "On time":
                msg += "The {0} to Spring Mill is late by {1} :red_circle:\n".format(data[i]["orig_departure_time"], data[i]["orig_delay"])
            else:
                msg += "The {0} to Spring Mill is {1} :greenlight:\n".format(data[i]["orig_departure_time"], data[i]["orig_delay"])

        #form next two trains to station closest to home string
        msg += "\nTo Philadelphia\n---------------\n\n"
        r = requests.get('http://www3.septa.org/hackathon/NextToArrive/Spring%20Mill/30th%20Street%20Station/2')
        data = r.json()
        #if septa error, return that
        if 'error' in data:
            return data['error']
        for i in range(0, len(data)):
            if data[i]["orig_delay"] != "On time":
                msg += "The {0} to Philadelphia is late by {1} :red_circle:\n".format(data[i]["orig_departure_time"], data[i]["orig_delay"])
            else:
                msg += "The {0} to Philadelphia is {1} :greenlight:\n".format(data[i]["orig_departure_time"], data[i]["orig_delay"])
        return msg
    #display next five trains going to the station where the user entered
    else:
        fromStation = t.split("-")[0]
        toStation = t.split("-")[1]
        r = requests.get('http://www3.septa.org/hackathon/NextToArrive/{0}/{1}/5'.format(fromStation, toStation))
        data = r.json()
        #if septa error, return that
        if 'error' in data:
            return data['error']
        msgs = []
        msg = ""
        for i in range(0, len(data)):
            if data[i]["orig_delay"] != "On time":
                msg = "The {0} to {1} is late by {2} :red_circle:".format(data[i]["orig_departure_time"], toStation, data[i]["orig_delay"])
            else:
                msg = "The {0} to {1} is {2} :greenlight:".format(data[i]["orig_departure_time"], toStation, data[i]["orig_delay"])
            msgs.append(msg)
        return "\n".join(msgs)

if __name__ == '__main__':
    run(host='0.0.0.0', port=port)
