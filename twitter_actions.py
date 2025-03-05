from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use import Browser

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