import pkg_resources
import unittest

from ebimport.handlers import PortugalAvesHandler


class LoadLocationTests(unittest.TestCase):
    """Tests for the function load_location()."""

    def test_load_locations(self):
        """Locations file can be loaded from package resources."""
        obj = PortugalAvesHandler()
        location_file = pkg_resources.resource_filename(
            'ebimport', 'data/portugalaves/locations.csv')
        obj.load_locations(obj.locations, location_file)
        self.assertTrue(obj.locations)


