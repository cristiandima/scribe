import os
import shutil
import frontmatter
from distutils.dir_util import copy_tree
from itertools import groupby
from markdown import markdown
from jinja2 import Environment, PackageLoader
from slugify import slugify

CONTENT = 'content'
STATIC = 'static'
THEME = 'default'
TEMPLATES = os.path.join('themes', THEME)
DEFAULT_TEMPLATE = 'article.html'
OUTPUT = 'website'
EXTENSIONS = ('.markdown', '.mdown', '.mkdn', '.mkd', '.md')


def get_posts():
    md_files = []
    for path, subdirs, files in os.walk(CONTENT):
        for name in files:
            if name.endswith(EXTENSIONS):
                md_files.append(os.path.join(path, name))

    posts = []
    for file in md_files:
        post = frontmatter.load(file)
        post['file_path'] = file
        post['file_name'] = os.path.basename(file)
        post['permalink'] = post.get('permalink', True)
        post['template'] = post.get('template', DEFAULT_TEMPLATE)
        post['content'] = post.content

        noext_name = os.path.splitext(post['file_name'])[0]
        if post['permalink']:
            slug = slugify(noext_name)
            post['output_path'] = os.path.join(slug, 'index.html')
            post['slug'] = slug
        else:
            post['output_path'] = noext_name + '.html'
            post['slug'] = post['output_path']

        posts.append(post)

    return posts


def apply_collections(posts):
    for post in posts:
        dir_path = os.path.dirname(post['file_path'])
        post['collection'] = os.path.basename(dir_path)


def apply_markdown(posts):
    extensions = ['markdown.extensions.fenced_code',
                  'markdown.extensions.codehilite']
    for post in posts:
        post['content'] = markdown(post.content, extensions=extensions)


def apply_templates(posts):
    collection_group = groupby(posts, lambda x: x['collection'])
    collections = dict((k, list(g)) for k, g in collection_group)

    env = Environment(loader=PackageLoader('scribe', TEMPLATES))
    for post in posts:
        tmpl = env.get_template(post['template'])
        post.html = tmpl.render(collections=collections, **post)


def make_site(posts):
    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)

    for post in posts:
        path = os.path.join(OUTPUT, post['output_path'])
        write_folders_and_file(path, post.html)

    copy_tree(STATIC, os.path.join(OUTPUT, STATIC))


def write_folders_and_file(path, content):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(path, "w") as f:
        f.write(content)


def run_server():
    from http.server import test, SimpleHTTPRequestHandler
    os.chdir(OUTPUT)
    test(HandlerClass=SimpleHTTPRequestHandler)


if __name__ == '__main__':
    posts = get_posts()
    apply_collections(posts)
    apply_markdown(posts)
    apply_templates(posts)
    make_site(posts)
    run_server()
