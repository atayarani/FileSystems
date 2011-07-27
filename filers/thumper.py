#!/usr/local/bin/python
"""Collect CIFS/NFS data for Thumpers"""
from fspkg import *
from globalfs import Gfs
from gethosts import GetHosts

class Thumper(object):
    def __init__(self):
        self.hostlist=GetHosts('thumper').hosts
        self.filerdict=defaultdict(defaultdict)

    def getShares(self,host):
            _nfsdict=Gfs().nfsDict
            _outCmd="ssh %s cat /etc/sfw/smb.conf" % host
            _out=Popen(_outCmd.split(),stdout=PIPE).communicate()[0].split('\n\n')
            for block in _out:
                    share=""
                    mountp=""
                    lines=block.split('\n')
                    for line in lines:
                        if (not search('\[|path',line) or
                            line.startswith(';')): continue
                        if '[' in line and 'global' not in line: share=line.strip('[').strip(']')
                        if 'path' in line: mountp=line.split('=')[1].strip()
                    if (len(mountp) > 0): 
                            shareCIFS=share
                            if not _nfsdict[host].has_key(mountp): shareNFS="N/A"
                            else: shareNFS=_nfsdict[host][mountp]
                            self.filerdict[host][mountp]=[shareNFS,shareCIFS]

    def prepdict(self):
        for host in self.hostlist:
                self.getShares(host)
                self.filerdict.update(Gfs().cleanShares(host,self.filerdict))
        return self.filerdict

if __name__ == "__main__": 
    thumperdict=Thumper().prepdict()
    Gfs().sort_dict(thumperdict)

