from __future__ import print_function

import re
import sys
import datetime
from itertools import repeat

from basic import scrape_grants_for_fy
# from detailed import scrape_grant_detailed


def timestamp():
    return str(datetime.datetime.now())


class Scraper(object):

    def __init__(self, conn):
        self.conn = conn
        self.curs = conn.cursor()

    def scrape_all(self):
        self.scrape_basic()
        self.scrape_detailed()

    def scrape_basic(self, years=range(1985, datetime.date.today().year - 1)):
        print("Scraping basic grants data:", file=sys.stderr)

        for year in years:
            print("  financial year %d-%d" % (year, year + 1), file=sys.stderr)

            for g in scrape_grants_for_fy(year):
                self.update_or_create_grant(g)

            self.conn.commit()

    def scrape_detailed(self):
        print("Scraping detailed grants data:", file=sys.stderr)

    def update_or_create_grant(self, grant):
        pi = grant['pi']
        org = grant['organisation']
        dept = grant['department']

        del grant['pi']
        del grant['organisation']
        del grant['department']

        grant['principal_investigator_id'] = pi['id']
        grant['department_id'] = dept['id']

        dept['organisation_id'] = org['id']

        self.update_or_create_person(pi)
        self.update_or_create_organisation(org)
        self.update_or_create_department(dept)

        self._update_or_create_object('grants', **grant)

    def update_or_create_person(self, person):
        self._update_or_create_object('people', **person)

    def update_or_create_organisation(self, organisation):
        self._update_or_create_object('organisations', **organisation)

    def update_or_create_department(self, department):
        self._update_or_create_object('departments', **department)

    def _update_or_create_object(self, table, **kwargs):
        sql = 'select count(*) from %s where id=?'
        params = (kwargs['id'],)
        res = self.curs.execute(sql % table, params).fetchone()

        if res[0] == 0:
            self._create_object(table, **kwargs)
        else:
            self._update_object(table, **kwargs)

    def _create_object(self, table, **kwargs):
        col_clause = ', '.join(kwargs.keys())
        val_clause = ', '.join(repeat('?', len(kwargs)))

        params = kwargs.values()
        params.append(timestamp())
        params.append(timestamp())

        sql = 'insert into %s (%s, created_at, modified_at) values (%s, ?, ?)'
        self.curs.execute(sql % (table, col_clause, val_clause), params)

    def _update_object(self, table, **kwargs):
        uid = kwargs['id']
        del kwargs['id']

        set_clause = ', '.join(map(lambda x: x + '=?', kwargs.keys()))

        params = kwargs.values()
        params.append(timestamp())
        params.append(uid)

        sql = 'update %s set %s, modified_at=? where id=?'
        self.curs.execute(sql % (table, set_clause), params)
