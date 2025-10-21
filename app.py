from flask import Flask, render_template, abort
import os, json

# create an instance of the flask class
app = Flask(__name__)
articles_dir = "articles"

# load all articles
def load_articles():
    articles = []
    for filename in os.listdir(articles_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(articles_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Derive slug from filename if not present
                data["slug"] = data.get("slug", filename[:-5])
                # if key "slug" exists, it returns the value. otherwise, it returns the default
                # (filename[:-5]). the [:-5] chops off the .json extension.
                articles.append(data)
    # Sort by date (newest first)
    articles.sort(key=lambda x: x["date"], reverse=True)
    return articles

# load particular article
def load_article(slug):
    filepath = os.path.join(articles_dir, f"{slug}.json")
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def home():
    articles = load_articles()
    return render_template("home.html", articles=articles)

@app.route("/article/<slug>")
def article_page(slug):
    article = load_article(slug)
    return render_template("article.html", article=article)

if __name__ == "__main__":
    app.run(debug=True)
