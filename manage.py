#!/usr/bin/env python
import os
import sys
import environ


root = environ.Path(__file__) - 1  # one folder back (/manage - 3 = /)
env = environ.Env()
environ.Env.read_env(env_file=root('.env'))  # reading .env file


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", env('DJANGO_SETTINGS_MODULE'))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
