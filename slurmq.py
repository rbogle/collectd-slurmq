
#!/usr/bin/env python

import pyslurm
import time

# removed interval for compat with collectd default.
#INTERVAL=30 # seconds

# Query queue for running,pending,suspended,total jobs in queue
def get_queue_counts():
    data = list()
    total =0
    states = ['RUNNING', 'PENDING', 'SUSPENDED']
    j = pyslurm.job()
    for state in states:
        count = len(j.find('job_state', state))
        data.append(count)
        total+=count
    data.append(total)
    return data

# Use nodes to get core allocations
def get_core_counts():
    data = dict()
    n = pyslurm.node()
    nodes = n.get()
    data['total']=[0,0,0]
    for id,node in nodes.iteritems():
        data[id] = [node['alloc_cpus'],node['cpus']-node['alloc_cpus'],node['cpus']]
        data['total'] = [x + y for x, y in zip(data['total'], data[id])]
    return data

# our callback for collecting all the data.
# uses the custom types:
# slurm_jobs: running,pending,suspended,total
# slurm_cores: alllocated, idle, total
# core counts are pushed for all nodes as well as total. 
def read_callback(data=None):
    now = int(time.time())
    queue = get_queue_counts()
    if queue:
        metric = collectd.Values()
        metric.plugin = 'slurmq'
        metric.type = 'slurm_jobs'
        # metric.time = now
        # metric.interval = INTERVAL
        metric.values = queue
        metric.dispatch()

    cores = get_core_counts()
    if cores:
     # for each key in each partition output, put the value
     for key in cores:
         metric = collectd.Values()
         metric.plugin = 'slurmq'
         metric.type = 'slurm_cores'
         metric.type_instance = key
         # metric.time = now
         # metric.interval = INTERVAL
         metric.values = cores[key]
         metric.dispatch()

if __name__ == '__main__':

    import pprint as pp
    queue = get_queue_counts()
    cores = get_core_counts()
    pp.pprint(queue)
    pp.pprint(cores)

else:
    import collectd
    # Register the callback
    collectd.register_read(read_callback)
