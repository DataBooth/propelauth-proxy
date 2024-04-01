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
    st.error(error_msg)
    logger.error(error_msg)
    st.stop()

with st.sidebar:
    st.link_button("Account", auth.get_account_url(), use_container_width=True)

login_msg = f"Logged in as {user.email} with user ID {user.user_id}"
st.text(login_msg)
logger.info(login_msg)
