from github import Github
from flask import Response
from flask import Flask
from flask import request

import re


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_issues():
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        repository = request.args.get("repository")
    except:
        username = None
        password = None
        repository = None

    if username and password and repository:
        def stream_issues(username, password, repo_name):
            yield "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><rows>"
            g = Github(username, password)
            states = ["open", "closed"]
            for repo in g.get_user().get_repos():
                if repo.name == repo_name:
                    for state in states:
                        for issue in repo.get_issues(state=state):
                            number = issue.number
                            title = issue.title
                            assignee = issue.assignee.name if issue.assignee else None
                            labels = ",".join([x.name for x in issue.labels])
                            created_at = issue.created_at.strftime("%m/%d/%Y")
                            closed_at = issue.closed_at.strftime("%m/%d/%Y") if issue.closed_at else None
                            milestone_title = None
                            milestone_number = None
                            milestone = issue.milestone
                            if milestone:
                                milestone_title = milestone.title
                                match = re.search("(\d+) - .*", milestone.title)
                                if match:
                                    milestone_number = int(match.group(1))                            
                            yield "<row><number>%s</number><state>%s</state><title>%s</title><assignee>%s</assignee><labels>%s</labels><created_at>%s</created_at><closed_at>%s</closed_at><milestone_title>%s</milestone_title><milestone_number>%s</milestone_number></row>" % (number, state, title, assignee, labels, created_at, closed_at, milestone_title, milestone_number)
                    break
            yield "</rows>"
        return Response(
            stream_issues(username, password, repository), mimetype="text/xml"
        )
    else:
        return Response("""
        <html>
        <body>
            <h4>Simple Issue Stream Usage:</h4>
            <p>/?username=&lt;github_username&gt;&password=&lt;github_password&gt;&repository=&lt;github_repository&gt;</p>
        </body>
        </html>
        """, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True)
