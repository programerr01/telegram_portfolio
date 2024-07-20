import json
import os 
import requests 
def generate_json_file(name, title, description,email,profile_pic):
    data = {
        "name": name,
        "title": title,
        "description": description,
        "email":email,
        "profile_pic": profile_pic,
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