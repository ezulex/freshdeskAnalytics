-- Проверка гипотезы по снижению срока решения с сентября
SELECT
    strftime('%Y', t.created_at) AS date_year,
	strftime('%m', t.created_at) AS date_month,
    p.priority_name,
    avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer)) AS avg_resolving_time
FROM tickets t
INNER JOIN priorities p ON p.priority_id = t.priority_id
WHERE t.resolved_at IS NOT NULL  AND t.created_at BETWEEN '2023-03-01' AND '2023-12-31'
GROUP BY  date_year, date_month, p.priority_name
ORDER BY date_year, date_month, p.priority_name;


-- Распределение задач по линиям
WITH tickets_count_by_month AS (
    SELECT
        strftime('%Y', t.created_at) AS date_year,
        strftime('%m', t.created_at) AS date_month,
        g.group_name AS group_name,
        COUNT(t.ticket_id) AS tickets_count
    FROM tickets t
    INNER JOIN groups g ON g.group_id = t.group_id AND g.group_id IN (101000345992, 101000350471, 101000364483)
    WHERE t.created_at BETWEEN '2023-03-01' AND '2023-12-31'
    GROUP BY date_year, date_month, g.group_name
)
SELECT
    group_name,
    AVG(tickets_count) AS tickets_count,
    ROUND(AVG(tickets_count) / SUM(AVG(tickets_count)) OVER () * 100) AS percents
FROM tickets_count_by_month
GROUP BY group_name


-- Топ-5 самых долгих задач по линиям
SELECT
    *
FROM (
    SELECT
        g.group_name,
        t.category,
        t.subcategory,
        ROUND(avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer))) AS avg_resolving_time,
        ROW_NUMBER() OVER (PARTITION BY g.group_name ORDER BY avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer)) DESC) AS rating
    FROM tickets t
    INNER JOIN groups g ON g.group_id = t.group_id AND g.group_id IN (101000345992, 101000350471)
    WHERE t.resolved_at IS NOT NULL  AND t.created_at BETWEEN '2023-03-01' AND '2023-12-31'
    GROUP BY g.group_name, t.category, t.subcategory
    ) AS category_rating
WHERE category_rating.rating <= 5