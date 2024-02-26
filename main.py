import app_logger
import db_connection as db_c
import analitic_data_print as an_p

if __name__ == '__main__':
    logger = app_logger.get_logger(__name__)

    logger.info("Start app")
    logger.info("Start filling DB")
    db_c.fill_db()
    logger.info("End filling DB")
    logger.info("Start print data")
    an_p.print_avg_speed_by_priority('urgent')
    an_p.print_avg_speed_by_priority('high')
    an_p.print_avg_speed_by_priority('medium')
    an_p.print_avg_speed_by_priority('low')
    an_p.print_lines_distrib()
    logger.info("End print data")
    logger.info("End app")


