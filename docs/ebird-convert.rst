=============
ebird-convert
=============

Description
===========

Converts records exported from birding databases so they can be imported
into eBird::

    usage: ebird-convert [-h] [-l LOGFILE] [-q] [-s] [-v]
                         [-f {portugalaves}]
                         [-o OUTPUTFILE]
                         [FILE]

    Converts records into eBird's Checklist Record Format. The conversion
    process converts species names and matches locations to existing ones.
    Does not split the file into chunks of 1MByte or less as required by eBird.

    positional arguments:
      FILE                  The CSV file to convert.

    required arguments:
      -f                    The format of the file to convert. See below for a
                            complete list of the supported databases.

    optional arguments:
      -o  --output-file     Path to a file where the converted records will be
                            written. If omitted records will be written to the
                            file, ebird.csv in the current directory.
      -h, --help            show this help message and exit
      -l, --log-file        The file where log messages will be written. If
                            omitted messages will be written to stdout
      -q, --quiet           decrease the verbosity
      -s, --silent          only log warnings
      -v, --verbose         raise the verbosity



Supported Databases
===================

    portugalaves            Portugal Aves - BirdLife's database for bird
                            records in Portugal

                            http://birdlaa5.memset.net/worldbirds/portugal.php

                            Only converts personal records exported using the
                            "Download My Data" report. The formats used in other
                            reports which include observations from different
                            users of the database are not supported.
