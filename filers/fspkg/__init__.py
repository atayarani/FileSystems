from collections import defaultdict
from nis import cat as ypcat
from pexpect import spawn,EOF
from re import search
from subprocess import *
#from globalfs import * #Needs to be last, or else imports break
