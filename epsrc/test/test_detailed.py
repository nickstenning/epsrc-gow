import os
import unittest
import json

from epsrc.detailed import scrape_grant_detailed_from_html as scrape_detailed

FIXTURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/fixture'

def _grant_fixture(ref):
    param = (FIXTURE_DIR, ref)
    html = open('%s/%s.html' % param).read()
    data = json.loads(open('%s/%s.json' % param).read())
    return (html, data)

class TestDetailedScrape(unittest.TestCase):
    def test_dt_e004687_2(self):
        grant_html, grant_data = _grant_fixture('dt-e004687-2')

        assert scrape_detailed("DT/E004687/2", grant_html) == grant_data

    def test_ep_c005694_1(self):
        grant_html, grant_data = _grant_fixture('ep-c005694-1')

        assert scrape_detailed("EP/C005694/1", grant_html) == grant_data

    def test_ep_c011074_1(self):
        grant_html, grant_data = _grant_fixture('ep-c011074-1')

        assert scrape_detailed("EP/C011074/1", grant_html) == grant_data

    def test_ep_c535278_1(self):
        grant_html, grant_data = _grant_fixture('ep-c535278-1')

        assert scrape_detailed("EP/C535278/1", grant_html) == grant_data