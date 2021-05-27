#!/usr/bin/env python3
# Copyright 2021 Giuseppe Petralia
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class MemcachedK8SClientCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.ubuntu_pebble_ready, self._on_ubuntu_pebble_ready)

        # Relations
        self.framework.observe(
            self.on["memcache"].relation_changed, self._on_memcache_relation_changed
        )
        self.framework.observe(
            self.on["memcache"].relation_departed, self._on_memcache_relation_departed
        )

        self._stored.set_default(memcached_servers={})

    def _on_ubuntu_pebble_ready(self, event):
        self.unit.status = ActiveStatus("Pod is ready")

    def _on_memcache_relation_changed(self, event):
        """Handle memcache-relation-changed event"""
        host = event.relation.data[event.unit].get("host")
        tcp_port = event.relation.data[event.unit].get("port")
        self._stored.memcached_servers.update({event.unit.name: {"host": host, "tcp_port": tcp_port}})

        for unit, memcached_server in self._stored.memcached_servers.items():
            host = memcached_server["host"]
            port = memcached_server["tcp_port"]
            logger.info(f"Available memcached_servers: {host}:{port}")

    def _on_memcache_relation_departed(self, event):
        """Handle memcache-relation-departed event"""
        if event.unit.name in self._stored.memcached_servers:
            del self._stored.memcached_servers[event.unit.name]

        for unit, memcached_server in self._stored.memcached_servers.items():
            host = memcached_server["host"]
            port = memcached_server["tcp_port"]
            logger.info(f"Available memcached_servers: {host}:{port}")


if __name__ == "__main__":
    main(MemcachedK8SClientCharm)
