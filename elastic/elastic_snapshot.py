import datetime
import sys
import requests
import os

BACKUP_PATH = "/home/ubuntu/elastic_data_backup"

if not os.path.exists(BACKUP_PATH):
    print "Please create following path with 777 permission.\n{}".format(BACKUP_PATH)
    exit(1)

REPO_CREATE_BODY = """
                {
                    "type": "fs",
                    "settings": {
                        "location": "%s",
                        "compress": true
                    }
                }
                """ % (BACKUP_PATH)

BACKUP_NAME = datetime.date.today().strftime("%d_%b_%Y").lower()

REPO_CREATE_URL = "/_snapshot/elastic_backup/"

CREATE_BACKUP = "/_snapshot/elastic_backup/{}?wait_for_completion=true".format(BACKUP_NAME)

SEARCH_URL = "http://172.16.0.176:9200"


def load_cofig(server_type='local'):
    global SEARCH_URL
    if server_type.lower() == 'beta':
        SEARCH_URL = "http://172.30.0.152:9200"
    elif server_type.lower() == 'staging':
        SEARCH_URL = "http://172.30.0.111:9200"
    elif server_type.lower() == 'local':
        SEARCH_URL = "http://172.16.0.176:9200"
    else:
#         print "Incorrect serrver type.Options are staging,beta or local"
#         exit(1)
        SEARCH_URL = "http://172.16.0.176:9200"


def check_config():
    """
    """
    if len(sys.argv) <= 1:
        print "Please supply server type i.e staging,beta or local"
        exit(1)
    server_type = sys.argv[1] if len(sys.argv) > 1 else 'local'
    load_cofig(server_type)
    print "SERVER TYPE is ".format(server_type)


def create_backup(initial_run=False):
    if not initial_run:
        check_config()
    print "Creating Backup"
    req = requests.put(SEARCH_URL + CREATE_BACKUP)
    if req.status_code not in [200, 201]:
        print "Unable to create backup"
        print req.content


def first_time_run():
    print "Loading configuration"
    check_config()
    print "Creating repository for backup"
    req = requests.put(SEARCH_URL + REPO_CREATE_URL, data=REPO_CREATE_BODY)
    if req.status_code not in [200, 201]:
        print "Unable to create repository for elastic backup"
        print req.content
    else:
        create_backup(initial_run=True)


if __name__ == "__main__":
    first_time_run()
