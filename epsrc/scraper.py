from __future__ import print_function

import re
import sys
import datetime
import json
from itertools import repeat

from basic import scrape_grants_for_fy
from detailed import scrape_grant_detailed


def timestamp():
    return str(datetime.datetime.now())


class Scraper(object):

    def __init__(self, conn):
        self.conn = conn

    def scrape_all(self):
        self.scrape_basic()
        self.scrape_detailed()

    def scrape_basic(self, years=range(1985, datetime.date.today().year - 1)):
        print("Scraping basic grants data:", file=sys.stderr)

        for year in years:
            print("  financial year %d-%d" % (year, year + 1), file=sys.stderr)

            for g in scrape_grants_for_fy(year):
                pi = grant.pop('pi')
                org = grant.pop('organisation')
                dept = grant.pop('department')

                grant['principal_investigator_id'] = pi['id']
                grant['department_id'] = dept['id']

                dept['organisation_id'] = org['id']

                self.update_or_create_person(pi)
                self.update_or_create_organisation(org)
                self.update_or_create_department(dept)
                self.update_or_create_grant(grant)

            self.conn.commit()

    def scrape_detailed(self):
        print("Scraping detailed grants data:", file=sys.stderr)

        curs = self.conn.cursor()
        curs.execute('select id from grants')
        batch = curs.fetchmany(20)

        while batch:
            for b in batch:
                id = b[0]
                print("  %s" % id, file=sys.stderr)
                grant = scrape_grant_detailed(id)
                self._process_grant_detailed(grant)

            self.conn.commit()
            print("  COMMITTED BATCH")
            batch = curs.fetchmany(20)

    def _process_grant_detailed(self, grant):
        curs = self.conn.cursor()

        # First, update PI. We have the id from the scrape.

        self.update_or_create_person(grant.pop('pi'))

        # Second, department and organisation. We need to retrieve ids from
        # the database.

        org = grant.pop('organisation')
        dept = grant.pop('department')

        sql = '''select d.organisation_id, g.department_id
                 from grants as g
                 left join departments as d on d.id = g.department_id
                 where g.id = ?'''

        curs.execute(sql, (grant['id'],))

        org['id'], dept['id'] = curs.fetchone()

        self.update_or_create_organisation(org)
        self.update_or_create_department(dept)

        # Project partners

        for o in grant.pop('project_partners'):
            self.update_or_create_organisation(o)

            sql = '''insert or ignore into grants_project_partners
                     (grant_id, organisation_id, created_at, modified_at)
                     values (?, ?, ?, ?)'''

            t = timestamp()
            curs.execute(sql, (grant['id'], o['id'], t, t))

        # Sectors

        for s in grant.pop('sectors'):
            s_id = self.update_or_create_sector(s)

            sql = '''insert or ignore into grants_sectors
                     (grant_id, sector_id, created_at, modified_at)
                     values (?, ?, ?, ?)'''

            t = timestamp()
            curs.execute(sql, (grant['id'], s_id, t, t))

        # Research topics

        for rt in grant.pop('research_topics'):
            # Occasionally we get an "Unclassified" grant. There's no point
            # storing this
            if len(rt) == 1 and rt[0] == 'Unclassified':
                continue

            # Assert bipartite research topic, simply because the code below
            # assumes it. The database could support an arbitrary tree.
            assert len(rt) == 2

            # A parent_id of -1 indicates the "Root" topic, as INSERTed by the
            # migration file 002_up.sql
            prt_id = self.update_or_create_research_topic(rt[0], -1)
            rt_id = self.update_or_create_research_topic(rt[1], prt_id)

            sql = '''insert or ignore into grants_research_topics
                     (grant_id, research_topic_id, created_at, modified_at)
                     values (?, ?, ?, ?)'''

            t = timestamp()
            curs.execute(sql, (grant['id'], rt_id, t, t))

        # Co-investigators and Other investigators

        sql = '''insert or ignore into grants_investigators
                 (grant_id, person_id, type, created_at, modified_at)
                 values (?, ?, ?, ?, ?)'''

        t = timestamp()

        for p in grant.pop('other_investigators'):
            self.update_or_create_person(p)
            curs.execute(sql, (grant['id'], p['id'], 'other', t, t))

        for p in grant.pop('co_investigators'):
            self.update_or_create_person(p)
            curs.execute(sql, (grant['id'], p['id'], 'co', t, t))

        # Related grants

        for rg_id in grant.pop('related_grants'):
            sql = '''insert or ignore into grants_related_grants
                     (grant_id, related_grant_id, created_at, modified_at)
                     values (?, ?, ?, ?)'''

            t = timestamp()
            curs.execute(sql, (grant['id'], rg_id, t, t))

        # Finally, process grant itself

        grant['panel_history'] = json.dumps(grant['panel_history'])
        self.update_or_create_grant(grant)

    def update_or_create_grant(self, grant):
        self._update_or_create_object('grants', **grant)

    def update_or_create_person(self, person):
        self._update_or_create_object('people', **person)

    def update_or_create_organisation(self, organisation):
        self._update_or_create_object('organisations', **organisation)

    def update_or_create_department(self, department):
        self._update_or_create_object('departments', **department)

    def update_or_create_sector(self, sector):
        sql = '''insert or ignore into sectors
                 (name, created_at, modified_at)
                 values (?, ?, ?)'''

        t = timestamp()
        self.conn.execute(sql, (sector, t, t))

        sql = 'select id from sectors where name=?'
        (s_id,) = self.conn.execute(sql, (sector,)).fetchone()
        return s_id

    def update_or_create_research_topic(self, name, parent_id):
        sql = '''insert or ignore into research_topics
                 (name, parent_id, created_at, modified_at)
                 values (?, ?, ?, ?)'''

        t = timestamp()
        self.conn.execute(sql, (name, parent_id, t, t))

        sql = 'select id from research_topics where name=? and parent_id=?'
        (rt_id,) = self.conn.execute(sql, (name, parent_id)).fetchone()

        return rt_id

    def _update_or_create_object(self, table, **kwargs):
        sql = 'select count(*) from %s where id=?'
        params = (kwargs['id'],)
        res = self.conn.execute(sql % table, params).fetchone()

        if res[0] == 0:
            self._create_object(table, **kwargs)
        else:
            self._update_object(table, **kwargs)

    def _create_object(self, table, **kwargs):
        col_clause = ', '.join(kwargs.keys())
        val_clause = ', '.join(repeat('?', len(kwargs)))

        t = timestamp()

        params = kwargs.values()
        params.append(t)
        params.append(t)

        sql = 'insert into %s (%s, created_at, modified_at) values (%s, ?, ?)'
        self.conn.execute(sql % (table, col_clause, val_clause), params)

    def _update_object(self, table, **kwargs):
        uid = kwargs['id']
        del kwargs['id']

        set_clause = ', '.join(map(lambda x: x + '=?', kwargs.keys()))

        params = kwargs.values()
        params.append(timestamp())
        params.append(uid)

        sql = 'update %s set %s, modified_at=? where id=?'
        self.conn.execute(sql % (table, set_clause), params)
