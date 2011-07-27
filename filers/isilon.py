#!/usr/local/bin/python
"""Collect CIFS/NFS data for Isilon filers"""
from fspkg import *
from globalfs import Gfs
from gethosts import GetHosts

class Isilon(object):
    def __init__(self):
        self.hostlist=GetHosts('isilon').hosts
        self.filerdict=defaultdict(defaultdict)

    def getShares(self,host):
            _nfsdict=Gfs().nfsDict
            _outCmd="ssh %s01 isi smb share list -v" % host
            _out=Popen(_outCmd.split(),stdout=PIPE).communicate()[0].split('\n\n')
            for block in _out:
                    lines=block.split('\n')
                    for line in lines:
                            if (len(line.split()) < 2 or
                                    "Description" in line.split()[0]): continue
                            (key,value)=line.split()
                            if key == "Name:": shareCIFS=value
                            if key == "Directory:": mountp=value
                    if not _nfsdict[host].has_key(mountp): shareNFS="N/A"
                    else: shareNFS=_nfsdict[host][mountp]

                    self.filerdict[host][mountp]=[shareNFS,shareCIFS]

    def prepdict(self):
        for host in self.hostlist:
                self.getShares(host)
                self.filerdict.update(Gfs().cleanShares(host,self.filerdict))
        return self.filerdict

if __name__ == "__main__": 
    isidict=Isilon().prepdict()
    Gfs().sort_dict(isidict)
