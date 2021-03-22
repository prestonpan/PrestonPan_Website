#!/usr/bin/python
### static assembly template generator, or SATG ###
### html adjacent language = SATL or static assembly template language ###
import os
import re
from pathlib import Path


### IMPORT ALL TEMPLATE FILES ###
TEMPLATE_PATH = Path('./templates')

with open((TEMPLATE_PATH / "project.html").resolve(), "r") as f:
    project_template = f.read()

with open((TEMPLATE_PATH / "projects.html").resolve(), "r") as f:
    projects_template = f.read()

with open((TEMPLATE_PATH / "post.html").resolve(), "r") as f:
    blog_template = f.read()

with open((TEMPLATE_PATH / "posts.html").resolve(), "r") as f:
    blogs_template = f.read()

with open((TEMPLATE_PATH / "item_overview.html").resolve(), "r") as f:
    item_overview_template = f.read()

with open((TEMPLATE_PATH / "item_total_overview.html").resolve(), "r") as f:
    item_total_overview_template = f.read()

with open((TEMPLATE_PATH / "index.html").resolve(), "r") as f:
    index_template = f.read()

with open((TEMPLATE_PATH / "404.html").resolve(), "r") as f:
    _404_template = f.read()

with open((TEMPLATE_PATH / "style.html").resolve(), "r") as f:
    style = f.read()

### DATA ###
dirname = os.path.dirname(__file__)

blog = [
    3,
    {
        'name': "{%TITLE%}",
        "description": "{%DESCRIPTION%}",
        "picture": None,
        'link': None,
        'path': "f{%MAIN_CONTENT%}",
        'template': blog_template,
    },
    {
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'picture': "{%PICTURE%}",
        'link': "{%ITEM_PATH%}",
        'path': None,
        'template': item_total_overview_template,
    },
    {
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'picture': "{%PICTURE%}",
        'link': "{%ITEM_PATH%}",
        'path': None,
        'template': item_overview_template,
    },
    {
        'name': "Minimalism",
        'description': "My thoughts on web bloat and software bloat.",
        'picture': "./content/projects/minimalism/minimalism.webp",
        'link': "./content/blog/minimalism/minimalism.html",
        'path': os.path.join(dirname, "content/blog/minimalism/minimalism.html"),
        'future_name': 'minimalism'
    }, 
    {
        'name': "Privacy",
        'description': "My thoughts on surveillance.",
        'picture': "./content/blog/privacy/privacy.webp",
        'link': "./content/blog/privacy/privacy.html",
        'path': os.path.join(dirname, "content/blog/privacy/privacy.html"),
        "future_name": 'privacy'
    },
    {
        'name': "First Blog",
        'description': "My first ever blog on my own site.",
        'picture': "./content/blog/first_blog/first_blog.webp",
        'link': "./content/blog/FirstBlog/first_blog.html",
        'path': os.path.join(dirname, "content/blog/first_blog/first_blog.html"),
        "future_name": "first_blog"
    },
]

project = [
    3, ### The number of templates ###
    { ### TEMPLATE 1, None means the key will be ignored by the compiler ###
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'path': "f{%MAIN_CONTENT%}", 
        'picture': None,
        'gitlab': "{%GITLAB_REPO%}",
        'template': project_template,
    },
    { ### TEMPLATE 2 ###
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'path': "{%ITEM_PATH%}",
        'picture': "{%PICTURE%}",
        'gitlab': None,
        'template': item_total_overview_template,
    },
    { ### TEMPLATE 3 ###
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'path': "{%ITEM_PATH%}",
        'picture': "{%PICTURE%}",
        'gitlab': None,
        'template': item_overview_template,
    },
    {
        'name': "My dotfiles",
        'description': "My minimal linux dotfiles.",
        'path': os.path.join(dirname, "content/projects/my_dotfiles/my_dotfiles.html"),
        'link': "./content/projects/my_dotfiles/my_dotfiles.html", 
        'picture': "./content/projects/my_dotfiles/my_dotfiles.webp",
        'gitlab': "https://gitlab.com/PrestonPan/dotfiles",
        "future_name": "my_dotfiles"
    },
    {
        'name': "PanTech website",
        'description': "My amazing website.",
        'path': os.path.join(dirname, "content/projects/prestonpan/prestonpan.html"),
        'link': "./content/projects/prestonpan/prestonpan.html", 
        'picture': "./content/projects/prestonpan/prestonpan.webp",
        'gitlab': "https://gitlab.com/PrestonPan/prestonpan",
        "future_name": "prestonpan"
    },
    {
        'name': "NoExcess",
        'description': "An elegant, and frankly useless compiled programming language.",
        'path': os.path.join(dirname, "content/projects/noexcess/noexcess.html"),
        'link': "./content/projects/NoExcess/noexcess.html", 
        'picture': "./content/projects/noexcess/noexcess.webp",
        'gitlab': "https://gitlab.com/PrestonPan/NoExcess",
        "future_name": "noexcess"
    },
]


### ATTEMPTING TO MAKE A CLASS ###
class SATG:
    def __init__(self, data):
        self.data = data
                
    def build_dataset(self, index):
        dicts = self.data[index]
        all_fragments = []
        for i in range(1, dicts[0] + 1): ### loops through all the template dicts ###
            keys = list(dicts[i].keys()) # get list of keys
            fragments = []
            
                
            for j in range(dicts[0] + 1, len(dicts)): ### loops through all the data dicts, this makes one list of fragments ###
                template = dicts[i]["template"] # the template 
                for key in keys[:-1]: ### Excluding the template key from the loop, loop's function is to loop through to replace all tags ###
                    tag = dicts[i][key] # the tag
                    content = dicts[j][key] # the content
                    if tag is None: ### Completely ignore tags which aren't existent in the template dicts ###
                        continue
                    elif tag[0] == "f": ### If the tag is a file tag then read that file, get the content and then replace ###
                        with open(content, "r") as f:
                            fragment = f.read()
                        template = re.sub(tag, fragment, template)
                    else: ### Else just replace the tag with content ###
                        template = re.sub(tag, content, template)
                if "future_name" in dicts[j]:
                    fragments.append([dicts[j]["future_name"], template]) ### outside the loop which replaces everything.###
                else:
                    fragments.append(template)

            all_fragments.append(fragments) # templates = all templates which are of the same kind using different data

        return all_fragments


            
    @staticmethod
    def replace_single_tag(fragment, tag, text):
        if tag[0] == 'f':
            with open(text, "r") as f:
                e = f.read()
        else:
            e = text
        return fragment.replace(tag, e)

generator = SATG([blog, project])
all_blog_templates = generator.build_dataset(0)
all_project_templates = generator.build_dataset(1)

for i in range(len(all_blog_templates)):
    for j in range(len(all_blog_templates[i])):
        if type(all_blog_templates[i][j]) is not list:
            all_blog_templates[i][j] = generator.replace_single_tag(all_blog_templates[i][j], "{%STYLE%}", style)
        else:
            all_blog_templates[i][j][1] = generator.replace_single_tag(all_blog_templates[i][j][1], "{%STYLE%}", style)

for i in range(len(all_project_templates)):
    for j in range(len(all_blog_templates[i])):
        if type(all_project_templates[i][j]) is not list:
            all_project_templates[i][j] = generator.replace_single_tag(all_blog_templates[i][j], "{%STYLE%}", style)
        else:
            all_project_templates[i][j][1] = generator.replace_single_tag(all_blog_templates[i][j][1], "{%STYLE%}", style)

d = os.path.dirname(dirname)

for i in range(len(all_blog_templates[0])):
    if not os.path.exists(os.path.join(d, f"build/content/blog/{all_blog_templates[0][i][0]}")):
        os.mkdir(f'{d}/build/content/blog/{all_blog_templates[0][i][0]}')
    with open(f'{d}/build/content/blog/{all_blog_templates[0][i][0]}/{all_blog_templates[0][i][0]}.html', "w+") as f:
        f.write(all_blog_templates[0][i][1])

for i in range(len(all_project_templates[0])):
    if not os.path.exists(os.path.join(dirname, f"build/content/projects/{all_project_templates[0][i][0]}")):
        os.mkdir(f'{d}/build/content/projects/{all_project_templates[0][i][0]}')
    with open(f'{d}/build/content/projects/{all_project_templates[0][i][0]}/{all_project_templates[0][i][0]}.html', "w+") as f:
        f.write(all_project_templates[0][i][1])

### first number specifies the format, second determines the topic###
compiled_404 = generator.replace_single_tag(_404_template, "{%STYLE%}", style)
with open(os.path.join(d, "build/404.html"), "w+") as f:
    f.write(compiled_404)

blogs_page = "".join(all_blog_templates[1])
finished_blogs_page = generator.replace_single_tag(blogs_template, "{%POSTS%}", blogs_page)

with open(os.path.join(d, "build/blogs.html"), "w+") as f:
    f.write(finished_blogs_page)

projects_page = "".join(all_project_templates[1])
finished_projects_page = generator.replace_single_tag(projects_template, "{%PROJECTS%}", projects_page)

with open(os.path.join(d, "build/projects.html"), "w+") as f:
    f.write(finished_projects_page)