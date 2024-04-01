# This code uses the Auth class from the `propelauth` module to authenticate a user 
# and display their account information in a Streamlit application.
# It requires two environment variables, `PROPEL_TRY_AUTH_URL` and `PROPEL_TRY_API_KEY`, 
# which are loaded from a .env file using the load_dotenv() function.

import os

import streamlit as st
from dotenv import load_dotenv
from loguru import logger
from try_propelauth.propelauth import Auth

load_dotenv()

auth = Auth(os.environ["PROPEL_TRY_AUTH_URL"], os.environ["PROPEL_TRY_API_KEY"])   # Variables defined in .env

logger.info("Starting...")
user = auth.get_user()

if user is None:
    error_msg = "Unauthorized (auth by https://www.PropelAuth.com)"
    logger.error(error_msg)
    st.error(error_msg)
    st.stop()

login_msg = f"Logged in as {user.email} with user ID {user.user_id}"
logger.info(login_msg)
st.text(login_msg)

with st.sidebar:
    st.link_button("Account", auth.get_account_url(), use_container_width=True)