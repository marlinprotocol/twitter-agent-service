import json
from os import getenv, path
from datetime import datetime
from browser_setup import setup_browser
from email_actions import login_into_email, reset_email_password
from twitter_actions import attempt_twitter_login, login_and_reset_twitter_password, generate_x_api_keys, generate_x_access_token_secret, twitter_account_verification

async def generate_keys_and_access_tokens_actions(kms_generated_password):
    # Get environment variables
    user_provided_password = getenv("USER_PASSWORD")
    username = getenv("USERNAME")
    user_email = getenv("USER_EMAIL")
    user_email_password = getenv("USER_EMAIL_PASSWORD")
    x_app_name = getenv("X_APP_NAME")

    # Initialize browser
    browser = await setup_browser()

    # Stage 1: Try to login with KMS generated password, if failed try to reset the password 
    if not await login_into_email(browser, user_email, kms_generated_password):
        print("Failed to login with KMS generated password")
        if not await reset_email_password(browser, user_email, user_email_password, kms_generated_password):
            print("Failed to reset email password and recovery code")
            return None, None, None
        print("Email password reset and recovery code updated successfully")
    else:
        print("Logged in with KMS generated password")

    # Stage 2: Attempt twitter login or password reset
    if not await attempt_twitter_login(browser, username, user_email, kms_generated_password):
        print("Failed to login into twitter with KMS password, attempting with user password")
        if await login_and_reset_twitter_password(browser, username, user_email, user_provided_password, kms_generated_password):
            print(f"Password reset successful, new password: {kms_generated_password}")
        else:
            print("Password reset failed")
            return None, None, None
    print("Successfully logged in into twitter with KMS password")

    # Stage 3: Fetch API keys from X developer dashboard
    api_key_result = await generate_x_api_keys(browser, username, user_email, kms_generated_password, x_app_name)
    api_keys = json.loads(api_key_result) if api_key_result else None

    # Stage 4: Fetch access token from X developer dashboard
    access_token_result = await generate_x_access_token_secret(browser, username, user_email, kms_generated_password, x_app_name)
    access_tokens = json.loads(access_token_result) if access_token_result else None
    timestamp = str(datetime.now())
    # Save the keys and tokens to a file
    if api_keys and access_tokens:
        with open("/app/shared_data/keys.json", "w") as f:
            json.dump({"api_keys": api_keys, "access_tokens": access_tokens, "timestamp": timestamp}, f)

    return api_keys, access_tokens, timestamp

async def verify_encumbrance_actions(kms_derived_password):
    # Get environment variables
    kms_generated_password = kms_derived_password
    username = getenv("USERNAME")
    user_email = getenv("USER_EMAIL")
    x_app_name = getenv("X_APP_NAME")

    # Initialize browser
    browser = await setup_browser()

    # Stage 1: Try to login into email account with KMS generated password
    if not await login_into_email(browser, user_email, kms_generated_password):
        print("Failed to login into email account with KMS generated password")
        return False
    else:
        print("Successfully logged in into email account with KMS generated password")

    # Stage 2: Attempt twitter login and verify email id
    if not await twitter_account_verification(browser, username, user_email, kms_generated_password, x_app_name):
        print("Failed to verify if the twitter account is encumbered")
        return False
    else:
        print("Successfully verified twitter account is encumbered")

    return True