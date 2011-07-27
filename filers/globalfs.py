#!/usr/local/bin/python
'''Contains global functions and variables for all filers'''
from fspkg import *

class Gfs:
    def __init__(self):
        self.nfsDict=self.nfs()

    def nfs(self):
        ypcatdict=ypcat('mounts.byname')
        nfsList=[v.split()[:2] for v in ypcatdict.values()]
        for pos,item in enumerate(nfsList):
            item=' '.join(item)
            item=item.replace(':',' ')
            nfsList[pos] = item
        nfsList.sort()
        localDict=defaultdict(defaultdict)

        for line in nfsList:
            fields=line.split()
            if len(fields) <= 1: continue
            (host,mount,share)=fields
            localDict[host][mount]=share
        return localDict
                
    def cleanShares(self,host,localDict):
        """
        Compares automount entries to CIFS shares to determine if filer has 
        NFS-only mounts
        """
        nfsDict=self.nfsDict
        if host in nfsDict.keys():
            for mountp in nfsDict[host].keys():
                if not localDict[host].has_key(mountp): 
                    shareCIFS="N/A"
                else: 
                    shareCIFS=localDict[host][mountp][1]
                shareNFS=nfsDict[host][mountp]
                localDict[host][mountp]=[shareNFS,shareCIFS]
        return localDict

    def sort_dict(self,local_dict):
        for host in sorted(local_dict.keys()):
            for mount in sorted(local_dict[host].keys()):
                share=local_dict[host][mount]
                print("%s,%s,%s,%s" % (host,mount,share[0],share[1]))

if __name__ == "__main__":
    _dictNFS=Gfs().nfs()
    for k in sorted(_dictNFS):
        for v in sorted(_dictNFS[k]):
            s=_dictNFS[k][v]
            print "key:%s\n(key)value:%s\nvalue:%s\n" % (k,v,s)
