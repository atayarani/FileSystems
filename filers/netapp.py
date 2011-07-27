#!/usr/local/bin/python
"""Collect CIFS/NFS data for NetApp filers"""
from fspkg import *
from gethosts import GetHosts
from globalfs import Gfs

class NetApp(object):
    def __init__(self):
        self.hostlist=GetHosts('netapp').hosts
        self.filerdict=defaultdict(defaultdict)

    def getShares(self,host):
            _nfsDict=Gfs().nfsDict
            _outCmd="ssh %s cifs shares" % host
            _out=Popen(_outCmd.split(),stdout=PIPE).communicate()[0].split('\n')
            for line in _out:
                    fields=line.split()
                    if (len(fields) < 2 or
                            "vol" not in fields[1]): continue
        
                    (shareCIFS,mountp)=fields[0:2]
                    if not _nfsDict[host].has_key(mountp): shareNFS="N/A"
                    else: shareNFS=_nfsDict[host][mountp]
                    self.filerdict[host][mountp]=[shareNFS,shareCIFS]

    def prepdict(self):
        for host in self.hostlist: 
                self.getShares(host)
                self.filerdict.update(Gfs().cleanShares(host,self.filerdict))
        return self.filerdict

if __name__ == "__main__": 
    netappdict=NetApp().prepdict()
    print netappdict
    #Gfs().sort_dict(netappdict)
