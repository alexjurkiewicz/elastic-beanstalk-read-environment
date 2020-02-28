#!/usr/bin/env python3

import json
import os
import sys

import boto3


def debug(msg):
    print(f"::debug::{msg}")


def fail(msg):
    print(f"::error ::{msg}")
    sys.exit(1)


def set_output(key, val):
    print(f"Set output {key}={val}")
    print(f"::set-output name={key}::{val}")


def load_config():
    config = {
        "app_name": os.environ.get("INPUT_APPLICATION_NAME"),
        "env_id": os.environ.get("INPUT_ENVIRONMENT_ID"),
        "env_name": os.environ.get("INPUT_ENVIRONMENT_NAME"),
    }
    debug(f"Loaded config: {config}")
    return config


def validate_config(config):
    if not config["app_name"] and not config["env_id"] and not config["env_name"]:
        fail("You must specify at least environment_id or environment_name.")
    if config["env_id"] and (config["env_name"] or config["app_name"]):
        fail(
            "If you specify environment_id, don't specify environment_name or application_name."
        )
    if config["app_name"] and not config["env_name"]:
        fail("If you specify application_name, environment_name is required.")


if __name__ == "__main__":
    CONFIG = load_config()
    validate_config(CONFIG)

    client = boto3.client("elasticbeanstalk")

    describe_environments_params = {}
    if CONFIG["app_name"]:
        describe_environments_params["ApplicationName"] = CONFIG["app_name"]
    if CONFIG["env_id"]:
        describe_environments_params["EnvironmentIds"] = [CONFIG["env_id"]]
    if CONFIG["env_name"]:
        describe_environments_params["EnvironmentNames"] = [CONFIG["env_name"]]
    debug(f"Request params: {describe_environments_params}")
    response = client.describe_environments(**describe_environments_params)
    debug(f"Response: {response}")

    if len(response["Environments"]) > 1:
        apps = ",".join(e["ApplicationName"] for e in response["environments"])
        fail(f"Found multiple matching environments in applications: {apps}")

    if not response["Environments"]:
        fail("Found no matching environment.")

    env = response["Environments"][0]

    set_output("name", env["EnvironmentName"])
    set_output("id", env["EnvironmentId"])
    set_output("application", env["ApplicationName"])
    set_output("version", env["VersionLabel"])
