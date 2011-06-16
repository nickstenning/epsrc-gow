from __future__ import print_function

import re
import sys

import mechanize
from pyquery import PyQuery

import util

PAST_GRANTS_URL = "http://gow.epsrc.ac.uk/SearchPastGrant.aspx"

RE_PERSON_ID = re.compile(r"PersonId=(\-?\d+)")
RE_ORGANISATION_ID = re.compile(r"OrganisationId=(\-?\d+)")
RE_DEPARTMENT_ID = re.compile(r"DepartmentId=(\-?\d+)")

b = browser = mechanize.Browser()

def scrape_grants_for_fy(year):
    b.open(PAST_GRANTS_URL)

    try:
        b.select_form(name="Form1")

        b["oUcStartDate$ddlDay"] = ["1"]
        b["oUcStartDate$ddlMonth"] = ["4"]
        b["oUcStartDate$ddlYear"] = [str(year)]

        b["oUcEndDate$ddlDay"] = ["31"]
        b["oUcEndDate$ddlMonth"] = ["3"]
        b["oUcEndDate$ddlYear"] = [str(year + 1)]

        resp = b.submit()
    except mechanize._form.ItemNotFoundError:
        print("ERROR: could not submit form. This usually means you're "
              "trying to scrape for a year that doesn't exist "
              "on the GOTW website.", file=sys.stderr)
        raise

    page = PyQuery(resp.read())

    for r in page("table tr:not(.GridHeader)"):
        grant = {}
        anchors = PyQuery(r).find('a')

        grant['id']    = anchors.eq(0).attr.title
        grant['title'] = anchors.eq(0).text()

        grant['pi']              = {}
        grant['pi']['id']        = util.extract_id(anchors.eq(1).attr.href, 'Person')
        grant['pi']['name']      = anchors.eq(1).text()

        grant['organisation']              = {}
        grant['organisation']['id']        = util.extract_id(anchors.eq(2).attr.href, 'Organisation')
        grant['organisation']['name']      = anchors.eq(2).text()

        grant['department']              = {}
        grant['department']['id']        = util.extract_id(anchors.eq(3).attr.href, 'Department')
        grant['department']['name']      = anchors.eq(3).text()

        value = PyQuery(r).find('span').eq(0).attr.title
        grant['value'] = util.extract_monetary_value(value)

        yield grant