import json
import os 
import requests 
import random

RANDOM_GRADIENT = [
    "linear-gradient(to right, #1fa2ff, #12d8fa, #a6ffcb)",
    "linear-gradient(to right, #f12711, #f5af19)",
    "linear-gradient(to right, #da4453, #89216b)",
    "linear-gradient(to right, #ff512f, #dd2476)",  
    "linear-gradient(to right, #c31432, #240b36)",
    "linear-gradient(to right, #654ea3, #eaafc8)",
    "linear-gradient(to right, #ff416c, #ff4b2b)",
    "linear-gradient(to right, #00b4db, #0083b0)",
    "linear-gradient(to right, #f83600, #f9d423)",
    "linear-gradient(to right, #ff9966, #ff5e62)",
]
def generate_json_file(name, title, description,email,profile_pic):
    data = {
        "name": name,
        "title": title,
        "description": description,
        "email":email,
        "profile_pic": profile_pic,
        "background": random.choice(RANDOM_GRADIENT)
    }
    with open(f"templates/data.json", "w") as file:
        json.dump(data, file)


def create_repo(token,repo_name):
    headers = {
    'Authorization': 'token '+token,
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    dt = {"name":repo_name }
    res = requests.post('https://api.github.com/user/repos', headers=headers, json=dt)
    return res

def upload_to_gh_pages(token,username,repo_url):
    headers = {
    'Authorization': 'token '+token,
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"source":{"branch":"master","path":"/"}}'
    response = requests.post(f'https://api.github.com/repos/{username}/{repo_url}/pages', headers=headers, data=data)
    return response

def initialize_git_and_upload_to_repo(token, username,repo_name):
    # delete existing .git folder in templates 
    # and set the remote origin and add all files to git 
    os.system('git config --global user.email {username}"@gmail.com"')
    os.system('git config --global user.name {username}')
    os.system("rm -rf templates/.git")
    os.system("cd templates && git init && git add . && git commit -m 'first commit'");
    os.system("cd templates && git remote add origin "  + f"https://{token}@github.com/{username}/{repo_name}" + "&& git push origin master");


def remote_init_and_upload(token, username,repo_name):
    # create a repo 
    res = create_repo(token,repo_name)
    print("uploading");
    initialize_git_and_upload_to_repo(token, username,repo_name)
    print("done")