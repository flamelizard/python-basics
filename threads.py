"""Fun lab with threads"""

"""
TAKEAWAY !!
It is best to use simple scenario to familiarize with new stuff than making
elaborate smart scenario like war simulator. It only got me drowning in
simulator details.

Simulator - war game

Hero has a health
Enemies will attack after some period and will delpete hero's health
Fruit packs will occasionally occur to boost health
Hero needs to surive specific number of enemy attacks to complete level

"""

import time
from threading import Thread, Condition, Lock
import random

class WarGame(object):
    def __init__(self, hero='BJ'):
        self.health = 100
        self.hero = hero
        self.war_ended = False

    def fight(self, land, enemy_dmg):
        while self.health > 0:
            print '%s on the battlefield in %s...' % (self.hero, land)
            time.sleep(1)
            self.health -= enemy_dmg
            print '--> health %s%% in %s' % (self.health, land)

    def negotiate_peace(self, n):
        """
        :ret True to end the war
        """
        cond = Condition()
        time.sleep(3)
        cond.notify_all

# war = WarGame()
# for land in ['Iraq', 'Benghazi', 'Shanghai']:
#     t = Thread(target=war.fight, args=(land, 10))
#     t.start()
# t.join()
# print '[war has ended]'

"""Thread

Interpreter will not finish until there are running threads. Unless, the thread
runs as daemon, use attribute .daemon = True.

.join() will block until all non-daemon threads has finished.
"""

"""
threading.Condition

This kind of lock is usefull only for synchronized access to shared storage.

Use .wait to have threads wait for update to storage that is signalled by call
to .notify from another thread. Method .wait will release lock until recieves
.notify.

Note that code execution blocks when lock is not available upon call to
.acquire or .wait. This is standard behaviour for acquiring lock.
"""

# Condition obj to control access to var store
store_updated_cond = Condition()
store = []

def consumer(name):
    # 'with' here equals .aquire and .release lock on exit
    # code execution will block (stop) here until lock is available
    with store_updated_cond:
        try:
            item = store.pop()
            print '[consume item %s]' % item
        except IndexError:
            print '[block until item available]'
            store_updated_cond.wait()

            item = store.pop()
            print '[consume item %s]' % item

def producer():
    for i in range(10):
        time.sleep(3)
        with store_updated_cond:
            print '[produce item]'
            store.append(random.randint(0, 10))

            # notify waiting threads that storage has been updated
            store_updated_cond.notify()
        # release the lock

# Thread(target=consumer).start()
# Thread(target=producer).start()

class Consumer(object):
    def __init__(self, name):
        self.name = name

    def consume(self, items=2):
        while items > 0:
            with store_updated_cond:
                try:
                    print '[%s] consume %s' % (self.name, store.pop())
                    items -= 1
                except IndexError:
                    print '[%s] wait for item' % self.name
                    store_updated_cond.wait()
                    # print '[%s] consume %s' % (self.name, store.pop())

"""
Scenario using Condition with multiple threads in .wait

Signalling with .notify seems to alternate threads equally 1-2-3-1-2-3...
Signalling with .notify_all is non-deterministic at when threads get a turn to
acquire a lock.

"""
# c1 = Consumer('jack')
# c2 = Consumer('sean')
# c3 = Consumer('mark')
# Thread(target=c1.consume).start()
# Thread(target=c2.consume).start()
# Thread(target=c3.consume).start()
# Thread(target=producer).start()

"""Queue

Queue is thread-safe shared data structure for information exchange between
producer(s) and consumer(s)

Key facts

Call to .get() will pick always single item no matter item's type.

Some methods will "block" (suspend code execution) until Queue state has
changed.

For example .get() will by default "block" (wait) until it can get item from
the Queue. Conversely, .put() will "block" until it can use Queue to put a
data on.

This default blocking behaviour can be overriden by argument "block=False" in
which case the command will return immediatelly. However, .get(block=False)
will raise Empty if there is no item on the Queue.

Queue.join() will block until item counter is 0. Counter goes up with each .put
() and down with each call to .task_done().
Warning !! Tricky command which will complete instantly if it runs before
anything is put on Queue.

"""

import Queue
import threading

q = Queue.Queue()
# prevent overlapping output in stdout
safeprint = threading._allocate_lock()

def producer(n, q):
    for i in range(n):
        with safeprint:
            print '[produce item]', i
        q.put(('product', i))
        time.sleep(2)

def consumer(q):
    assert isinstance(q, Queue.Queue)
    while True:
        item = q.get()
        with safeprint:
            print '[consume item]', item
        q.task_done()
        time.sleep(1)

tp = Thread(target=producer, args=(3, q))
tp.start()

tc = Thread(target=consumer, args=(q,))
tc.daemon = True
tc.start()

# q.join()
# print '[queue - all tasks marked done]'

tp.join()
if tp.is_alive():
    print '[thread is still runnning]'















