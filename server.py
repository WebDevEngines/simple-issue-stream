from github import Github
from flask import Response
from flask import Flask
from flask import request

import re
import json
import os


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_issues():
    def stream_issues(username, password, repo_name):
        yield "["
        g = Github(username, password)
        states = ["open", "closed"]
        issues = []
        first_issue = True
        for repo in g.get_user().get_repos():
            if repo.name == repo_name:
                for state in states:
                    for issue in repo.get_issues(state=state):
                        if first_issue:
                            first_issue = False
                        else:
                            yield ","

                        assignee = issue.assignee
                        obj = {
                            "id": issue.id,
                            "state": state,
                            "number" : issue.number,
                            "title": issue.title,
                            "assignee": assignee.name if assignee else None,
                            "labels": ",".join([x.name for x in issue.labels]),
                            "created_at": issue.created_at.strftime("%m/%d/%Y"),
                            "closed_at": issue.closed_at.strftime("%m/%d/%Y") if issue.closed_at else None,
                            "milestone_title": None,
                            "milestone_number" : None
                        }

                        milestone = issue.milestone
                        if milestone:
                            obj["milestone_title"] = milestone.title
                            match = re.search("(\d+) - .*", milestone.title)
                            if match:
                                obj["milestone_number"] = int(match.group(1))
                        
                        yield json.dumps(obj)
                break
        yield "]"

    return Response(
        stream_issues(request.args.get("username"), request.args.get("password"), request.args.get("repository")), 
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True)
