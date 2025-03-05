import asyncio
from os import getenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserConfig, Browser
import json

async def setup_browser() -> Browser:
    config = BrowserConfig(
        headless=True,
        disable_security=True
    )
    return Browser(config=config)

async def login_into_email(
    browser: Browser, 
    user_email: str, 
    kms_generated_password: str
) -> bool:
    agent_script = f"""
    1. Visit https://app.tuta.com/login, if you see Sign up and Switch color theme the page has loaded. (Don't say it has not loaded even though it has loaded, STOP REFRESHING!)
    2. Enter the email {user_email} in the email address field and password {kms_generated_password} in the password field and click on Log in.
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
    3. If you are able to see the For you and Following tab login was successfull and just return the message 'Login to the twitter account successfull with KMS generated password'.
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


async def generate_x_api_keys(
    browser: Browser, 
    username: str, 
    user_email: str, 
    kms_generated_password: str,
    x_app_name: str
) -> dict:
    """
    Generates X API keys (API key and API secret).
    """
    agent_script = f"""
    1. Visit http://developer.x.com/en and click on Developer portal.
    2. Click on sign in, enter username {username}.
    3. If login asks for email verification, enter {user_email} and click next.
    4. On password screen enter {kms_generated_password} (click show password button first).
    5. Once on developer portal, locate and click keys and tokens icon for {x_app_name}.
    6. On keys and tokens page:
       - Find API key section
       - Click regenerate button
       - Confirm by clicking "Yes, regenerate"
    7. Copy both API key and API secret.
    8. Return result in JSON format as:
       {{"api_key": "API_KEY", "api_key_secret": "API_KEY_SECRET"}}
    """
    agent = Agent(browser=browser, task=agent_script, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    
    content = result.final_result()
    print("API Keys Result:", content)
    
    return content if "api_key" in content else None


async def generate_x_access_token_secret(
    browser: Browser, 
    username: str, 
    user_email: str, 
    kms_generated_password: str,
    x_app_name: str
) -> dict:
    """
    Generates X Access Token and Secret.
    """
    agent_script = f"""
    1. Visit http://developer.x.com/en and click on Developer portal.
    2. Click on sign in, enter username {username}.
    3. If login asks for email verification, enter {user_email} and click next.
    4. On password screen enter {kms_generated_password} (click show password button first).
    5. Once on developer portal, locate and click keys and tokens icon for {x_app_name}.
    6. On keys and tokens page:
       - Find Access token and secret section
       - Click regenerate button
       - Confirm by clicking "Yes, regenerate"
    7. Copy both Access Token and Access Token Secret.
    8. Return result in JSON format as:
       {{"access_token": "ACCESS_TOKEN", "access_token_secret": "ACCESS_TOKEN_SECRET"}}
    """
    agent = Agent(browser=browser, task=agent_script, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    
    content = result.final_result()
    print("Access Token Result:", content)
    
    return content if "access_token" in content else None

async def main():
    # Get environment variables
    kms_generated_password = getenv("KMS_GENERATED_PASSWORD")
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
            return
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
            return
    print("Successfully logged in into twitter with KMS password")
    

    # Stage 3: Fetch API keys from X developer dashboard
    api_key_result = await generate_x_api_keys(browser, username, user_email, kms_generated_password, x_app_name)
    if api_key_result != None:    
        api_keys = json.loads(api_key_result)
        print(api_keys)
    else:
        print("Failed to fetch API keys!")

    # Stage 4: Fetch access token from X developer dashboard
    access_token_result = await generate_x_access_token_secret(browser, username, user_email, kms_generated_password, x_app_name)
    if access_token_result != None:    
        acess_tokens = json.loads(access_token_result)
        print(acess_tokens)
    else:
        print("Failed to fetch API keys!")

if __name__ == "__main__":
    asyncio.run(main())