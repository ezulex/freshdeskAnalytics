import json
import time
import requests
import os
import app_logger
from dotenv import load_dotenv

logger = app_logger.get_logger(__name__)
load_dotenv()
base_url = os.environ.get("BASE_URL")
api_key = os.environ.get("FD_API_KEY")
password = os.environ.get("FD_PASS")


def get_all_tickets():
    postfix_url = "/tickets"
    url = base_url + postfix_url

    page = 1
    list_of_tickets_json = []
    while True or page > 1000:
        try:
            once_response = requests.get(url, auth=(api_key, password),
                                         params={'page': page, 'per_page': 100, 'include': 'stats',
                                                 'updated_since': '2023-03-01T00:00:00Z'})
            time.sleep(2)
        except requests.ConnectionError as e:
            logger.error(f"Request to {postfix_url}. {e}")
        except requests.Timeout as e:
            logger.error(f"Request to {postfix_url}. {e}")
        except requests.RequestException as e:
            logger.error(f"Request to {postfix_url}. {e}")
        else:
            if once_response.status_code == 200:
                response = once_response.json()
                if response == []:
                    break
                part_of_tickets_data = json.loads(once_response.content)
                list_of_tickets_json.append(part_of_tickets_data)
                logger.info(
                    f"Request to {postfix_url}, page: {page}. Status code: {once_response.status_code}, data received")
            else:
                logger.error(f"Request to {postfix_url}, page: {page}. Status code: {once_response.status_code}")
        finally:
            page += 1

    return list_of_tickets_json


def get_all_groups():
    postfix_url = "/groups"
    url = base_url + postfix_url
    try:
        all_response = requests.get(url, auth=(api_key, password))
    except requests.ConnectionError as e:
        logger.error(f"Request to {postfix_url}. {e}")
    except requests.Timeout as e:
        logger.error(f"Request to {postfix_url}. {e}")
    except requests.RequestException as e:
        logger.error(f"Request to {postfix_url}. {e}")
    else:
        if all_response.status_code == 200:
            response = all_response.json()
            logger.info(f"Request to {postfix_url}. Status code: {all_response.status_code}, data received")
        else:
            logger.error(f"Request to {postfix_url}. Status code: {all_response.status_code}")
    return response
