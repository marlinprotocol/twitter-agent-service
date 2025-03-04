import asyncio

from os import getenv
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig
from browser_use import Browser


async def main():
    kms_generated_password = getenv("KMS_GENERATED_PASSWORD")
    user_provided_password = getenv("USER_PASSWORD")
    username = getenv("USERNAME")
    user_email = getenv("USER_EMAIL")

    config = BrowserConfig(
        headless=True,
        disable_security=True
    )

    browser = Browser(config=config)

    # Stage 1: Attempt login with kms_generated_password
    agent_script_stage1 = f"""
        1. visit https://x.com and click on Sign in, enter username {username}, on next screen enter the password {kms_generated_password} (While entering the password, make sure to click on show password button on the right of the password field).
        2. If while login it asks for email or phone no for verification, enter this {user_email} and click on next.
        3. If login is successful with kms_generated_password, return the message Login successful with KMS password and **IMMEDIATELY STOP EXECUTION HERE**."""

    agent = Agent(browser=browser, task=agent_script_stage1, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    print("Result", result)
    
    if "Login successful with KMS password" in str(result):
        print("Result : Login successful with KMS password")
        return
    else:
        print("Result : Login failed with KMS password")

    # Stage 2: Attempt login with user_provided_password and reset password
    agent_script_stage2 = f"""
        1. visit https://x.com and click on Sign in, enter username {username}, on next screen enter the password {user_provided_password} (While entering the password, make sure to click on show password button on the right of the password field).
        2. If while login it asks for email, enter this {user_email} and click on next.
        3. If login is successful with user_provided_password, proceed to reset the password.
        4. Click on more on left hand side and click on settings and privacy (do it in the same tab after login, don't redirect to something else).
        5. Click on your account and after that click on change your password.
        6. Enter the current password {user_provided_password} and then enter the new password {kms_generated_password} and confirm it and click on save.
        7. Return the message 'Password reset successful'."""

    agent = Agent(browser=browser, task=agent_script_stage2, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()

    if "Password reset successful" in str(result):
        print("Password reset successful , new password :", kms_generated_password)
        return
    else:
        print("Result : Password reset failed")

    print(result)

asyncio.run(main())
