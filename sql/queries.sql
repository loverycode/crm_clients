         


SELECT id, name, status, created
FROM clients
ORDER BY name;


SELECT id, title, amount, stage
FROM deals
ORDER BY amount DESC;


SELECT id, name, created
FROM clients
WHERE status = 'В работе';


SELECT id, title, amount
FROM deals
WHERE stage = 'Открыта';

SELECT id, title, amount
FROM deals
WHERE amount BETWEEN 50000 AND 200000
ORDER BY amount;

SELECT id, name
FROM clients
WHERE name LIKE '%ООО%';


SELECT
    deals.id,
    deals.title,
    deals.amount,
    deals.stage,
    clients.name AS client_name,
    managers.name AS manager_name,
    contacts.name AS contact_name
FROM deals
JOIN clients ON deals.client_id = clients.id
JOIN managers ON deals.manager_id = managers.id
LEFT JOIN contacts ON deals.contact_id = contacts.id
ORDER BY deals.id;


SELECT
    contacts.id,
    contacts.name AS contact_name,
    contacts.phone,
    contacts.position,
    clients.name AS client_name
FROM contacts
JOIN clients ON contacts.client_id = clients.id
ORDER BY clients.name, contacts.name;


SELECT COUNT(*) AS clients_count FROM clients;

SELECT SUM(amount) AS total_amount FROM deals;


SELECT AVG(amount) AS avg_amount FROM deals;


SELECT COUNT(*) AS open_deals_count
FROM deals
WHERE stage = 'Открыта';

              GROUP BY           

SELECT
    clients.name AS client_name,
    COUNT(deals.id) AS deals_count
FROM clients
LEFT JOIN deals ON clients.id = deals.client_id
GROUP BY clients.id, clients.name
ORDER BY deals_count DESC;

SELECT
    managers.name AS manager_name,
    COUNT(deals.id) AS deals_count
FROM managers
LEFT JOIN deals ON managers.id = deals.manager_id
GROUP BY managers.id, managers.name
ORDER BY deals_count DESC;

SELECT
    stage,
    COUNT(*) AS deals_count,
    SUM(amount) AS total_amount
FROM deals
GROUP BY stage
ORDER BY total_amount DESC;

              HAVING           

SELECT
    managers.name AS manager_name,
    COUNT(deals.id) AS deals_count
FROM managers
JOIN deals ON managers.id = deals.manager_id
GROUP BY managers.id, managers.name
HAVING COUNT(deals.id) > 1;


SELECT
    managers.id,
    managers.name,
    managers.email,
    COUNT(deals.id) AS open_count
FROM managers
LEFT JOIN deals ON managers.id = deals.manager_id AND deals.stage = 'Открыта'
GROUP BY managers.id, managers.name, managers.email
HAVING COUNT(deals.id) < 5
ORDER BY open_count;

              Сделка по ID с JOIN           


SELECT
    deals.id,
    deals.title,
    deals.amount,
    deals.stage,
    deals.manager_id,
    clients.name AS client_name,
    managers.name AS manager_name,
    contacts.name AS contact_name
FROM deals
JOIN clients ON deals.client_id = clients.id
JOIN managers ON deals.manager_id = managers.id
LEFT JOIN contacts ON deals.contact_id = contacts.id
WHERE deals.id = ?;