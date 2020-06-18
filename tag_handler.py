from flask import render_template, request, redirect, url_for, Blueprint, session, abort
import data_manager
import util

tag = Blueprint('tag', __name__, template_folder='templates')


@tag.route('/tags')
def display_tags():
    username, logged_user_id = util.set_user_details_based_on_logged_status()
    tags_collection = data_manager.get_available_tags()
    for element in tags_collection:
        element["questions"] = util.prepare_questions_to_display(
            data_manager.get_questions_with_specific_tag(element.get("name")))
        element["amount_of_question"] = len(element["questions"])
    return render_template(
        "tags_list.html",
        tags=tags_collection,
        user_id=logged_user_id,
        username=username
    )


@tag.route('/question/<question_id>/new-tag')
def add_tag(question_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_question = data_manager.get_specific_record(question_id, "question")
    util.check_if_user_is_owner(logged_user_id, selected_question["user_id"])
    tags_collection = data_manager.get_available_tags()
    new_tag = request.args.get("new_tag")
    if new_tag:
        if not data_manager.check_if_tag_already_available(new_tag, tags_collection):
            data_manager.add_tag_to_db(new_tag)
        tag_id = data_manager.get_tag_id(new_tag).get("id")
        if not data_manager.is_tag_already_assigned(question_id, tag_id):
            data_manager.assign_tag_to_question(question_id, tag_id)
        return redirect(f"/question/{question_id}")
    return render_template(
        "add_tag.html",
        tags_list=tags_collection,
        user_id=logged_user_id,
        username=username
    )


@tag.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    util.check_if_user_is_logged()
    username, logged_user_id = util.get_user_details_from_session()
    selected_tag = data_manager.get_specific_record(question_id, "question")
    util.check_if_user_is_owner(logged_user_id, selected_tag["user_id"])
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("show_question", question_id=question_id))
