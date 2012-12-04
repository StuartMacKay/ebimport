#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import datetime
import pkg_resources
import re

from ebimport.shared import read_csv_file


EBIRD_HEADERS = [
    'Common Name',
    'Genus',
    'Species',
    'Number',
    'Species Comments',
    'Location Name',
    'Latitude',
    'Longitude',
    'Date',
    'Start Time',
    'State/Province',
    'Country Code',
    'Protocol',
    'Number of Observers',
    'Duration',
    'All observations reported?',
    'Effort Distance Miles',
    'Effort area acres',
    'Submission Comments',
]


class PortugalAvesHandler(object):
    species_filename = None
    species = {}

    locations_filename = None
    locations = {}

    headers = [
        'Family name',
        'Family sequence',
        'Species sequence',
        'Scientific name',
        'Common name',
        'BirdLife common name',
        'Location','Region/State',
        'Location area',
        'Minimum Altitude',
        'Maximum Altitude',
        'Latitude','Longitude',
        'Location notes',
        'WBDB code',
        'Location is IBA',
        'Location can have subunits',
        'Location is private',
        'Location validated',
        'Location accuracy',
        'Visit date',
        'Start time',
        'End time',
        'Timebirding',
        'Number of observers',
        'Visit notes','Number',
        'Activity',
        'Purpose',
        'Duplicate',
        'Observation is private',
        'Status',
        'Validation notes',
        'All birds recorded?',
        'Poor conditions',
        'Visit species notes',
        'Location ID',
        'Visit ID',
        'Visit Species ID',
    ]

    species_filename = 'data/portugalaves/species.csv'
    locations_filename = 'data/portugalaves/locations.csv'

    def load_resources(self):
        species_file = pkg_resources.resource_filename(
            'ebimport', self.species_filename)
        self.load_species(self.species, species_file)
        locations_file = pkg_resources.resource_filename(
            'ebimport', self.locations_filename)
        self.load_locations(self.locations, locations_file)

    def load_species(self, table, filename):
        """Update the species table with the records from the file.

        arguments:
            table (dict): maps BirdLife common name to the equivalent species
                used by eBird.
            filename (str): the path to a csv formatted file.
        """
        species_table = read_csv_file(filename)
        for entry in species_table:
            key = entry['BirdLife common name']
            table[key] = entry

    def load_locations(self, table, filename):
        """Update the location table with the records from the file.

        arguments:
            table (dict): maps Worldbirds location to the equivalent location
                used by eBird.
            filename (str): the path to a csv formatted file.
        """
        locations_table = read_csv_file(filename)
        for entry in locations_table:
            key = (entry["Worldbirds Location"], entry["Worldbirds Latitude"],
                   entry["Worldbirds Longitude"])
            table[key] = entry

    def read_header(self, file):
        """Get the names of the fields for the records.

        Skip over the contents of the file until the data section starts, which
        is a line containing only the string 'Data'. The first non-blank row after
        that contains the field names for the exported records.

        A ValueError is raised if the row contains the field names appears to be
        missing.

        arguments:
            fp (File): a file object containing the records.

        returns:
            an array containing the names of the fields.
        """
        headers = []
        next = False
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.lower() == u'data':
                next = True
            elif next:
                if re.search('\d', line, re.UNICODE):
                    raise ValueError("Found a record instead of the column names")
                headers = line.split('\t')
                break
        if not headers:
            raise ValueError("Could not find row containing column names")
        return headers

    def read_record(self, line, names):
        """Read the record into a dict.

        An extra field, Row Number, is added to identify the record in the
        file. eBird csv files do not contain a header row with the column names
        so the same number can be used to identify a row in the output file.

        arguments:
            line (unicode): a line read from the file containing a record from
                WorldBirds.
            names (list(str)): a list of the names of each field in the record.

        returns:
            a dict with the field names as the key and the value from the
            corresponding column in the record.
        """
        fields = [column.strip() for column in line.strip().split('\t')]
        return dict(zip(['Row Number'] + names, fields))

    def convert_species(self, rin):
        """Map the WorldBirds species name to the species name used in eBird.

        In addition to the fields used by eBird a field, species Converted, with
        a value of True or False is added to indicate whether an eBird species
        name matching the BirdLife common name used by WorldBirds was found. This
        is used to identify the records which must either be edited before the
        records are imported into eBird or corrected after the initial import.

        arguments:
            rin (dict): the record from WorldBirds
            species (dict): the table of eBird species names

        returns:
            a dict containing the fields for an eBird species.
        """
        name = rin['BirdLife common name']
        rout = {
            'Common Name': '',
            'Genus': '',
            'Species': '',
            }
        if name in self.species:
            rout['Common Name'] = self.species[name]['eBird Common Name']
            rout['Species Converted'] = True
        else:
            rout['Common Name'] = name
            rout['Species Converted'] = False
        return rout

    def convert_location(self, rin):
        """Update the location details if there is an entry in the table.

        arguments:
            rin (dict): the record from WorldBirds
            table (dict): a table of values that define a location.

        returns
            the records with the location related field updated if there is a
            corresponding entry in the table.

        """
        rout = {
            'Location Name': rin["Location"],
            'Latitude': rin["Latitude"],
            'Longitude': rin["Longitude"],
            'State/Province': '',
            'Country Code': '',
            'Location Converted': False,
            }

        key = rin["Location"], rin["Latitude"], rin["Longitude"]
        if key in self.locations:
            entry = self.locations[key]
            if entry['eBird Location']:
                rout['Location Name'] = entry['eBird Location']
                rout['Latitude'] = entry['eBird Latitude']
                rout['Longitude'] = entry['eBird Longitude']
            rout['State/Province'] = entry['eBird Region Code']
            rout['Country Code'] = entry['eBird Country Code']
            rout['Location Converted'] = True
        return rout

    def convert_record(self, rin):
        """Convert the record from WorldBirds to the format used by eBird.

        In addition to mapping the different fields and values the conversion
        also handles mapping locations and species names used in WorldBirds to the
        equivalent locations and species named used in eBird. If a mapping cannot
        be found then the value(s) from the WorldBirds record will be added
        directly allowing the mapping to be performed when the records are imported
        into eBird.

        arguments:
            record_in (dict): a dict containing the fields names and values from
                the WorldBirds record.

        returns:
            a dict mapping the names and values from the WorldBirds record to the
            format used by eBird.
        """
        rout = {
            'Protocol': '',
            'Effort Distance Miles': '',
            'Effort area acres': '',
            }

        rout.update(self.convert_species(rin))

        if not rin['Number'] or rin['Number'].lower() == 'present':
            rout['Number'] = 'X'
        else:
            rout['Number'] = rin['Number']

        rout['Species Comments'] = rin['Visit species notes'].replace('"', "'")

        rout.update(self.convert_location(rin))

        date = datetime.datetime.strptime(rin['Visit date'], "%Y-%m-%d")
        rout['Date'] = date.strftime("%m/%d/%Y")

        start_time = datetime.datetime.strptime(rin['Start time'], "%H:%M")
        rout['Start Time'] = start_time.strftime("%H:%M")

        end_time = datetime.datetime.strptime(rin['End time'], "%H:%M")
        duration_hours = (end_time - start_time).seconds / 3600
        duration_minutes = ((end_time - start_time).seconds % 3600) / 60
        rout['Duration'] = "%d" % (duration_hours * 60 + duration_minutes)

        rout['Number of Observers'] = rin['Number of observers']
        rout['All observations reported?'] = rin['All birds recorded?'][0].upper()
        rout['Submission Comments'] = rin['Visit notes'].replace('"', "'")

        return rout

    def convert_file(self, filein, fileout):
        fin = None
        fout = None
        record_number = 1

        try:
            fin = codecs.open(filein, 'rb', 'utf-16')
            self.read_header(fin)

            for line in fin:
                rin = self.read_record(line, self.headers)
                rout = self.convert_record(rin)

                if not fout:
                    fout = open(fileout, 'wb')
                row = ['"%s"' % rout[name] for name in EBIRD_HEADERS]
                fout.write(','.join(row).encode('utf-8'))
                fout.write('\r\n')
                record_number += 1

        except Exception, err:
            pass
        finally:
            if fin:
                fin.close()
            if fout:
                fout.close()
