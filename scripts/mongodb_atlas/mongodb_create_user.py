import argparse
import json
import logging
import requests
import os,sys
import time
import uuid
from requests.auth import HTTPDigestAuth

logging.basicConfig(level=logging.INFO, format="[%(levelname)s][%(funcName)s] %(message)s")


class MongodbUser:
    def __init__(self, env):
        """Initialize Class"""
        self.app_name = env.app_name
        self.env_name = env.env_name
        self.db_name = env.db_name
        self.user_name = env.user_name
        self.user_password = env.user_password
        self.user_role = env.user_role
        self.atlas_pub_key = os.environ["TF_VAR_mongodb_atlas_api_pub_key"]
        self.atlas_pri_key = os.environ["TF_VAR_mongodb_atlas_api_pri_key"]
        self.atlas_org_id = os.environ["TF_VAR_mongodb_atlas_org_id"]
        self.atlas_main_url = "https://cloud.mongodb.com/api/atlas/v2"
        self.headers =  {"Content-Type":"application/json", "Accept":"application/vnd.atlas.2023-02-01+json"}
        self.project_name = f"mng-{self.app_name}-{self.env_name}-project"
        self.cluster_name = f"mng-{self.app_name}-{self.env_name}-cluster"
        self.groupId = ''


    def create_user(self):
        """create_user"""
        logging.info(f"Create user module..")
        logging.info(f"User Name: {self.user_name}")

        atlas_url = self.atlas_main_url + "/groups"
        response = requests.get(atlas_url, auth=HTTPDigestAuth(self.atlas_pub_key, self.atlas_pri_key) , headers=self.headers )
        r = response.content.decode("utf-8")
        logging.info(f"Getting project id")
        data = json.loads(r)
        projects = data.get('results', [])
        for rec in projects:
            if rec.get('name', '') == self.project_name:
                print(rec)
                self.groupId = rec.get('id', '')
                print('Project name:', rec.get('name', ''))
                print('Group ID: ', rec.get('id', ''))

        #### Create user
        #https://cloud.mongodb.com/api/atlas/v2/groups/{groupId}/databaseUsers
        atlas_url = f"{self.atlas_main_url}/groups/{self.groupId}/databaseUsers"
        if self.user_role == "read":
            roles = [
                {
                    "databaseName": self.db_name,
                    "roleName": "read"
                },
                {
                    "databaseName": "admin",
                    "roleName": "clusterMonitor"
                }
            ]
        elif self.user_role == "readWrite":
            roles = [
                {
                    "databaseName": self.db_name,
                    "roleName": "readWrite"
                }
            ]

        payload = {
            "databaseName": "admin",
            "groupId": self.groupId,
            "password": self.user_password,
            "roles": roles,
            "scopes": [
                {
                "name": self.cluster_name,
                "type": "CLUSTER"
                }
            ],
            "username": self.user_name
        }
        response = requests.post(atlas_url, auth=HTTPDigestAuth(self.atlas_pub_key, self.atlas_pri_key) , headers=self.headers, json=payload )
        logging.info(f"User created with responce.. {response.json()}")



def get_args():
    parser = argparse.ArgumentParser(description="MongoDB Atlas User Creation Workflow")
    parser.add_argument("--env_name", required=True, help="Life cycle Name")
    parser.add_argument("--db_name", required=True, help="DB Name")
    parser.add_argument("--app_name", required=True, help="App Name")
    parser.add_argument("--user_name", required=True, help="User Name")
    parser.add_argument("--user_role", required=True, help="User Role")
    parser.add_argument("--user_password", required=True, help="User Password")
    args = parser.parse_args()
    return args


def set_output(msg):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{msg}', file=fh)


def main():
    args = get_args()
    ma = MongodbUser(args).create_user()

if __name__ == "__main__":
    main()