import pandas as pd
import dicts
import app_logger

logger = app_logger.get_logger(__name__)


def get_tickets_dataframe(data):
    df_tickets_list = []
    for record in data:
        df_ticket = pd.json_normalize(record)
        df_tickets_list.append(df_ticket)
    df = pd.concat(df_tickets_list)

    main_df = df[["id",
                  "source",
                  "requester_id",
                  "priority",
                  "status",
                  "company_id",
                  "spam",
                  "group_id",
                  "responder_id",
                  "type",
                  "fr_due_by",
                  "due_by",
                  "created_at",
                  "updated_at",
                  "custom_fields.cf_rand76706",
                  "custom_fields.cf_rand289447",
                  "stats.resolved_at"]]

    main_df = main_df.rename(columns={"id": "ticket_id", "source": "source_id", "priority": "priority_id",
                                      "status": "status_id", "custom_fields.cf_rand76706": "category",
                                      "custom_fields.cf_rand289447": "subcategory", "stats.resolved_at": "resolved_at"})
    logger.info("Tickets dataframe created")
    logger.info("Start deleting dublicates")
    main_df.drop_duplicates(['ticket_id'])
    logger.info("Dublicates deleted")
    return main_df


def get_groups_dataframe(data):
    df = pd.DataFrame.from_records(data)
    result_df = df[["id",
                    "name"]]
    result_df = result_df.rename(columns={"id": "group_id", "name": "group_name"})
    logger.info("Groups dataframe created")
    return result_df


def get_statuses_dataframe():
    statuses_dict = dicts.get_statuses_dict()
    result_df = pd.DataFrame(statuses_dict)
    logger.info("Statuses dataframe created")
    return result_df


def get_sources_dataframe():
    sources_dict = dicts.get_sources_dict()
    result_df = pd.DataFrame(sources_dict)
    logger.info("Sources dataframe created")
    return result_df


def get_priorities_dataframe():
    priority_dict = dicts.get_priorities_dict()
    result_df = pd.DataFrame(priority_dict)
    logger.info("Priorities dataframe created")
    return result_df
