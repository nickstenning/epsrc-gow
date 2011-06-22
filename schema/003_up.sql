-- Relax foreign key constraint on related_grant_id -- we don't necessarily
-- have it but it's stupid to throw away the information.
UPDATE schema SET version=3;

CREATE TABLE grants_related_grants_new (
    grant_id                    INTEGER,
    related_grant_id            INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(grant_id,related_grant_id),
    FOREIGN KEY(grant_id) REFERENCES grants(id)
);

INSERT INTO grants_related_grants_new
(grant_id, related_grant_id, created_at, modified_at)
SELECT grant_id, related_grant_id, created_at, modified_at
FROM grants_related_grants;

DROP TABLE grants_related_grants;
ALTER TABLE grants_related_grants_new RENAME TO grants_related_grants;