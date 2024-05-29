import argparse
import json
import logging
import requests
import os,sys
import time
import uuid


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

    def create_user(self):
        """create_user"""
        fh = open(os.environ['GITHUB_OUTPUT'], 'a')
        print("Create user module...")
        print("User name", self.user_name)
        fh.write("inside...User name: " + self.user_name + "\n")
        fh.close()


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
    ma = MongodbUser(args)

if __name__ == "__main__":
    main()