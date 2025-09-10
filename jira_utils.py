import os
from jira import JIRA
from dotenv import load_dotenv

load_dotenv() 

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER_LOGIN = os.getenv("JIRA_USER_LOGIN")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_UPDATED= int(os.getenv("JIRA_UPDATED"))

def connect_to_jira():    
    options = {"server": JIRA_SERVER}
    jira = JIRA(options, basic_auth=(JIRA_USER_LOGIN, JIRA_TOKEN))
    return jira

def configure_updated_value():
    global JIRA_UPDATED
    if JIRA_UPDATED is None or JIRA_UPDATED > 0:
        JIRA_UPDATED = -45
   
def fetch_bugs():
    configure_updated_value()
    jira = connect_to_jira() 
    jql = f'project = "{JIRA_PROJECT_KEY}" AND issuetype = Bug AND updated >= {JIRA_UPDATED}'
    issues = jira.search_issues(jql, maxResults=False)
    return issues
  
