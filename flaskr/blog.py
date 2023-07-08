from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from datetime import date

from flaskr.auth import login_required
#from flaskr.db import get_db

from .db import db_session
from .models import Post, User

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    pass
    # db = get_db()
    # posts = db.execute('SELECT p.id, title, body, created, author_id, username'' FROM post p JOIN user u ON p.author_id = u.id'' ORDER BY created DESC').fetchall()
    posts = Post.query.join(User).add_columns(User.name, Post.autor_id, Post.body, Post.created, Post.id, Post.title, Post.user).order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # db = get_db()
            # db.execute(
            #     'INSERT INTO post (title, body, author_id)'
            #     ' VALUES (?, ?, ?)',
            #     (title, body, g.user['id'])
            # )
            # db.commit()
            hoje = date.today()
            post = Post(g.user.id, hoje, title, body)
            db_session.add(post)
            db_session.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    # post = get_db().execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.id = ?',
    #     (id,)
    # ).fetchone()
    post = Post.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    # post = get_post(id)
    post = Post.query.get(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # db = get_db()
            # db.execute(
            #     'UPDATE post SET title = ?, body = ?'
            #     ' WHERE id = ?',
            #     (title, body, id)
            # )
            # db.commit()
            post.title = title
            post.body = body
            post.created = date.today()
            db_session.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    # get_post(id)
    # db = get_db()
    # db.execute('DELETE FROM post WHERE id = ?', (id,))
    # db.commit()
    post = Post.query.get(id)
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for('blog.index'))    