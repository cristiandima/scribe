# Scribe

This is a very small but somewhat capabale static blog generator. Out of the box it can easily generate blogs of the form

- index page (home page listing the titles of all the blog posts)
- other pages (about, contact, etc)
- blog posts (the articles themselves)

As an end user you only have to write .md files in the articles directory and run the script. For any advanced options or to better understand how the program works have a look at the source code (it's around a hundred lines long).

## Usage

Run these commands:

```
git clone https://github.com/cristiandima/scribe my-blog
cd my-blog
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
python scribe.py
```

and visit localhost:8000 to see the generated default blog.
