import time
from flask import Flask, render_template, request, redirect
import data_manager
import util


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
@app.route("/list", methods=['GET', 'POST'])
def question_table():
    table = data_manager.read_csv('question.csv')
    reversed_table = reversed(table)
    return render_template("list.html", table=reversed_table)


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def display_a_question(question_id):

    table = data_manager.read_csv('question.csv')
    answer_table = data_manager.read_csv('answer.csv')
    reverse_timeline = reversed(list(answer_table))
    question_line = util.find_line(table, question_id, 0)
    question_title = question_line[4]
    question_msg = question_line[5]

    answer_line = util.find_line(answer_table, question_id, 2)
    answer = answer_line[4]

    return render_template('display_a_question.html', answer_table=reverse_timeline, answer=answer, line=answer_line,
                           table=table, question_id=question_id, title=question_title, question_msg=question_msg)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'GET':
        return render_template('post_answers.html')
    elif request.method == 'POST':
        answers = data_manager.read_csv("answer.csv")
        form = request.form.to_dict()
        form_list = [util.add_new_id(answers), int(time.time()), 0, 0, form['post_answers'], answers, '']
        answers.append(form_list)
        data_manager.write_csv("answers.csv", answers)
        return redirect('/list')


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("ask_question.html")
    elif request.method == "POST":
        questions = data_manager.read_csv("question.csv")
        form = request.form.to_dict()
        form_list = [util.add_new_id(questions), int(time.time()), 0, 0, form['questiontitle'], form['question_body'], '']
        questions.append(form_list)
        data_manager.write_csv("question.csv", questions)
        return redirect("/")


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True)
