# -*- coding: utf-8 -*-

import unittest

from ebimport.handlers import PortugalAvesHandler


class ConvertLocationTestCase(unittest.TestCase):
    """Test for the convert_location() function."""

    def setUp(self):
        super(ConvertLocationTestCase, self).setUp()
        self.obj = PortugalAvesHandler()
        self.obj.locations = {
            ('location a', '1.1', '1.1'): {
                'eBird Location': 'Location A',
                'eBird Region Code': 'Region A',
                'eBird Country Code': 'CC',
                'eBird Latitude': '1.0000',
                'eBird Longitude': '1.0000',
                },
            ('location b', '2.0001', '2.0001'): {
                'eBird Location': 'Location B',
                'eBird Region Code': 'Region B',
                'eBird Country Code': 'CC',
                'eBird Latitude': '2.0000',
                'eBird Longitude': '2.0000',
                }
        }

    def test_convert_location_name(self):
        """The location name is updated"""
        rin = {
            'Location': 'location a',
            'Region/State': 'region a',
            'Latitude': '1.1',
            'Longitude': '1.1',
        }
        actual = self.obj.convert_location(rin)
        self.assertEqual(actual['Location Name'], 'Location A')

    def test_convert_region(self):
        """The region is updated"""
        rin = {
            'Location': 'location a',
            'Region/State': 'region a',
            'Latitude': '1.1',
            'Longitude': '1.1',
            }
        actual = self.obj.convert_location(rin)
        self.assertEqual(actual['State/Province'], 'Region A')

    def test_convert_country(self):
        """The region is updated"""
        rin = {
            'Location': 'location a',
            'Region/State': 'region a',
            'Latitude': '1.1',
            'Longitude': '1.1',
            }
        actual = self.obj.convert_location(rin)
        self.assertEqual(actual['Country Code'], 'CC')

    def test_convert_latitude(self):
        """The latitude is updated"""
        rin = {
            'Location': 'location a',
            'Region/State': 'region a',
            'Latitude': '1.1',
            'Longitude': '1.1',
            }
        actual = self.obj.convert_location(rin)
        self.assertEqual(actual['Latitude'], '1.0000')

    def test_convert_longitude(self):
        """The longitude is updated"""
        rin = {
            'Location': 'location a',
            'Region/State': 'region a',
            'Latitude': '1.1',
            'Longitude': '1.1',
            }
        actual = self.obj.convert_location(rin)
        self.assertEqual(actual['Longitude'], '1.0000')

    def test_result_is_marked_as_converted(self):
        """Location Converted is True for converted locations"""
        rin = {
            'Location': 'location a',
            'Region/State': 'region a',
            'Latitude': '1.1',
            'Longitude': '1.1',
            }
        actual = self.obj.convert_location(rin)
        self.assertTrue(actual['Location Converted'])

    def test_unknownlocation_is_not_marked_as_converted(self):
        """Location Converted is False for unknown locations"""
        rin = {
            'Location': 'location z',
            'Region/State': 'region z',
            'Latitude': '1.1',
            'Longitude': '1.1',
            }
        actual = self.obj.convert_location(rin)
        self.assertFalse(actual['Location Converted'])
