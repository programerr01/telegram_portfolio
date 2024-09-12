import json
import subprocess 
import random
import re 
import time 
import shlex
import logging 

import requests 


logging.basicConfig(level=logging.DEBUG)

STYLES = [
    "deep_blue",
    "vibrant_purple",
    "teal_green",
    "warm_orange",
    "cool_blue_green",
    "magenta_indigo",
    "sunset",
    "neon"
    ]


CONVERSIONS =  {
   '🔵': "deep_blue",
   '🟣': "vibrant_purple",
    '🟩': "teal_green",
    '🟧': "warm_orange",
    '🟦':"cool_blue_green",
    '🟥':"magenta_indigo",
    '🟨':"sunset",
    '📗':"neon"
}


def generate_json_file(name, title, description,email,linkedin,profile_pic,theme):
    logging.critical("Generating json file")
    try:
        data = {
            "name": name,
            "title": title,
            "description": description,
            "email":email,
            "linkedin":linkedin,
            "profile_pic": profile_pic,
            "theme": CONVERSIONS[theme]
        }
        with open(f"templates/data.json", "w") as file:
            json.dump(data, file)
    except Exception as e: 
        logging.error("Error while in generate json file",str(e))
        raise e 
    


def create_repo(token,repo_name):
    logging.critical("Creating Repo")

    try:
        headers = {
        'Authorization': 'token '+token,
        'Content-Type': 'application/x-www-form-urlencoded',
        }

        dt = {"name":repo_name }
        res = requests.post('https://api.github.com/user/repos', headers=headers, json=dt)
        return res
    except Exception as e:
        logging.error("Error while creating repo",str(e))
        raise e

def check_repo_status(token,username,repo_url):
    logging.critical("Checking repo status")
    try:
        headers = {
        'Authorization': 'token '+token,
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_url}/pages/builds/latest', headers=headers)
        return response.json()
    except Exception as e:
        logging.error("Error while checking repo status",str(e))
        raise e
    
def upload_to_gh_pages(token,username,repo_url):
    logging.critical("Uploading to gh pages")

    try:
        headers = {
        'Authorization': 'token '+token,
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = '{"source":{"branch":"master","path":"/"}}'
        response = requests.post(f'https://api.github.com/repos/{username}/{repo_url}/pages', headers=headers, data=data)
        return response
    except Exception as e:
        logging.error("Error while uploading to gh pages",str(e))
        raise e

def initialize_git_and_upload_to_repo(token, username,repo_name):
    logging.critical("Initializing git and uploading to repo")

    # delete existing .git folder in templates 
    # and set the remote origin and add all files to git 
    try:
        run_bash_command('git config --global user.email {username}"@gmail.com"')
        run_bash_command('git config --global user.name {username}')
        run_bash_command("rm -rf templates/.git")
        run_bash_command("cd templates && git init && git add . && git commit -m 'first commit'");
        run_bash_command("cd templates && git remote add origin "  + f"https://{token}@github.com/{username}/{repo_name}" + "&& git push origin master");
    except Exception as e:
        logging.error("Error while initializing git and uploading to repo",str(e))
        raise e
            


def remote_init_and_upload(token, username,repo_name):
    # create a repo 
    res = create_repo(token,repo_name)
    print("uploading");
    initialize_git_and_upload_to_repo(token, username,repo_name)
    print("done")


## LOCAL HELPERS 
def share_bad_news(update):
    update.message.reply_text("Sorry! Some Error Occured. Please try again in Some Time.")
    return 0

def sanitize_user_name(user_name):
    try:
        safe_username = re.sub(r'[^\w\-]', '', user_name)
        return shlex.quote(safe_username)
    except Exception as e:
        logging.error("Error while sanitizing username",str(e));
        return ""


def run_bash_command(command):
    result = subprocess.run(command, shell=True)
    return_code = result.returncode
    if(return_code != 0):
        raise Exception(f"Error while running command {command}")
    

def check_for_build_updates(token,username,repo_url):
    TOTAL_TRIES = 10;
    DELAY_IN_BETWEEN = 20;
    curr_tries = 0;
    while curr_tries < TOTAL_TRIES:
        try:
            response = check_repo_status(token,username,repo_url)
            if(response['status'] == 'built'):
                return True
        except Exception as e:
            logging.error("Error while checking for build updates",str(e)) 
        curr_tries += 1
        time.sleep(DELAY_IN_BETWEEN)
    return False;