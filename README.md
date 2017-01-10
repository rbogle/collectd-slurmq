## Collectd Plugin for Slurm Monitoring

This plugin delivers:
  core allocations: allocated,idle,total for each node and the cluster
  queue states: jobs running,pending,suspended,total

### Install

copy slurmq.conf to the include directory for collectd configs, typically
```
/etc/collectd.d
```
ensure the /etc/collectd.conf file includes this location

copy slurmq_types.db to a location for reading by collectd daemon, make sure it matches the location inthe slurm.conf file

```
/usr/share/collectd/slurmq.types.db
```
ensure that the main collectd config file includes the location of the main Types.db file:

```
TypesDB "/usr/share/collectd/types.db"
```
copy slurmq.py to a location for collectd plugins:
```
/usr/local/lib/Collectd/Plugins/
```

If the this data gets relayed to another location or collectd server you may need to copy the slurmq_types.db file to that server and include it in the collectd config there. 
