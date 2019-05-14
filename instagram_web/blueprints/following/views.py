from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from models.users import User
from models.followers import Followers

following_blueprint = Blueprint(
    'following', __name__, template_folder='templates')


@following_blueprint.route('<idol_id>', methods=["POST"])
@login_required
def create(idol_id):
    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash('No user found', 'warning')
        return redirect(url_for('home'))

    new_follow = Followers(
        fan_id=current_user.id,
        idol_id=idol.id
    )

    if not idol.is_private:
        new_follow.approved = True

    for i in current_user.idols:
        if i.idol_id == idol.id:
            flash('Already following')
            return redirect(url_for('users.show', username=idol.username))

    if not new_follow.save():
        flash("unable to follow this user", "danger")
        return redirect(url_for('users.show', username=idol.username))

    if new_follow.is_approved:
        flash('You are not following {idol.username}', 'success')
        return redirect(url_for('users.show', username=idol.username))

    flash('Requested', 'success')
    return redirect(url_for('users.show', username=idol.username))
