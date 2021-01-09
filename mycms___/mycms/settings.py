# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import os

from environs import Env

env = Env()
env.read_env()

# ENV = env.str("FLASK_ENV", default="production")
# DEBUG = ENV == "development"
# SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
# SECRET_KEY = env.str("SECRET_KEY")
# UPLOAD_DIR = env.str("UPLOADED_IMAGES_DEST") if env.str("UPLOADED_IMAGES_DEST") else '/uploads'
# UPLOADED_IMAGES_DEST = os.path.dirname(os.path.realpath(__file__)) + UPLOAD_DIR
# SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
# BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
# DEBUG_TB_ENABLED = DEBUG
# DEBUG_TB_INTERCEPT_REDIRECTS = False
# CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# AVAILABLE_ADMIN_SETTINGS = [('git_repo', "Git Repo"), ('stripe_key', "Stripe Key")]
# REVERSE_PROXY = env.int("REVERSE_PROXY") if env.int("REVERSE_PROXY") else 0
# REVERSE_PROXY_PATH = env.str("REVERSE_PROXY_PATH") if env.str("REVERSE_PROXY_PATH") else '/'



###########################################################

ENV = "production"
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://ubuntu:password_ubuntu@localhost/sweet_cms"
SECRET_KEY = "thisissecretkey"
UPLOAD_DIR = '/uploads'
UPLOADED_IMAGES_DEST = os.path.dirname(os.path.realpath(__file__)) + UPLOAD_DIR
SEND_FILE_MAX_AGE_DEFAULT = 0
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
AVAILABLE_ADMIN_SETTINGS = [('git_repo', "Git Repo"), ('stripe_key', "Stripe Key")]
REVERSE_PROXY = 0
REVERSE_PROXY_PATH = '/'
