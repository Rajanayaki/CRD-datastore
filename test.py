import datastore_module as db
import time
import threading
event=threading.Event()
db.create('a','b',1)
db.read('a')
db.create('d',['c','d'])
db.read('d')
t=time.time()
while(time.time()<t+2):
    db.read('d')

db.read('a')
t1=threading.Thread(target=(db.create),args=('c','d')) 
t1.start()
event.wait(8)

t2=threading.Thread(target=(db.read),args=('a'))
t2.start()
event.wait(3)
