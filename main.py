#!/usr/bin/env python
# pylint: disable=missing-docstring,invalid-name

import time

from mininet.topo import Topo
from mininet.node import Controller, OVSKernelSwitch
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


class DCellController(Controller):
    """
    Run a POX controller for DCell routing in a separate process.
    Log location: /tmp/c0.log
    """
    def __init__(self, name):
        args = {
            "name": name,
            "command": "./pox/pox.py",
            "cargs": (
                "--verbose "
                "openflow.of_01 --port=%d "
                "openflow.discovery --link_timeout=1 "  # 1 sec
                "dcell_pox "
            )
        }
        Controller.__init__(self, **args)


class DCellTopo(Topo):
    def build(self, link_bw=100, switch_cls=OVSKernelSwitch):
        # tree topo
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")
        s1 = self.addSwitch("s1", cls=switch_cls)
        s2 = self.addSwitch("s2", cls=switch_cls)
        s3 = self.addSwitch("s3", cls=switch_cls)
        self.addLink(s1, h1, bw=link_bw)
        self.addLink(s1, h2, bw=link_bw)
        self.addLink(s2, h3, bw=link_bw)
        self.addLink(s3, h4, bw=link_bw)
        self.addLink(s3, s1, bw=link_bw)
        self.addLink(s3, s2, bw=link_bw)


def main():
    net = Mininet(topo=DCellTopo(), link=TCLink, controller=DCellController, autoSetMacs=True)
    net.start()
    time.sleep(3)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h3"
    h1, h3 = net["h1"], net["h3"]
    net.iperf((h1, h3))
    # CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()