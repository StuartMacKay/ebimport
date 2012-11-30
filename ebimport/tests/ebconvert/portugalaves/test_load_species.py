import pkg_resources
import unittest

from ebimport.handlers import PortugalAvesHandler


class LoadSpeciesTests(unittest.TestCase):
    """Tests for the function load_species()."""

    def test_load_species(self):
        """Species file can be loaded from package resources."""
        obj = PortugalAvesHandler()
        location_file = pkg_resources.resource_filename(
            'ebimport', 'data/portugalaves/species.csv')
        obj.load_species(obj.species, location_file)
        self.assertTrue(obj.species)


