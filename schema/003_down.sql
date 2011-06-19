-- Since this migration *reintroduces* a FK constraint that was relaxed by the
-- "up" migration, it is very likely that you'll hit foreign key constraint
-- errors while running it.

-- I've enabled this so that you KNOW you're doing bad things if you reverse
-- this migration.
PRAGMA foreign_keys=on;

CREATE TABLE grants_related_grants_old (
    grant_id                    INTEGER,
    related_grant_id            INTEGER,
    created_at                  TEXT, -- DATETIME
    modified_at                 TEXT, -- DATETIME
    PRIMARY KEY(grant_id,related_grant_id),
    FOREIGN KEY(grant_id) REFERENCES grants(id)
    FOREIGN KEY(related_grant_id) REFERENCES grants(id)
);

INSERT INTO grants_related_grants_old
(grant_id, related_grant_id, created_at, modified_at)
SELECT grant_id, related_grant_id, created_at, modified_at
FROM grants_related_grants;

DROP TABLE grants_related_grants;
ALTER TABLE grants_related_grants_old RENAME TO grants_related_grants;