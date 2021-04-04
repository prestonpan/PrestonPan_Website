#!/usr/bin/python
### static assembly template generator, or SATG ###
### html adjacent language = SATL or static assembly template language ###
import os
import re
from pathlib import Path
import shutil


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

with open((TEMPLATE_PATH / 'item_overview.html').resolve(), "r") as f:
    item_overview_template_project = f.read()
  
with open((TEMPLATE_PATH / "item_total_overview.html").resolve(), "r") as f:
    item_total_overview_template = f.read()

with open((TEMPLATE_PATH / "item_total_overview.html").resolve(), 'r') as f:
    item_total_overview_template_project = f.read()

with open((TEMPLATE_PATH / "index.html").resolve(), "r") as f:
    index_template = f.read()

with open((TEMPLATE_PATH / "404.html").resolve(), "r") as f:
    _404_template = f.read()

with open((TEMPLATE_PATH / "rss.xml").resolve(), "r") as f:
    rss = f.read()
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
        'picture': "content/blog/Minimalism/Minimalism.webp",
        'link': "content/blog/Minimalism/Minimalism.html",
        'path': os.path.join(dirname, "content/blog/Minimalism/Minimalism.html"),
    }, 
    {
        'name': "Privacy",
        'description': "My thoughts on surveillance.",
        'picture': "content/blog/Privacy/Privacy.webp",
        'link': "content/blog/Privacy/Privacy.html",
        'path': os.path.join(dirname, "content/blog/Privacy/Privacy.html"),
    },
    {
        'name': "First Blog",
        'description': "My first ever blog on my own site.",
        'picture': "content/blog/First_Blog/First_Blog.webp",
        'link': "content/blog/First_Blog/First_Blog.html",
        'path': os.path.join(dirname, "content/blog/First_Blog/First_Blog.html"),
    },
]

project = [
    3, ### The number of templates ###
    { ### TEMPLATE 1, None means the key will be ignored by the compiler ###
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'path': "f{%MAIN_CONTENT%}", 
        'picture': None,
        'git': "{%GIT_REPO%}",
        'template': project_template,
    },
    { ### TEMPLATE 2 ###
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'link': "{%ITEM_PATH%}",
        'path': None,
        'picture': "{%PICTURE%}",
        'git': None,
        'template': item_total_overview_template_project,
    },
    { ### TEMPLATE 3 ###
        'name': "{%TITLE%}",
        'description': "{%DESCRIPTION%}",
        'path': None,
        'link': "{%ITEM_PATH%}",
        'picture': "{%PICTURE%}",
        'git': None,
        'template': item_overview_template_project,
    },
    {
        'name': "My Dotfiles",
        'description': "My minimal linux dotfiles.",
        'path': os.path.join(dirname, "content/projects/My_Dotfiles/My_Dotfiles.html"),
        'link': "content/projects/My_Dotfiles/My_Dotfiles.html", 
        'picture': "content/projects/My_Dotfiles/My_Dotfiles.webp",
        'git': "git://prestonpan.tech/dotfiles.git",
    },
    {
        'name': "PrestonPan Website",
        'description': "My amazing website.",
        'path': os.path.join(dirname, "content/projects/PrestonPan_Website/PrestonPan_Website.html"),
        'link': "content/projects/PrestonPan_Website/PrestonPan_Website.html", 
        'picture': "content/projects/PrestonPan_Website/PrestonPan_Website.webp",
        'gitlab': "git://prestonpan.tech/prestonpan.git",
    },
    {
        'name': "NoExcess",
        'description': "An elegant, and frankly useless compiled programming language.",
        'path': os.path.join(dirname, "content/projects/NoExcess/NoExcess.html"),
        'link': "content/projects/NoExcess/NoExcess.html", 
        'picture': "content/projects/NoExcess/NoExcess.webp",
        'gitlab': "git://prestonpan.tech/NoExcess.git",
    },
]

### TODO: automatic json generation ###

### ATTEMPTING TO MAKE A CLASS ###
class SATG:
    def __init__(self, data):
        self.data = data
                
    def build_dataset(self):
        all_fragments = []
        dicts = self.data
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
                debug_var = [dicts[j]["name"].replace(" ", "_"), template]
                fragments.append(debug_var) ### outside the loop which replaces everything.###
            all_fragments.append(fragments)
        return all_fragments


            
    @staticmethod
    def replace_single_tag(fragment, tag, text):
        if tag[0] == 'f':
            with open(text, "r") as f:
                e = f.read()
        else:
            e = text
        return fragment.replace(tag, e)

generator1 = SATG(blog)
generator2 = SATG(project)
all_blog_templates = generator1.build_dataset()
all_project_templates = generator2.build_dataset()
for i in range(len(all_blog_templates)):
    for j in range(len(all_blog_templates[i])):
        all_blog_templates[i][j][1] = generator1.replace_single_tag(all_blog_templates[i][j][1], "{%STYLE%}", style)

for i in range(len(all_project_templates)):
    for j in range(len(all_blog_templates[i])):
        all_project_templates[i][j][1] = generator2.replace_single_tag(all_project_templates[i][j][1], "{%STYLE%}", style)

# d = os.path.dirname(dirname)

# making needed folders and removing the last build
if os.path.exists(os.path.join(dirname, 'build')):
    shutil.rmtree(os.path.join(dirname, 'build'))
os.mkdir(os.path.join(dirname, 'build'))
os.mkdir(os.path.join(dirname, 'build/content'))
os.mkdir(os.path.join(dirname, 'build/content/projects'))
os.mkdir(os.path.join(dirname, 'build/content/blog'))


for i in range(len(all_blog_templates[0])):
    # if not os.path.exists(os.path.join(dirname, f"build/content/blog/{all_blog_templates[0][i][0]}")):
    os.mkdir(f'{dirname}/build/content/blog/{all_blog_templates[0][i][0]}')
    with open(f'{dirname}/build/content/blog/{all_blog_templates[0][i][0]}/{all_blog_templates[0][i][0]}.html', "w+") as f:
        f.write(all_blog_templates[0][i][1])

for i in range(len(all_project_templates[0])):
    # if not os.path.exists(os.path.join(dirname, f"build/content/projects/{all_project_templates[0][i][0]}")):
    os.mkdir(f'{dirname}/build/content/projects/{all_project_templates[0][i][0]}')
    with open(f'{dirname}/build/content/projects/{all_project_templates[0][i][0]}/{all_project_templates[0][i][0]}.html', "w+") as f:
        f.write(all_project_templates[0][i][1])

### first number specifies the format, second determines the topic###
compiled_404 = generator1.replace_single_tag(_404_template, "{%STYLE%}", style)
with open(os.path.join(dirname, "build/404.html"), "w+") as f:
    f.write(compiled_404)
### BLOGS PAGE ASSEMBLY###
blogs_page_all_content = [i[1] for i in all_blog_templates[1]]
blogs_page = "".join(blogs_page_all_content)
blogs_page_ = generator1.replace_single_tag(blogs_template, "{%POSTS%}", blogs_page)
finished_blogs_page = generator1.replace_single_tag(blogs_page_, "{%STYLE%}", style)
with open(os.path.join(dirname, "build/posts.html"), "w+") as f:
    f.write(finished_blogs_page)

### PROJECTS PAGE ASSEMBLY###
projects_page_all_content = [i[1] for i in all_project_templates[1]]
projects_page = "".join(projects_page_all_content)
projects_page_ = generator2.replace_single_tag(projects_template, "{%PROJECTS%}", projects_page)
finished_projects_page = generator2.replace_single_tag(projects_page_, "{%STYLE%}", style)
with open(os.path.join(dirname, "build/projects.html"), "w+") as f:
    f.write(finished_projects_page)

### ASSEMBLY OF INDEX.HTML PROJECTS SECTION ###
project1 = all_project_templates[2][0][1]
project2 = all_project_templates[2][1][1]
project3 = all_project_templates[2][2][1]
# print(project1, project2, project3)

finished_index_template1 = generator1.replace_single_tag(index_template, "{%PROJECT1%}", project1)
# print(finished_index_template1)
# print(all_project_templates[2])
finished_index_template2 = generator1.replace_single_tag(finished_index_template1, "{%PROJECT2%}", project2)
finished_index_template3 = generator1.replace_single_tag(finished_index_template2, "{%PROJECT3%}", project3)
### ASSEMBLY OF INDEX.HTML BLOG SECTION ###
blog1 = all_blog_templates[2][0][1]
blog2 = all_blog_templates[2][1][1]
blog3 = all_blog_templates[2][2][1]
finished_index_template4 = generator1.replace_single_tag(finished_index_template3, "{%BLOG1%}", blog1)
finished_index_template5 = generator1.replace_single_tag(finished_index_template4, "{%BLOG2%}", blog2)
finished_index_template6 = generator1.replace_single_tag(finished_index_template5, "{%BLOG3%}", blog3)

finished_index_template = generator1.replace_single_tag(finished_index_template6, "{%STYLE%}", style)
# print(finished_index_template)
with open(os.path.join(dirname, "build/index.html"), "w+") as f: 
    f.write(finished_index_template)

# copies all non template files into build dir
for di in range(project[0] + 1, len(project)):
    dic_p = project[di]
    loop_dir_p = os.path.dirname(os.path.join(dirname, dic_p['picture']))
    for i in os.listdir(loop_dir_p):
        name_p = dic_p['name'].replace(" ", "_") + '.html'
        if i != name_p:
            shutil.copyfile(os.path.join(loop_dir_p, i), os.path.join(dirname, "build/content/projects", os.path.basename(loop_dir_p), i))

for di in range(blog[0] + 1, len(blog)):
    dic = blog[di]
    loop_dir = os.path.dirname(os.path.join(dirname, dic['picture']))
    for i in os.listdir(loop_dir):
        name = dic['name'].replace(" ", "_") + '.html'
        if i != name:
            shutil.copyfile(os.path.join(loop_dir, i), os.path.join(dirname, "build/content/blog", os.path.basename(loop_dir), i))

### Copy fonts dir ###
shutil.copytree(os.path.join(dirname, 'fonts'), os.path.join(dirname, 'build/fonts'))
### Copy img dir ###
shutil.copytree(os.path.join(dirname, "img"), os.path.join(dirname, "build/img"))
### Generate RSS feed ###
