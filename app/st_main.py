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

APP_TITLE = "Try PropelAuth"
APP_ICON = "🔐"
APP_LAYOUT = "centered"
APP_SIDEBAR_INITIAL = "expanded"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state=APP_SIDEBAR_INITIAL,
)

# Authentication (variables defined in .env and loaded by dotenv)

logger.info("Authenticating...")
auth = Auth(os.environ["PROPEL_TRY_AUTH_URL"], os.environ["PROPEL_TRY_API_KEY"])

user = auth.get_user()
if user is None:
    error_msg = "Unauthorized (auth by https://www.PropelAuth.com)"
    logger.error(error_msg)
    st.error(error_msg)
    st.stop()

# Main app (once authenticated)

st.title("Try PropelAuth")
st.subheader("Demo app")

login_msg = f"Logged in as **{user.email}** with user ID: `{user.user_id}`"
logger.info(login_msg.replace("*", "").replace("`", ""))
st.markdown(login_msg)

with st.sidebar:
    st.link_button("My account settings", auth.get_account_url(), use_container_width=True)
