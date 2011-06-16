import re

import mechanize
from pyquery import PyQuery

GRANT_DETAIL_URL = "http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=%s"

MAPPING = {
    "EPSRC Reference:":             scrape_grant_ref,
    "Title:":                       scrape_title,
    "Principal Investigator:":      scrape_pi,
    "Other Investigators:":         scrape_ois,
    "Researcher Co-investigators:": scrape_cois,
    "Project Partners:":            scrape_pps,
    "Department:":                  scrape_dept,
    "Organisation:":                scrape_org,
    "Scheme:":                      scrape_scheme,
    "Starts:":                      scrape_dates,
    "EPSRC Research Topic Classifications:": scrape_research_topics,
    "EPSRC Industrial Sector Classifications:": scrape_sectors,
    " Related Grants:":             scrape_related,
    "Panel History:":               scrape_panel_hist,
    "Further Information:":         scrape_further_info,
    "Organisation Website:":        scrape_org_web
}

b = browser = mechanize.Browser()

def scrape_grant_detailed(ref):
    grant = {'id': ref}

    b.open(GRANT_DETAIL_URL % ref)

    def scrape_row(i, r):
        key = PyQuery(r).find('td').eq(0).text()

    page = PyQuery(b.response().read())
    page.find('#tblFound tr').each(scrape_row)

if __name__ == '__main__':
    scrape_grant_detailed('GR/L27916/01')