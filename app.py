from flask import Flask, render_template
import json

app = Flask(__name__)

# Helper function to load blog posts from JSON file
def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
