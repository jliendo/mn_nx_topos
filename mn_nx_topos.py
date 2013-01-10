"""
Copyright (c) 2013, Javier Liendo
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list 
of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimer in the documentation and/or other 
materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from mininet.topo import Topo

class NxTopo ( Topo ):
    """Super class for basic NxTopo actions: switch/host add and graphing.
    All networkx based topologies must derive from this super class"""
    def __init__(self):
        # super
        super(NxTopo, self).__init__()

    def build_nx_topo(self, ref_g):
        """ 1 Create switches, hosts...attach host to switch acording to nx topo
            2 Add one host to each switch (h0->s0, h1->s1, etc.)
            3 Link switches between them"""
        # create switches and attach a host to the switch
        # one host per switch
        for n in ref_g.nodes():
            self.addSwitch('s%d' % n)
            self.addHost('h%d' % n)
            self.addLink("s%d" % n, "h%d" % n)
        # link switches acording to topology
        for (n1, n2) in ref_g.edges():
            self.addLink("s%d" % n1, "s%d" % n2)

    def graph(self):
        """ Draws a graphical representation of the topology.
            Switches are blue, hosts are red."""
        pos = nx.spring_layout(self.g)
        nodes = self.node_info
        # switches are blue
        nx.draw_networkx_nodes(self.g, pos, \
                               nodelist = [x for x in nodes if nodes[x] and \
                                          nodes[x]['isSwitch']],
                               node_color = 'b')
        # hosts are red
        nx.draw_networkx_nodes(self.g, pos, \
                               nodelist = [x for x in nodes if not nodes[x]], \
                               node_color = 'r')
        nx.draw_networkx_edges(self.g, pos)
        nx.draw_networkx_labels(self.g, pos)
        plt.show()


class BalancedTree( NxTopo ):
    """networkx based BalancedTree topology.
       r = range (fanout), h = height (depth) """
    def __init__(self, **kwargs):
        # super
        super(BalancedTree, self).__init__()
        r = kwargs.get('r', 2)
        h = kwargs.get('h', 2)
        # nx topology definition
        self.build_nx_topo(nx.balanced_tree(r, h))


class ErdosRenyi( NxTopo ):
    """networkx based Erdos-Renyi topology.
        n = Number of nodes, p = probability of an edge
        between nodes """
    def __init__(self, **kwargs):
        # super
        super(ErdosRenyi, self).__init__()
        n = kwargs.get('n', 5)
        p = kwargs.get('p', 0.8)
        # nx topology definition
        self.build_nx_topo(nx.erdos_renyi_graph(n, p))


topos = { 'balanced_tree': (lambda **args: BalancedTree(**args)),
          'erdos_renyi'  : (lambda **args: ErdosRenyi(**args)) }

