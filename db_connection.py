import sqlite3
import pandas as pd
import app_logger
import fd_api_connection as fd_api_c
import df_creation as df_c
import os
from dotenv import load_dotenv

logger = app_logger.get_logger(__name__)
load_dotenv()
db_path = os.environ.get("DB_PATH")
try:
    con = sqlite3.connect(db_path, timeout=10)
except (sqlite3.Error, sqlite3.Warning) as e:
    logger.error(f"Can`t connect to the DB. {e}")
else:
    logger.info("Conection to the DB successful")
cur = con.cursor()


def fill_db():
    df_tickets = df_c.get_tickets_dataframe(fd_api_c.get_all_tickets())
    df_groups = df_c.get_groups_dataframe(fd_api_c.get_all_groups())
    df_statuses = df_c.get_statuses_dataframe()
    df_sources = df_c.get_sources_dataframe()
    df_priorities = df_c.get_priorities_dataframe()

    df_tickets.to_sql(con=con, name='tickets', index=False, if_exists='replace')
    df_groups.to_sql(con=con, name='groups', index=False, if_exists='replace')
    df_statuses.to_sql(con=con, name='statuses', index=False, if_exists='replace')
    df_sources.to_sql(con=con, name='sources', index=False, if_exists='replace')
    df_priorities.to_sql(con=con, name='priorities', index=False, if_exists='replace')


def create_df_avg_speed_by_priority(priority):
    if priority == 'urgent':
        df = pd.read_sql_query(
            "SELECT "
            "strftime('%Y', t.created_at) AS date_year, "
            "strftime('%m', t.created_at) AS date_month, "
            "p.priority_name, "
            "avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer)) AS avg_resolving_time "
            "FROM tickets t "
            "INNER JOIN priorities p ON p.priority_id = t.priority_id "
            "WHERE t.resolved_at IS NOT NULL AND p.priority_id = 4 AND t.created_at BETWEEN '2023-03-01' AND '2023-12-31' "
            "GROUP BY  date_year, date_month, p.priority_name "
            "ORDER BY date_year, date_month, p.priority_name",
            con)
    elif priority == 'high':
        df = pd.read_sql_query(
            "SELECT "
            "strftime('%Y', t.created_at) AS date_year, "
            "strftime('%m', t.created_at) AS date_month, "
            "p.priority_name, "
            "avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer)) AS avg_resolving_time "
            "FROM tickets t "
            "INNER JOIN priorities p ON p.priority_id = t.priority_id "
            "WHERE t.resolved_at IS NOT NULL AND p.priority_id = 3 AND t.created_at BETWEEN '2023-03-01' AND '2023-12-31' "
            "GROUP BY  date_year, date_month, p.priority_name "
            "ORDER BY date_year, date_month, p.priority_name",
            con)
    elif priority == 'medium':
        df = pd.read_sql_query(
            "SELECT "
            "strftime('%Y', t.created_at) AS date_year, "
            "strftime('%m', t.created_at) AS date_month, "
            "p.priority_name, "
            "avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer)) AS avg_resolving_time "
            "FROM tickets t "
            "INNER JOIN priorities p ON p.priority_id = t.priority_id "
            "WHERE t.resolved_at IS NOT NULL AND p.priority_id = 2 AND t.created_at BETWEEN '2023-03-01' AND '2023-12-31' "
            "GROUP BY  date_year, date_month, p.priority_name "
            "ORDER BY date_year, date_month, p.priority_name",
            con)
    elif priority == 'low':
        df = pd.read_sql_query(
            "SELECT "
            "strftime('%Y', t.created_at) AS date_year, "
            "strftime('%m', t.created_at) AS date_month, "
            "p.priority_name, "
            "avg(cast((julianday(t.resolved_at) - julianday(t.created_at)) * 24 As Integer)) AS avg_resolving_time "
            "FROM tickets t "
            "INNER JOIN priorities p ON p.priority_id = t.priority_id "
            "WHERE t.resolved_at IS NOT NULL AND p.priority_id = 1 AND t.created_at BETWEEN '2023-03-01' AND '2023-12-31' "
            "GROUP BY  date_year, date_month, p.priority_name ORDER BY date_year, date_month, p.priority_name",
            con)
    else:
        return "Invalid argument"
    return df


def create_df_lines_distrib():
    df = pd.read_sql_query(
        "WITH tickets_count_by_month AS "
        "( SELECT "
        "strftime('%Y', t.created_at) AS date_year, "
        "strftime('%m', t.created_at) AS date_month, "
        "g.group_name AS group_name, "
        "COUNT(t.ticket_id) AS tickets_count "
        "FROM tickets t "
        "INNER JOIN groups g ON g.group_id = t.group_id AND g.group_id IN (101000345992, 101000350471, 101000364483) "
        "WHERE t.created_at BETWEEN '2023-03-01' AND '2023-12-31' "
        "GROUP BY date_year, date_month, g.group_name ) "
        "SELECT "
        "group_name, "
        "AVG(tickets_count) AS tickets_count "
        "FROM tickets_count_by_month "
        "GROUP BY group_name",
        con)
    return df
