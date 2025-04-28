#! /bin/bash

ps aux | grep python | grep data_generation.py | awk '{print $2}' | xargs kill -9
ps aux | grep ansysedt | awk '{print $2}' | xargs kill -9
ps aux | grep ansyscl | awk '{print $2}' | xargs kill -9
ps aux | grep mwrpcss | awk '{print $2}' | xargs kill -9
