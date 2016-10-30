Introduction
------------
This document adheres to the specifications outlined in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

Database
--------
- In general, lowercase_delimited_by_underscores **should** be used.
- Tables **must** be named with the plural form of their entity.
- Tables **must** have a primary key.
- Primary keys **should** be surrogate keys.
```
-- YES
CREATE TABLE users (
    id              serial                  PRIMARY KEY,
    email_address   varchar(64) NOT NULL    UNIQUE
);

-- No
CREATE TABLE users (
    email_address   varchar(64)             PRIMARY KEY
);
```
- Primary keys **must** be named "id".
- Foreign keys **must** be named <table_name> + "_id".
```
-- YES
CREATE TABLE parents (
    id          serial              PRIMARY KEY,
    children_id int     NOT NULL    REFERENCES children (id)
);
```
- Tables **must** include metadata fields.
```
-- YES
CREATE TABLE users (
    id              serial                  PRIMARY KEY,
    email_address   varchar(64) NOT NULL    UNIQUE
    created_at      timestamp   NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    created_by      int         NOT NULL,
    updated_at      timestamp,
    updated_by      int
);

-- No
CREATE TABLE users (
    id              serial                  PRIMARY KEY,
    email_address   varchar(64) NOT NULL    UNIQUE
);
```
- Tables describing one-to-many relationships **should** be named <parent_table>_<child_table>.
- Tables describing many-to-many relationships **must** start a new naming convention hierarchy.
```
/* There are sibling A entities in the siblings_a table.
 * There are sibling B entities in the siblings_b table.
 */

-- YES
CREATE TABLE foo (
    id              serial              PRIMARY KEY,
    siblings_a_id   int     NOT NULL    REFERENCES siblings_a (id),
    siblings_b_id   int     NOT NULL    REFERENCES siblings_b (id),
);

-- No
CREATE TABLE siblings_a_siblings_b (
    id              serial              PRIMARY KEY,
    siblings_a_id   int     NOT NULL    REFERENCES siblings_a (id),
    siblings_b_id   int     NOT NULL    REFERENCES siblings_b (id),
);
```
- Column constraints **should** trend towards being restrictive.
- Data type constraints **should** trend towards being more relaxed.