import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from mininet.topo import Topo

class NxTopo ( Topo ):

    def __init__(self):
        # super
        super(NxTopo, self).__init__()

    def build_nx_topo(self, ref_g):
        # 1 Create switches, hosts...attach host to switch
        # 1.1 add one host to each switch (h0->s0, h1->s1, etc.)
        for n in ref_g.nodes():
            self.addSwitch('s%d' % n)
            self.addHost('h%d' % n)
            self.addLink("s%d" % n, "h%d" % n)

        # 2 Link switches 
        for (n1, n2) in ref_g.edges():
            self.addLink("s%d" % n1, "s%d" % n2)

    def graph(self):
        """ Draws a graphical representation of the topology"""
        pos = nx.spring_layout(self.g)

        # switch nodes in blue, hosts nodes in red
        nodes = self.node_info
        nx.draw_networkx_nodes(self.g, pos, \
                               nodelist = [x for x in nodes if nodes[x] and \
                                          nodes[x]['isSwitch']],
                               node_color = 'b')

        nx.draw_networkx_nodes(self.g, pos, \
                               nodelist = [x for x in nodes if not nodes[x]], \
                               node_color = 'r')

        nx.draw_networkx_edges(self.g, pos)
        nx.draw_networkx_labels(self.g, pos)
        plt.show()


class BalancedTree( NxTopo ):
    """networkx based BalancedTree topology"""
    def __init__(self, **p):
        # super
        super(BalancedTree, self).__init__()
        # nx topology definition
        self.build_nx_topo(nx.balanced_tree(p['r'], p['h']))
        self.build_nx_topo(ref_g)


class ErdosRenyi( NxTopo ):
    """networkx based Erdos-Renyi topology"""
    def __init__(self, **p):
        # super
        super(ErdosRenyi, self).__init__()
        # nx topology definition
        self.build_nx_topo(nx.erdos_renyi_graph(p['n'], p['p']))



topos = { 'balanced_tree': (lambda **args: BalancedTree(**args)),
          'erdos_renyi'  : (lambda **args: ErdosRenyi(**args))}

