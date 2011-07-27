#!/usr/bin/env python
"""Collect CIFS/NFS data for Toros"""
from fspkg import *
from globalfs import Gfs
from gethosts import GetHosts

class Toro(object):
    def __init__(self):
        self.hostlist=GetHosts('toro').hosts
        self.filerdict=defaultdict(defaultdict)

    def getShares(self,host):
            nfsDict=Gfs().nfsDict

            _child=spawn("ssh %s" % host) 
            _child.expect("%s:>" % host)
            _child.sendline('shares list')
            _child.expect("%s:>" % host)
            _projectlist=_child.before.split('\n')

            for project in _projectlist:
                    project=project.strip('\r')
                    if ('shares list' in project or
                            '\x1b' in project or
                            len(project) < 1): continue
                    _child.sendline("shares select %s" % project)
                    _child.expect("%s:shares %s>" % (host,project))
                    _child.sendline('list')
                    _child.expect("%s:shares %s>" % (host,project))
                    mounts=_child.before.split('\n')
                    for item in mounts:
                            item=item.strip('\r')
                            if ('list' in item or
                                    'NAME' in item or
                                    'Filesystems:' in item or 
                                    '\x1b' in item or 
                                    len(item) < 1): continue
                            share=item.split()[0]
                            _child.sendline("select %s" % share)
                            _child.expect("%s:shares %s/%s>" % (host,project,share))
                            _child.sendline('get mountpoint')
                            _child.expect("%s:shares %s/%s>" % (host,project,share))
                            mountp=_child.before.split('\n')[1].split()[2]
                            _child.sendline('get sharesmb')
                            _child.expect("%s:shares %s/%s>" % (host,project,share))
                            isCIFS=_child.before.split('\n')[1].split()[2]
                            shareCIFS="N/A" if isCIFS.split(',')[0] == "off" else "%s" % (isCIFS.split(',')[0])
                            _child.sendline('get sharenfs')
                            _child.expect("%s:shares %s/%s>" % (host,project,share))
                            isNFS=_child.before.split('\n')[1].split()[2]
                            if (isNFS == "off" or
                                    not nfsDict[host].has_key(mountp)):
                                    shareNFS="N/A"
                            else:
                                    shareNFS=nfsDict[host][mountp]
                            _child.sendline('done')
                            _child.expect("%s:shares %s>" % (host,project))
                            self.filerdict[host][mountp]=[shareNFS,shareCIFS]
                    _child.sendline('done')
            _child.expect("%s:>" % host)
            _child.sendline('exit')
            _child.expect(EOF)

    def prepdict(self):
        for host in self.hostlist: self.getShares(host)
        return self.filerdict


if __name__ == "__main__": 
    torodict=Toro().prepdict()
    Gfs().sort_dict(torodict)
