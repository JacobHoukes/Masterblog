from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_blog_posts():
    """This function loads the blog posts from the JSON file"""
    try:
        with open('blog_posts.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_blog_posts(blog_posts):
    """This function saves the blog posts to the JSON file"""
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)


@app.route('/')
def index():
    """This function renders the homepage with a list of blog posts."""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """This function handles adding a new blog post and redirects to the homepage."""
    if request.method == 'POST':
        blog_posts = load_blog_posts()

        new_post = {
            "id": max([post["id"] for post in blog_posts], default=0) + 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """This function deletes a blog post by its ID and redirects to the homepage."""
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """This function updates an existing blog post and redirects to the homepage."""
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    elif request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
