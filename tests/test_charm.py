# Copyright 2021 Yoshi Kadokawa
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import Mock

from charm import LokiCharm
from ops.model import ActiveStatus
from ops.testing import Harness

CONFIG_PATH = "/etc/loki/local-config.yaml"

class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(LokiCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_loki_pebble_ready(self):
        # Check the initial Pebble plan is empty
        initial_plan = self.harness.get_container_pebble_plan("loki")
        self.assertEqual(initial_plan.to_yaml(), "{}\n")
        # Expected plan after Pebble ready with default config
        expected_plan = {
            "services": {
                "loki": {
                    "override": "replace",
                    "summary": "loki",
                    "command": "/usr/bin/loki -target=all -config.file={}".format(CONFIG_PATH),
                    "startup": "enabled",
                }
            },
        }
        # Get the loki container from the model
        container = self.harness.model.unit.get_container("loki")
        # Emit the PebbleReadyEvent carrying the loki container
        self.harness.charm.on.loki_pebble_ready.emit(container)
        # Get the plan now we've run PebbleReady
        updated_plan = self.harness.get_container_pebble_plan("loki").to_dict()
        # Check we've got the plan we expected
        self.assertEqual(expected_plan, updated_plan)
        # Check the service was started
        service = self.harness.model.unit.get_container("loki").get_service("loki")
        self.assertTrue(service.is_running())
        # Ensure we set an ActiveStatus with no message
        self.assertEqual(self.harness.model.unit.status, ActiveStatus())
