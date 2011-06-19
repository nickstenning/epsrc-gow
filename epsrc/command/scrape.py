import sys
import argparse
import sqlite3

from epsrc.scraper import Scraper

SCHEMA_VERSION = 3

parser = argparse.ArgumentParser(description='Scrape EPSRC Grants on the Web data.')
parser.add_argument('database', type=str,
                    help='The database to fill or update with scraped data.')
parser.add_argument('-b', '--basic', action='store_true', default=False,
                    help='Only scrape basic data.')
parser.add_argument('-d', '--detailed', action='store_true', default=False,
                    help='Only scrape detailed data (using current database content as starting point).')
parser.add_argument('-y', '--year', type=int, default=None,
                    help='Only scrape basic data for this financial year.')

def establish_connection(db):
    conn = sqlite3.connect(db)

    schema_version = None

    try:
        schema_version = conn.execute("select version from schema limit 1").fetchone()[0]
    except sqlite3.OperationalError, e:
        pass

    if schema_version != SCHEMA_VERSION:
        print "The database needs to be at schema version %d." % SCHEMA_VERSION
        print "Perhaps you need to run migrate.sh?"
        sys.exit(1)

    conn.execute('pragma foreign_keys=on')

    return conn

def main():
    args = parser.parse_args()
    conn = establish_connection(args.database)

    s = Scraper(conn)

    if args.basic:
        if args.year:
            s.scrape_basic(range(args.year, args.year + 1))
        else:
            s.scrape_basic()
    elif args.detailed:
        s.scrape_detailed()
    else:
        s.scrape_all()

if __name__ == '__main__':
    main()