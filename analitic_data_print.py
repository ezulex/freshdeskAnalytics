import db_connection as db_c
import app_logger
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('ggplot')
logger = app_logger.get_logger(__name__)


def print_avg_speed_by_priority(priority):
    df = db_c.create_df_avg_speed_by_priority(priority)
    df.plot(x="date_month", y="avg_resolving_time")
    plt.savefig(f'print_avg_speed_by_priority-{priority}.png')
    logger.info(f"Figure print_avg_speed_by_priority-{priority} saved")
    plt.show()
    logger.info(f"Figure print_avg_speed_by_priority-{priority} showed")


def print_lines_distrib():
    df = db_c.create_df_lines_distrib()
    plt.pie(df["tickets_count"], labels=df["group_name"])
    plt.savefig('lines_distrib.png')
    logger.info("Figure lines_distrib saved")
    plt.show()
    logger.info("Figure lines_distrib showed")
