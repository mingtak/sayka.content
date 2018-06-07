# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from sayka.content.testing import SAYKA_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that sayka.content is properly installed."""

    layer = SAYKA_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if sayka.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'sayka.content'))

    def test_browserlayer(self):
        """Test that ISaykaContentLayer is registered."""
        from sayka.content.interfaces import (
            ISaykaContentLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ISaykaContentLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = SAYKA_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['sayka.content'])

    def test_product_uninstalled(self):
        """Test if sayka.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'sayka.content'))

    def test_browserlayer_removed(self):
        """Test that ISaykaContentLayer is removed."""
        from sayka.content.interfaces import \
            ISaykaContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ISaykaContentLayer,
           utils.registered_layers())
