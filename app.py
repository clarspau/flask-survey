from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as sat_survey

# This is a constant variable and will be used as a key to access and store data in the Flask session object.
USER_RESPONSES = "responses"


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    """Beginning of the chosen survey"""

    return render_template("survey.html", sat_survey=sat_survey)


@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the stored data in the Flask session of user's responses."""

    session[USER_RESPONSES] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save the user's response and redirect to next question."""

    # get the chosen response/answer.
    choice = request.form['answer']

    # add this response to the session
    responses = session[USER_RESPONSES]
    responses.append(choice)
    session[USER_RESPONSES] = responses

    if (len(responses) == len(sat_survey.questions)):
        # All questions have been answered.
        return redirect("/end-survey")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(USER_RESPONSES)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(sat_survey.questions)):
        # All questions have been answered.
        return redirect("/end-survey")

    if (len(responses) != qid):
        # Flash a message if the user is trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = sat_survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/end-survey")
def end_survey():
    """Survey complete. Show completion page."""

    return render_template("end_survey.html")
