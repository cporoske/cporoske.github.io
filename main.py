# -*- coding: utf-8 -*-
import argparse
import markdown

from github import Github

MD_HEAD = """My personal blog"""

def get_me(user):
    return user.get_user().login

def is_me(issue, me):
    return issue.user.login == me

def format_time(time):
    return str(time)[:10]

def login(token):
    return Github(token)

def get_repo(user: Github, repo: str):
    return user.get_repo(repo)

def add_issue_info(issue, md):
    time = format_time(issue.created_at)
    md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")

def add_md_recent(repo, md, me, limit=5):
    count = 0
    with open(md, "a+", encoding="utf-8") as md:
        # one the issue that only one issue and delete (pyGitHub raise an exception)
        try:
            md.write("## 最近更新\n")
            for issue in repo.get_issues(sort="created", direction="desc"):
                if is_me(issue, me):
                    add_issue_info(issue, md)
                    convert_html_file = "index" + ("" if count == 0 else str(count)) + ".html"
                    with open(convert_html_file, "w", encoding="utf-8") as html_file:
                        html_file.write(markdown.markdown(issue.body))
                    count += 1
                    if count >= limit:
                        break
        except Exception as e:
            print(str(e))

def add_md_header(md, repo_name):
    with open(md, "w", encoding="utf-8") as md:
        md.write(MD_HEAD.format(repo_name=repo_name))
        md.write("\n")

def main(token, repo_name, issue_number=None):
    user = login(token)
    me = get_me(user)
    repo = get_repo(user, repo_name)
    # add to readme one by one, change order here
    add_md_header("README.md", repo_name)
    for func in [add_md_recent]:
        func(repo, "README.md", me)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument(
        "--issue_number", help="issue_number", default=None, required=False
    )
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
