import asyncio
from os import getenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserConfig, Browser
from typing import Tuple

async def setup_browser() -> Browser:
    config = BrowserConfig(
        headless=False,
        disable_security=True
    )
    return Browser(config=config)

async def login_into_email(
    browser: Browser, 
    user_email: str, 
    user_email_password: str, 
    kms_generated_password: str
) -> bool:
    agent_script = f"""
    1. Visit https://app.tuta.com/login and enter the email {user_email} and password {kms_generated_password} and click on Log in.
    2. If you are able to login into the account, return message 'Logged in with KMS generated password'.
    """
    agent = Agent(browser=browser, task=agent_script, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    action_results = result.action_results()
    final_result = action_results[-1].success
    return final_result

async def reset_email_password(
    browser: Browser, 
    user_email: str, 
    user_email_password: str, 
    kms_generated_password: str
) -> bool:
    agent_script = f"""
    1. Visit https://app.tuta.com/login and enter the email {user_email} and password {user_email_password} and click on Log in password.
    2. On the bottom-left hand side of the homepage click on the settings icon.
    3. On the settings menu page click on the edit button next to the password field.
    4. Enter the old password {user_email_password} and enter the {kms_generated_password} in the set password and repeat password field and after that click on Ok button.
    5. Below the Password field there is a recovery code field, click on the edit button and click on update button.
    6. After clicking on update button enter the {kms_generated_password} and click on Ok.
    7. Once the recovery pop-up shows up, click on the Ok button.
    8. If all the steps are done successfully, return message 'Email password reseted and recovery code updated.'
    """
    agent = Agent(browser=browser, task=agent_script, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    action_results = result.action_results()
    final_result = action_results[-1].success
    return final_result

async def attempt_twitter_login(
    browser: Browser, 
    username: str, 
    user_email: str, 
    kms_generated_password: str
) -> bool:
    agent_script = f"""
    1. Visit https://x.com and click on Sign in, enter username {username}, on next screen enter the password {kms_generated_password} (While entering the password, make sure to click on show password button on the right of the password field).
    2. If while login it asks for email or phone no for verification, enter this {user_email} and click on next.
    3. If login is successful with kms_generated_password, return the message 'Login successful with KMS password' and **IMMEDIATELY STOP EXECUTION HERE**.
    4. If login fails, return the message 'Login failed with KMS password'.
    """
    agent = Agent(browser=browser, task=agent_script, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    action_results = result.action_results()
    final_result = action_results[-1].success
    return final_result

async def login_and_reset_twitter_password(
    browser: Browser, 
    username: str, 
    user_email: str, 
    user_provided_password: str,
    kms_generated_password: str
) -> bool:
    agent_script = f"""
    1. Visit https://x.com and click on Sign in, enter username {username}, on next screen enter the password {user_provided_password} (While entering the password, make sure to click on show password button on the right of the password field).
    2. If while login it asks for email, enter this {user_email} and click on next.
    3. If login is successful with user_provided_password, proceed to reset the password.
    4. Click on more on left hand side and click on settings and privacy (do it in the same tab after login, don't redirect to something else).
    5. Click on your account and after that click on change your password.
    6. Enter the current password {user_provided_password} and then enter the new password {kms_generated_password} and confirm it and click on save.
    7. Return the message 'Password reset successful'.
    """
    agent = Agent(browser=browser, task=agent_script, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    action_results = result.action_results()
    final_result = action_results[-1].success
    return final_result

async def main():
    # Get environment variables
    kms_generated_password = getenv("KMS_GENERATED_PASSWORD")
    user_provided_password = getenv("USER_PASSWORD")
    username = getenv("USERNAME")
    user_email = getenv("USER_EMAIL")
    user_email_password = getenv("USER_EMAIL_PASSWORD")

    # Initialize browser
    browser = await setup_browser()

    # Stage 1: Try to login with KMS generated password, if failed try to reset the password 
    if not await login_into_email(browser, user_email, user_email_password, kms_generated_password):
        print("Failed to login with KMS generated password")
        if not await reset_email_password(browser, user_email, user_email_password, kms_generated_password):
            print("Failed to reset email password and recovery code")
            return
        print("Email password reset and recovery code updated successfully")
    else:
        print("Logged in with KMS generated password")

    # Stage 2: Attempt twitter login
    if await attempt_twitter_login(browser, username, user_email, kms_generated_password):
        print("Successfully logged in into twitter with KMS password")
        return

    print("Failed to login into twitter with KMS password, attempting with user password")

    # Stage 3: Login with user password and reset
    if await login_and_reset_twitter_password(browser, username, user_email, user_provided_password, kms_generated_password):
        print(f"Password reset successful, new password: {kms_generated_password}")
    else:
        print("Password reset failed")

if __name__ == "__main__":
    asyncio.run(main())