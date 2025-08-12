# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from re import L
from time import sleep
import unittest

from unittest.mock import patch, MagicMock
from ovos_bus_client import Message
from neon_phal_plugin_skill_api import NeonPhalPluginSkillAPI


class TestSkillApi(unittest.TestCase):
    def setUp(self):
        self.bus = MagicMock()
        self.plugin = NeonPhalPluginSkillAPI(bus=self.bus)

    def test_00_init(self):
        self.assertIsInstance(self.plugin, NeonPhalPluginSkillAPI)
        self.assertEqual(self.plugin.name, "neon-phal-plugin-skill-api")
        self.assertEqual(self.plugin.bus, self.bus)

        # Check Messagebus event listeners
        self.bus.on.assert_any_call("mycroft.ready", self.plugin._on_ready)
        self.bus.on.assert_any_call(
            "neon.skill_api.update", self.plugin.update_available_apis
        )
        self.bus.on.assert_any_call(
            "neon.skill_api.get", self.plugin.get_available_apis
        )

        self.bus.wait_for_response.assert_called_once_with(
            Message("mycroft.skills.is_ready")
        )

    def test_get_active_skills(self):
        self.bus.reset_mock()
        skills = self.plugin._get_active_skills()
        self.bus.wait_for_response.assert_called_once_with(
            Message(
                "skillmanager.list",
                context={
                    "source": ["neon-phal-plugin-skill-api"],
                    "destination": ["skills"],
                },
            ),
            "mycroft.skills.list",
        )
        self.assertEqual(skills, [])

        # TODO: Test with simulated response

    def test_get_skill_api_methods(self):
        self.bus.reset_mock()
        skill_id = "test_skill.neongeckocom"
        methods = self.plugin._get_skill_api_methods(skill_id)
        self.bus.wait_for_response.assert_called_once_with(
            Message(
                f"{skill_id}.public_api",
                context={
                    "source": ["neon-phal-plugin-skill-api"],
                    "destination": ["skills"],
                },
            )
        )
        self.assertEqual(methods, {})

        # TODO: Test with simulated response

    def test_update_available_apis(self):
        pass
        # TODO

    def test_get_available_apis(self):
        pass
        # TODO
