UPDATE schema SET version=2;

ALTER TABLE grants ADD COLUMN start_date TEXT; -- DATE
ALTER TABLE grants ADD COLUMN end_date TEXT; -- DATE
ALTER TABLE grants ADD COLUMN scheme TEXT;
ALTER TABLE grants ADD COLUMN abstract TEXT;
ALTER TABLE grants ADD COLUMN final_report_summary TEXT;
ALTER TABLE grants ADD COLUMN further_information TEXT;
ALTER TABLE grants ADD COLUMN panel_history TEXT;

ALTER TABLE organisations ADD COLUMN website TEXT;

CREATE TABLE sectors (
    id                          INTEGER,
    name                        TEXT,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(id ASC),
    UNIQUE(name)
);

CREATE TABLE grants_sectors (
    grant_id                    INTEGER,
    sector_id                   INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    FOREIGN KEY(grant_id) REFERENCES grants(id),
    FOREIGN KEY(sector_id) REFERENCES sectors(id)
);

CREATE TABLE research_topics (
    id                          INTEGER,
    parent_id                   INTEGER,
    name                        TEXT,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(id ASC),
    FOREIGN KEY(parent_id) REFERENCES research_topics(id),
    UNIQUE(parent_id,name)
);

CREATE TABLE grants_research_topics (
    grant_id                    INTEGER,
    research_topic_id           INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    FOREIGN KEY(grant_id) REFERENCES grants(id),
    FOREIGN KEY(research_topic_id) REFERENCES research_topics(id)
);

CREATE TABLE grants_project_partners (
    grant_id                    INTEGER,
    organisation_id             INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    FOREIGN KEY(grant_id) REFERENCES grants(id),
    FOREIGN KEY(organisation_id) REFERENCES organisations(id)
);

CREATE TABLE grants_investigators (
    grant_id                    INTEGER,
    person_id                   INTEGER,
    type                        TEXT,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(grant_id,person_id,type),
    FOREIGN KEY(grant_id) REFERENCES grants(id),
    FOREIGN KEY(person_id) REFERENCES people(id)
);

CREATE TABLE grants_related_grants (
    grant_id                    INTEGER,
    related_grant_id            INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(grant_id,related_grant_id),
    FOREIGN KEY(grant_id) REFERENCES grants(id),
    FOREIGN KEY(related_grant_id) REFERENCES grants(id)
);


