from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def load_blog_posts():
    if os.path.exists('blog_posts.json'):
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    return []


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
