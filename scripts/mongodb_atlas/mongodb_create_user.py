import argparse
import json
import logging
import requests
import sys
import time

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

    def create_user(self, project_name: str):
        """create_user"""
        print("Create user module...")


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


def main():
    args = get_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    ma = MongodbUser(args.env)

if __name__ == "__main__":
    main()