from __future__ import print_function

import re

import mechanize
from pyquery import PyQuery

import util


class GrantParseException(Exception):
    pass


GRANT_DETAIL_URL = "http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=%s"


def _extract_multiple_ids(elem, type):
    res = []

    for el in (PyQuery(x) for x in elem.find("a")):
        o = {}
        o['id'] = util.extract_id(el.attr.href, type)
        o['name'] = el.text()
        res.append(o)

    return res

def _scrape_grant_ref(g, el):
    grant_ref = el.find('#lblGrantReference').eq(0).text()
    if grant_ref != g['id']:
        msg = "Grant claims to be %s but has %s in scraped HTML!"
        raise GrantParseException, msg % (g['id'], grant_ref)


def _scrape_title(g, el):
    g['title'] = el.find('span#lblTitle strong').eq(0).text()


def _scrape_pi(g, el):
    pi_el = el.find('a#hlPrincipalInvestigator + a').eq(0)
    g['pi'] = pi = {}
    pi['id'] = util.extract_id(pi_el.attr.href, 'Person')
    pi['name'] = pi_el.text()


def _scrape_ois(g, el):
    g['other_investigators'] = _extract_multiple_ids(el, 'Person')


def _scrape_cois(g, el):
    g['co_investigators'] = _extract_multiple_ids(el, 'Person')


def _scrape_pps(g, el):
    g['project_partners'] = _extract_multiple_ids(el, 'Organisation')


def _scrape_dept(g, el):
    g['department']['name'] = el.find('#lblDepartment').eq(0).text()


def _scrape_org(g, el):
    g['organisation']['name'] = el.find('#lblOrganisation').eq(0).text()


def _scrape_scheme(g, el):
    g['scheme'] = el.find('#lblAwardType').eq(0).text()


def _scrape_dates_value(g, el):
    g['start_date'] = util.extract_date(el.find('#lblStarts').eq(0).text())
    g['end_date'] = util.extract_date(el.find('#lblEnds').eq(0).text())
    value = el.find('#lblValue').eq(0).attr.title
    g['value'] = util.extract_monetary_value(value)


def _scrape_research_topics(g, el):
    g['research_topics'] = rt = []

    for e in (PyQuery(x) for x in el.find('table td')):
        topic = e.text().strip().split(': ')

        if len(topic) > 0 and len(topic[0]) > 0:
            rt.append(topic)


def _scrape_sectors(g, el):
    g['sectors'] = se = []

    for e in (PyQuery(x) for x in el.find('table td')):
        sector = e.text().strip()
        if len(sector) > 0:
            se.append(sector)


def _scrape_related(g, el):
    g['related_grants'] = rg = []

    for e in (PyQuery(x) for x in el.find('table td a')):
        grant = e.text().strip()

        if len(grant) > 0:
            rg.append(grant)


def _scrape_panel_hist(g, el):
    g['panel_history'] = []

    for e in (PyQuery(x) for x in el.find('#dgPanelHistory tr.DetailValue')):
        ph = map(lambda x: PyQuery(x).text(), e.find('td'))
        ph[0] = util.extract_date(ph[0], "%d %b %Y")
        g['panel_history'].append(ph)


def _scrape_further_info(g, el):
    fi = el.find('td.DetailValueAlt').html().strip()
    if fi != '&nbsp;':
        g['further_information'] = fi


def _scrape_org_web(g, el):
    a = el.find('a').eq(0)
    if a:
        href = a.attr.href.strip()
        if len(href) > 0:
            g['organisation']['website'] = href

def _scrape_abstract(g, el):
    ab_el = el.find('#lblAbstract').eq(0)
    if ab_el:
      ab = ab_el.html().strip()
      if len(ab) > 0 and ab != 'No summary is available for this grant.':
        g['abstract'] = ab


def _scrape_final_report(g, el):
    fr_el = el.find('#lblFinalReportSummary').eq(0)
    if fr_el:
      fr = fr_el.html().strip()
      if len(fr) > 0 and fr != 'No final report summary is available for this grant.':
        g['final_report_summary'] = fr


MAPPING = {
    "EPSRC Reference:":             _scrape_grant_ref,
    "Title:":                       _scrape_title,
    "Principal Investigator:":      _scrape_pi,
    "Other Investigators:":         _scrape_ois,
    "Researcher Co-investigators:": _scrape_cois,
    "Project Partners:":            _scrape_pps,
    "Department:":                  _scrape_dept,
    "Organisation:":                _scrape_org,
    "Scheme:":                      _scrape_scheme,
    "Starts:":                      _scrape_dates_value,
    "EPSRC Research Topic Classifications:": _scrape_research_topics,
    "EPSRC Industrial Sector Classifications:": _scrape_sectors,
    "Related Grants:":              _scrape_related,
    "Panel History:":               _scrape_panel_hist,
    "Further Information:":         _scrape_further_info,
    "Organisation Website:":        _scrape_org_web
}


b = browser = mechanize.Browser()


def scrape_grant_detailed(ref):
    b.open(GRANT_DETAIL_URL % ref)
    return scrape_grant_detailed_from_html(b.response().read())


def scrape_grant_detailed_from_html(ref, html):

    def _scrape_row(idx, row):
        pqrow = PyQuery(row)
        key = pqrow.find('td').eq(0).text()

        if key in MAPPING:
            MAPPING[key](grant, pqrow)

    grant = {'id': ref, 'organisation': {}, 'department': {}}

    page = PyQuery(html)
    page.find('#tblFound tr').each(_scrape_row)

    _scrape_abstract(grant, page)
    _scrape_final_report(grant, page)

    return grant

