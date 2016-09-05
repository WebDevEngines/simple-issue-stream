from github import Github
from flask import Response
from flask import Flask
from flask import request
from StringIO import StringIO

import re
import csv
import os


app = Flask(__name__)


username = os.environ.get("GITHUB_USERNAME", None)
password = os.environ.get("GITHUB_PASSWORD", None)
repository = os.environ.get("GITHUB_REPOSITORY", None)
token = os.environ.get("TOKEN", None)


def remove_non_ascii(text):
    if text:
        return "".join([i if ord(i) < 128 else " " for i in text])
    return ""


@app.route("/", methods=["GET"])
def get_issues():
    try:
        user_token = request.args.get("user_token")
    except:
        user_token = None

    if token != user_token:
        return Response("Access denied", 401)

    if username and password and repository:
        def stream_issues(username, password, repo_name):
            g = Github(username, password)
            states = ["open", "closed"]
            for repo in g.get_user().get_repos():
                if repo.name == repo_name:
                    yield "number,title,assignee,labels,created_at,closed_at,milestone_title,milestone_number\n"
                    for state in states:
                        for issue in repo.get_issues(state=state):
                            number = issue.number
                            title = issue.title
                            assignee = issue.assignee.name if issue.assignee else ""
                            labels = ",".join([x.name for x in issue.labels])
                            created_at = issue.created_at.strftime("%m/%d/%Y")
                            closed_at = issue.closed_at.strftime("%m/%d/%Y") if issue.closed_at else ""
                            milestone_title = ""
                            milestone_number = 0
                            milestone = issue.milestone
                            if milestone:
                                milestone_title = milestone.title
                                match = re.search("(\d+) - .*", milestone.title)
                                if match:
                                    milestone_number = int(match.group(1))                            
                            output = StringIO()
                            try:
                                writer = csv.writer(output)
                                writer.writerow([
                                    number,
                                    remove_non_ascii(title),
                                    remove_non_ascii(assignee),
                                    remove_non_ascii(labels),
                                    created_at,
                                    closed_at,
                                    remove_non_ascii(milestone_title),
                                    milestone_number
                                ])
                                yield output.getvalue()
                            finally:
                                output.close()
                    break
        return Response(
            stream_issues(username, password, repository), mimetype="application/csv"
        )

    return Response("user_token missing", 400)

if __name__ == "__main__":
    app.run(debug=True)
