"""Blogly application."""

from flask import Flask,render_template,request,redirect
from models import db, connect_db,User,Post,Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'f724'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.debug = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    '''Homepage defaults to list of users'''
    return redirect('/users')

@app.route('/users')
def users():
    '''Page of list of users'''
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/user_page.html',users = users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    '''Show form for adding new user'''
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    '''Handle form submission to add new user'''
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Show individual user page'''
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html',user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Show form for editing specific user'''
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html',user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    '''Handle form submission of edit info for user'''
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Remove user from list'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')



# Post Routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    '''Show form for user to create post'''
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html',user=user)

@app.route('/users/<int:user_id>/posts/new',methods=['POST'])
def new_post(user_id):
    '''Handle form submission of post'''
    user = User.query.get_or_404(user_id)
    post = Post(title=request.form['title'],
                content=request.form['content'],
                user_id=user_id
            )
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show an individual post'''
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''Show form for editing posts'''
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    '''Handle form submission to edit post'''
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete specified post'''
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')



# Tag Routes
@app.route('/tags')
def tags_list():
    '''Show a list of all tags'''
    tags = Tag.query.all()
    return render_template('tags/tags_page.html',tags=tags)

@app.route('/tags/new')
def new_tag_form():
    '''Show form for creating new tag'''
    posts = Post.query.all()
    return render_template('tags/new.html',posts=posts)

@app.route('/tags/new', methods=['POST'])
def new_tag():
    '''Handle form submission for creating tag'''
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tags = Tag(name=request.form['name'],posts=posts)

    db.session.add(new_tags)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):
    '''Show info of specific tag'''
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/show.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    '''Show form to edit tag info'''
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tags/edit.html',tag=tag,posts=posts)

@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def edit_tag(tag_id):
    '''Handle form submission to edit tag'''
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''Remove tag'''
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
