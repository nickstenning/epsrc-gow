-- NB: SQLite does not support DROP COLUMN, thus making this migration
--     *irreversible* in SQLite.

ALTER TABLE grants DROP COLUMN start_date;
ALTER TABLE grants DROP COLUMN end_date;
ALTER TABLE grants DROP COLUMN scheme;
ALTER TABLE grants DROP COLUMN abstract;
ALTER TABLE grants DROP COLUMN final_report_summary;
ALTER TABLE grants DROP COLUMN further_information;
ALTER TABLE grants DROP COLUMN panel_history;

DROP TABLE sectors;
DROP TABLE grants_sectors;
DROP TABLE research_topics;
DROP TABLE grants_research_topics;
DROP TABLE grants_project_partners;
DROP TABLE grants_investigators;
DROP TABLE grants_related_grants;
