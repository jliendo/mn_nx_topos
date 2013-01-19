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

    def build_nx_topo(self, g):
        """ 
        1) Create switches, hosts...attach host to switch acording to nx topo (self.ref_g)
        2) Add one host to each switch (h0->s0, h1->s1, etc.)
        3) Add edges between switches
        """
        # create switches and attach a host to the switch
        # one host per switch
        for n in g.nodes():
            n = n + 1
            self.addSwitch('s%d' % n)
            self.addHost('h%d' % n)
            self.addLink("s%d" % n, "h%d" % n)
        # link switches acording to topology
        for (n1, n2) in g.edges():
            n1 = n1 + 1
            n2 = n2 + 1
            self.addLink("s%d" % n1, "s%d" % n2)

    def graph(self):
        """ 
        Graph function. Has to be overloaded. For graphing puproses
        it can use self.ref_g which is mn_nx's view of the topology
        (this view has to match mininet's view, less the hosts) or
        it can also use self.g which is mininet's topology view
        """
        pass

class BalancedTree( NxTopo ):
    """networkx based BalancedTree topology.
       r = range (fanout), h = height (depth) """
    def __init__(self, **kwargs):
        # super
        super(BalancedTree, self).__init__()
        r = kwargs.get('r', 2)
        h = kwargs.get('h', 2)
        # mn_nx's topology view of the network
        self.ref_g = nx.balanced_tree(r,h)
        # nx topology definition
        self.build_nx_topo(self.ref_g)

    def graph(self):
        """
        Overloaded graph function to draw a hierachical view of
        tree-like topologies. Switches are red and there are no
        hosts on the graph. 
        In reality (mininet virtual network) there exists a host 
        for each switch in the topology with a name that starts 
        with 'hn' where 'n' is the switch number.
        """
        pos = nx.graphviz_layout(self.ref_g, prog='dot')
        nx.draw(self.ref_g, pos)
        plt.show()


class ErdosRenyi( NxTopo ):
    """networkx based Erdos-Renyi topology.
        n = Number of nodes, p = probability of an edge
        between nodes """
    def __init__(self, **kwargs):
        # super
        super(ErdosRenyi, self).__init__()
        n = kwargs.get('n', 5)
        p = kwargs.get('p', 0.8)
        # topology view of the network
        self.ref_g = nx.erdos_renyi_graph(n,p)
        # nx topology definition
        self.build_nx_topo(self.ref_g)

    def graph(self):
        pos = nx.circular_layout(self.ref_g)
        nx.draw(self.ref_g, pos)
        plt.show()


topos = { 'balanced_tree': (lambda **args: BalancedTree(**args)),
          'erdos_renyi'  : (lambda **args: ErdosRenyi(**args)) }

