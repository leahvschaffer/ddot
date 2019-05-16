import sys

sys.path.insert(0, '/cellar/users/f6zheng/Code/ddot-dev/')
from ddot import *

P = ['11111111',
     '11111100',
     '00001111',
     '11100000',
     '00110000',
     '00001100',
     '00000011']

nodes = 'ABCDEFGH'

w = Weaver(P, boolean=True, terminals=nodes, assume_levels=False)
T = w.weave(cutoff=0.9, top=10)
