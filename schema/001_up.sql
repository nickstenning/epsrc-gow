CREATE TABLE schema (
    version                     INTEGER
);
INSERT INTO schema (version) values (1);

CREATE TABLE grants (
    id                          TEXT,
    title                       TEXT,
    value                       INTEGER,
    principal_investigator_id   INTEGER,
    department_id               INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(id),
    FOREIGN KEY(principal_investigator_id) REFERENCES people(id),
    FOREIGN KEY(department_id) REFERENCES departments(id)
);

CREATE TABLE organisations (
    id                          INTEGER,
    name                        TEXT,
    latlng                      TEXT,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(id)
);

CREATE TABLE departments (
    id                          INTEGER,
    name                        TEXT,
    organisation_id             INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(id),
    FOREIGN KEY(organisation_id) REFERENCES organisations(id)
);

CREATE TABLE people (
    id                          INTEGER,
    name                        TEXT,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(id)
);

