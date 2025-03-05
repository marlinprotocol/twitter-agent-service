from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use import Browser

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