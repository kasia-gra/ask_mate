from flask import render_template, request, redirect, url_for, Blueprint, session, flash
import data_manager

tag = Blueprint('tag', __name__, template_folder='templates')


@tag.route('/question/<question_id>/new-tag')
def add_tag(question_id):
    if 'username' not in session:
        flash("You can't add tag!")
        return redirect(f"/question/{question_id}")
    logged_status = True
    username = session['username']
    user_id = session['user_id']
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
        logged=logged_status,
        user_id=user_id,
        username=username
    )


@tag.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    if 'username' not in session:
        flash("You can't delete tag!")
        return redirect(url_for("show_question", question_id=question_id))
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("show_question", question_id=question_id))
