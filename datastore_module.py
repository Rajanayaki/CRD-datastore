import threading
from threading import *
import json
import time

lock=threading.Lock() #to ensure only one client process is allowed to use the file

data_store={}
ds_size=1073741824 #data store size = 1gb
value_size=16384 # data value size =16kb
json_data=data_store # for json data objects

#create operation
def create(key,value,time_to_live=0):
    lock.acquire()
    json_data=data_store
    try:
        if key in json_data:
            print("Key Error: Key already exists!")
        else:
            if key.isalpha(): #checks the key for only alphabets
                data=[value,time_to_live]
                if(time_to_live==0):
                    if len(json_data)<ds_size and len(data[0])<value_size: #checks json object size and new value size
                        data_store[key]=data
                        json_data=json.dumps(data_store,indent=2) #dumps data into json object
                        
                        print("Success")
                        print(json_data) #new json object
                    else:
                        print("Storage Error: No enough space")
                else:
                    data[1]=time.time()+time_to_live 
                    data_store[key]=data
                    json_data=json.dumps(data_store,indent=2)
            else:
                print("Key Error: Keys should contain only alphabets")
    finally:
        lock.release()

#read operation
def read(key):
    lock.acquire()
    try:
        if key not in json_data:
            print("Key Error: Key doesnt exist!")
        else:
            data=json_data[key]
            if data[1]==0:
                print(json_data[key][0])
            elif data[1]>time.time():  #checks for time to live
                print(json_data[key][0])
            else:
                print("Time Error:Key or value expired!")
    finally:
        lock.release()

#delete operation
def delete(key):
    lock.acquire()
    try:
        if key not in data_store:
            print("Key Error: Key doesnt exist!")
        else:
            data=data_store[key]
            if data[1]==0 or (data[1]!=0 and data[1]<time.time()):
                data_store.pop(key)
                json_data=json.dump(data_store)
                print("Sucess: Key-Value deleted")
            else:
                print("Time Error:Key or value expired!")
    finally:
        lock.release()
