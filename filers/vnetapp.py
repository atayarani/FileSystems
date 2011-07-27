#!/usr/local/bin/python
"""Collect CIFS/NFS data for NetApp vfilers"""
from fspkg import *
from gethosts import GetHosts
from globalfs import Gfs

class vNetApp(object):
    def __init__(self):
        self.hostdict=GetHosts('vnetapp').hosts
        self.hostlist=self.hostdict.keys()
        self.filerdict=defaultdict(defaultdict)

    def getShares(self,host):
            __nfsDict=Gfs().nfsDict
            __vfiler=self.hostdict[host]
            __outCmd="ssh %s vfiler run %s cifs shares" % (host,__vfiler)
            __out=Popen(__outCmd.split(),stdout=PIPE).communicate()[0].split('\n')
            for line in __out:
                    fields=line.split()
                    if (len(fields) < 2 or
                            "vol" not in fields[1]): continue
        
                    (shareCIFS,mountp)=fields[0:2]
                    if not __nfsDict[__vfiler].has_key(mountp): shareNFS="N/A"
                    else: shareNFS=__nfsDict[__vfiler][mountp]
                    self.filerdict[__vfiler][mountp]=[shareNFS,shareCIFS]

    def prepdict(self):
        for host in self.hostlist: 
                self.getShares(host)
                self.filerdict.update(Gfs().cleanShares(host,self.filerdict))
        return self.filerdict

if __name__ == "__main__": 
    netappdict=vNetApp().prepdict()
    print vNetApp().hostdict.values()
    for k,v in netappdict.items():
        print '%s:%s' % (k,v)
