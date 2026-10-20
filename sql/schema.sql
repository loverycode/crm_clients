
DROP TABLE IF EXISTS deals;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS managers;
DROP TABLE IF EXISTS clients;

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Новый',
    created TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    position TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    manager_id INTEGER NOT NULL,
    contact_id INTEGER,
    amount REAL NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    stage TEXT NOT NULL DEFAULT 'Открыта',
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (manager_id) REFERENCES managers(id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);