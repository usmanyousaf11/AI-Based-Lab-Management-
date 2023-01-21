#!/bin/env python
"""
Given a clone name, report any matching accessions in NCBI's nucleotide
database.
"""
from Bio import Entrez
import csv
import urllib2
Entrez.email = "jlhudd@uw.edu"

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_lims.settings")

from models import SequencedClone


def search_clone_by_name(clone_name):
    """
    Search NCBI's clone database for the given clone name and return a list of
    zero or more accessions from the nucleotide database.

    >>> search_clone_by_name("1205403_ABC13_11_000048822500_O14")
    ['AC216972']
    >>> search_clone_by_name("fakeclone")
    []
    """
    # By default, expect no accessions.
    accessions = []

    # Search NCBI clone database by clone name.
    try:
        handle = Entrez.esearch(db="clone", term=clone_name)

        clone_record = Entrez.read(handle)

        if clone_record["Count"] > 0:
            # Search nucleotide database for the nucleotide id of a record matching the clone id.
            handle = Entrez.elink(dbfrom="clone", db="nuccore", id=clone_record["IdList"])
            nuccore_record = Entrez.read(handle)
            nuccore_ids = [link_id["Id"]
                           for nuc in nuccore_record
                           for link in nuc["LinkSetDb"]
                           for link_id in link["Link"]]

            if len(nuccore_ids) > 0:
                # Get the summary of the nucleotide record(s) matching the clone id.
                handle = Entrez.esummary(db="nuccore", id=",".join(nuccore_ids))
                nuccore_summary = Entrez.read(handle)

                # Report the unique accession(s) for this term.
                accessions = list(set([summary["Caption"] for summary in nuccore_summary]))
    except urllib2.URLError:
        accessions = ["ncbi_lookup_failed"]

    return accessions


def load_report_records(report_filename):
    """
    Load records from an NCBI CloneDB report into the database.
    """
    clones = []

    with open(report_filename, "r") as report_fh:
        reader = csv.DictReader(report_fh, delimiter="\t")
        for row in reader:
            if row["Stdn"] == "Y":
                clone = SequencedClone()
                for key, value in row.iteritems():
                    setattr(clone, key.lower(), value)

                clones.append(clone)

    SequencedClone.objects.bulk_create(clones)
