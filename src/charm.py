#!/usr/bin/env python3
# Copyright 2021 Yoshi Kadokawa
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

CONFIG_PATH = "/etc/loki/local-config.yaml"


class LokiCharm(CharmBase):
    """Charm to run Loki on Kubernetes."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.loki_pebble_ready, self._on_loki_pebble_ready)
        self._stored.set_default(things=[])

    def _on_loki_pebble_ready(self, event):
        """Define and start a workload using the Pebble API."""
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        # Define an initial Pebble layer configuration
        pebble_layer = {
            "summary": "Loki layer",
            "description": "pebble config layer for Loki",
            "services": {
                "loki": {
                    "override": "replace",
                    "summary": "loki",
                    "command": "/usr/bin/loki -target=all -config.file={}".format(CONFIG_PATH),
                    "startup": "enabled",
                }
            },
        }
        # Add intial Pebble config layer using the Pebble API
        container.add_layer("loki", pebble_layer, combine=True)
        # Autostart any services that were defined with startup: enabled
        container.autostart()
        # Learn more about statuses in the SDK docs:
        # https://juju.is/docs/sdk/constructs#heading--statuses
        self.unit.status = ActiveStatus("loki started")


if __name__ == "__main__":
    main(LokiCharm)
