from flask import render_template, request, redirect, url_for, Blueprint, session, abort
import data_manager
import util

tag = Blueprint('tag', __name__, template_folder='templates')


@tag.route('/tags')
def display_tags():
    if 'username' in session:
        username = session['username']
        user_id = data_manager.get_user_id(username)['id']
    else:
        user_id = None
        username = None
    tags_list = data_manager.get_available_tags()
    for tag in tags_list:
        tag["questions"] = util.prepare_questions_to_display(data_manager.get_questions_with_specific_tag(tag.get("name")))
        tag["amount_of_question"] = len(tag["questions"])
    return render_template(
        "tags_list.html",
        tags=tags_list,
        user_id=user_id,
        username=username
    )


@tag.route('/question/<question_id>/new-tag')
def add_tag(question_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    record = data_manager.get_specific_record(question_id, "question")
    user_id = data_manager.get_user_id(username)['id']
    if user_id != record["user_id"]:
        abort(401)
    tags_list = data_manager.get_available_tags()
    new_tag = request.args.get("new_tag")
    if new_tag:
        if not data_manager.check_if_tag_already_available(new_tag, tags_list):
            data_manager.add_tag_to_db(new_tag)
        tag_id = data_manager.get_tag_id(new_tag).get("id")
        if not data_manager.is_tag_already_assigned(question_id, tag_id):
            data_manager.assign_tag_to_question(question_id, tag_id)
        return redirect(f"/question/{question_id}")
    return render_template(
        "add_tag.html",
        tags_list=tags_list,
        user_id=user_id,
        username=username
    )


@tag.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    if 'username' not in session:
        abort(401)
    username = session['username']
    record = data_manager.get_specific_record(question_id, "question")
    user_id = data_manager.get_user_id(username)['id']
    if user_id != record["user_id"]:
        abort(401)
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("show_question", question_id=question_id))
