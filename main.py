from flask import Flask, render_template
from post import Post
import requests
from datetime import datetime

app = Flask(__name__)


class Blog:
    def __init__(self):

        self.posts_url = requests.get(
            url="https://api.npoint.io/5abcca6f4e39b4955965").json()
        self.posts_list = list()
        for post in self.posts_url:
            self.blog_post = Post(post["id"], post["title"], post["subtitle"],
                                  post["body"])
            self.posts_list.append(self.blog_post)
        self.year = datetime.now().year

        self.home_route()
        self.single_post()

    def home_route(self):
        """Main blog page displays all posts"""
        @app.route("/")
        def get_all_posts():
            return render_template("index.html", all_posts=self.posts_list,
                                   year=self.year)

    def single_post(self):
        """url for each of the posts"""
        @app.route("/post/<int:index>")
        def show_post(index):
            requested_post = None
            for blog_post in self.posts_list:
                if blog_post.id == index:
                    requested_post = blog_post
            return render_template("post.html", post=requested_post)


Blog()

if __name__ == "__main__":
    app.run()
