import os
from pathlib import Path
import shutil
from datetime import datetime

class SATG:
    def __init__(self, templates, templates_dir, data): 
        # will be a list of template dictionaries
        self.templates = templates
        self.templates_dir = templates_dir
        # will be a dictionary with the file name colon the content
        self.template_files = self.generate_template_files(self.templates_dir)
        # directory of template files        
        self.data = data
        self.processed_templates = self.build_dataset()
    
    @staticmethod
    def generate_template_files(templates_dir):
        templates = {}
        for f in os.listdir(templates_dir):
            f_dir = os.path.join(templates_dir, f)
            with open(f_dir, "r") as fi:
                f_contents = fi.read()
            templates[f] = f_contents
        return templates

    def build_dataset(self):
        all_fragments = []
        dicts = [len(self.templates)]
        dicts.extend(self.templates)
        dicts.extend(self.data)
        for i in range(1, dicts[0] + 1):
            keys = list(dicts[i].keys())
            fragments = []
            for j in range(dicts[0] + 1, len(dicts)):
                template = self.template_files[dicts[i]['template']]
                for key in keys[:-1]:
                    if key == 'template':
                        continue
                    tag = dicts[i][key]
                    content = dicts[j][key]
                    if tag is None:
                        continue
                    elif tag[0] == "f":
                        with open(content, 'r') as f:
                            fragment = f.read()
                        template = template.replace(tag, fragment)
                    else:
                        template = template.replace(tag, content) 
                fragments.append([dicts[j]['name'].replace(" ", "_"), template])
            all_fragments.append(fragments)
        return all_fragments
    
    def replace_tag_for_all(self, tag, text, is_template=True):
        for i in self.processed_templates:
            for j in i:
                j[1] = self.replace_single_tag(j[1], tag, text)
        for key in self.template_files:
            self.template_files[key] = self.replace_single_tag(self.template_files[key], tag, text, is_template)
 
    def replace_single_tag(self, fragment, tag, text, is_template=True):
        if tag[0] == 'f' and not is_template:
            with open(text, "r") as f:
                e = f.read()
        elif is_template:
            e = self.template_files[text]
        else:
            e = text
        return fragment.replace(tag, e)


def generate_dataset_project(current_path, projects_path):
    projects = []
    for dirname in os.listdir(projects_path):
        project = {} 
        project['name'] = dirname.replace("_", " ")
        project['path'] = os.path.join(current_path, f'content/projects/{dirname}/{dirname}.html') 
        project['link'] = f"content/projects/{dirname}/{dirname}.html"
        project['picture'] = f"content/projects/{dirname}/{dirname}.webp"
        project['git'] = f'git://prestonpan.tech/{dirname}.git'
        date = datetime.fromtimestamp(os.path.getmtime(project['path'])).strftime('%d-%m-%Y')
        project['date'] = date
        with open(os.path.join(current_path, f'content/projects/{dirname}/description.txt'), 'r') as f:
            project['description'] = f.read()
        projects.append(project)
    
    projects.sort(reverse=True, key = lambda di: datetime.strptime(di['date'], '%d-%m-%Y'))
    return projects


def generate_dataset_blog(current_path, blogs_path):
    blogs = []
    for dirname in os.listdir(blogs_path):
        blog = {}
        blog['name'] = dirname.replace("_", " ")
        blog['path'] = os.path.join(current_path, f'content/blog/{dirname}/{dirname}.html')
        blog['link'] = f"content/blog/{dirname}/{dirname}.html"
        blog['picture'] = f"content/blog/{dirname}/{dirname}.webp"
        with open(os.path.join(current_path, f'content/blog/{dirname}/description.txt'), "r") as f:
            blog['description'] = f.read()
        date = datetime.fromtimestamp(os.path.getmtime(blog['path'])).strftime('%d-%m-%Y')
        blog['date'] = date
        blogs.append(blog)
    blogs.sort(reverse=True, key = lambda di: datetime.strptime(di['date'], '%d-%m-%Y'))
    return blogs


if __name__ == '__main__':
    ### GLOBALS ###
    dirname = os.path.dirname(__file__)
    
    # deleting and recreating the build directory
    if os.path.exists(os.path.join(dirname, 'build')):
        shutil.rmtree(os.path.join(dirname, 'build'))
    os.mkdir(os.path.join(dirname, 'build'))
    os.mkdir(os.path.join(dirname, 'build/content'))
    os.mkdir(os.path.join(dirname, 'build/content/projects'))
    os.mkdir(os.path.join(dirname, 'build/content/blog'))
   
    ### GENERATION OF PROJECT TEMPLATES ###
    project_templates = [
        {
            'name': "{%TITLE%}",
            'description': "{%DESCRIPTION%}",
            'link': None,
            'path': "f{%MAIN_CONTENT%}",
            'picture': None,
            'git': "{%GIT_REPO%}",
            'template': 'project.html',
            'date': None
        },
        {
            'name': "{%TITLE%}",
            'description': '{%DESCRIPTION%}',
            'link': "{%ITEM_PATH%}",
            'path': None,
            'picture': "{%PICTURE%}",
            'git': None,
            "template": 'item_total_overview.html', 
            "date": None,
        },
        {
            'name': "{%TITLE%}",
            'description': "{%DESCRIPTION%}",
            'link': "{%ITEM_PATH%}",
            'path': None,
            'picture': "{%PICTURE%}",
            'git': None,
            'template': 'item_overview.html',
            'date': None,
        },
    ]

    ### BUILDING FROM PROJECTS DATASET ###
    projects_gen = SATG(
            project_templates, 
            os.path.join(dirname, 'templates'), 
            generate_dataset_project(dirname, os.path.join(dirname, "content/projects"))
    )
    projects_gen.replace_tag_for_all("{%STYLE%}", 'style.html')
    project_templates = projects_gen.processed_templates
    
    for i in range(len(project_templates[0])):
        os.mkdir(os.path.join(dirname, f'build/content/projects/{project_templates[0][i][0]}'))
        with open(os.path.join(dirname, f'build/content/projects/{project_templates[0][i][0]}/{project_templates[0][i][0]}.html'), 'w') as f:
            f.write(project_templates[0][i][1])

    projects_page_all_content = ''.join([i[1] for i in project_templates[1]])
    projects_page = projects_gen.replace_single_tag(
            projects_gen.template_files['projects.html'], 
            "{%PROJECTS%}", 
            projects_page_all_content, 
            False
    )
    with open(os.path.join(dirname, 'build/projects.html'), "w+") as f:
        f.write(projects_page)
   
    ### BLOG DATASET ASSEMBLY ###
    blog_templates = [
        {
            'name': "{%TITLE%}",
            'description': '{%DESCRIPTION%}',
            'picture': None,
            'link': None,
            'path': "f{%MAIN_CONTENT%}",
            'template': 'post.html',
            'date': None,
        },
        {
            'name': '{%TITLE%}',
            'description': "{%DESCRIPTION%}",
            'picture': "{%PICTURE%}",
            'link': "{%ITEM_PATH%}",
            'path': None,
            'template': 'item_total_overview.html',
            'date': None,
        },
        {
            'name': "{%TITLE%}",
            'description': "{%DESCRIPTION%}",
            'picture': '{%PICTURE%}',
            'link': "{%ITEM_PATH%}",
            'path': None,
            'template': 'item_overview.html',
            'date': None,
        },
    ]
    blogs_gen = SATG(
        blog_templates,
        os.path.join(dirname, "templates"),
        generate_dataset_blog(dirname, os.path.join(dirname, 'content/blog'))
    )
    blogs_gen.replace_tag_for_all("{%STYLE%}", 'style.html')
    blog_templates = blogs_gen.processed_templates

    for i in range(len(blog_templates[0])):
        os.mkdir(os.path.join(dirname, f'build/content/blog/{blog_templates[0][i][0]}'))
        with open(os.path.join(dirname, f'build/content/blog/{blog_templates[0][i][0]}/{blog_templates[0][i][0]}.html'), 'w') as f:
            f.write(blog_templates[0][i][1])

    blogs_page_all_content = ''.join([i[1] for i in blog_templates[1]])
    blogs_page = blogs_gen.replace_single_tag(
            blogs_gen.template_files['posts.html'], 
            "{%POSTS%}", 
            blogs_page_all_content, 
            False
    )
    with open(os.path.join(dirname, 'build/posts.html'), "w+") as f:
        f.write(blogs_page)
 
    ### GENERAL PAGE ASSEMBLY ###
    
    # 404 page
    with open(os.path.join(dirname, "build/404.html"), "w+") as f:
        f.write(projects_gen.template_files['404.html'])
    
    # index page
    index_projects = project_templates[2][0][1] + project_templates[2][1][1] + project_templates[2][2][1]
    index_template = projects_gen.replace_single_tag(
            projects_gen.template_files['index.html'], 
            "{%PROJECTS%}",
            index_projects,
            False
    )
    index_blogs = blog_templates[2][0][1] + blog_templates[2][1][1] + blog_templates[2][2][1]
    index_template = blogs_gen.replace_single_tag(
            index_template,
            "{%BLOGS%}",
            index_blogs,
            False
    )

    with open(os.path.join(dirname, 'build/index.html'), 'w+') as f:
        f.write(index_template)
    
    # TODO: atom feed
    ### - Make new blog/project template for atom feed ###
    ### generate the feed like the index page ###
    ### write to atom.xml ###

    ### COPY IMPORTANT DIRS (fonts, img, etc...) ###
    
    # copy stuff from content/projects
    for dname in os.listdir(os.path.join(dirname, 'content/projects')):
        
        # webp image
        shutil.copyfile(
            os.path.join(dirname, 'content/projects', dname, f'{dname}.webp'),
            os.path.join(dirname, 'build/content/projects', dname, f'{dname}.webp')
        )
        
        # img folder
        shutil.copytree(
                os.path.join(dirname, 'content/projects', dname, 'img'), 
                os.path.join(dirname, 'build/content/projects', dname, 'img')
        )
    
    # copy stuff from content/build
    for dname in os.listdir(os.path.join(dirname, 'content/blog')):
        
         # webp image 
        shutil.copyfile(
                os.path.join(dirname, 'content/blog', dname, f'{dname}.webp'),
                os.path.join(dirname, 'build/content/blog', dname, f"{dname}.webp" )
        )

        # img folder
        shutil.copytree(
                os.path.join(dirname, 'content/blog', dname, 'img'), 
                os.path.join(dirname, 'build/content/blog', dname, 'img')
        )
    
    # copy stuff from content/
    shutil.copytree(os.path.join(dirname, 'fonts'), os.path.join(dirname, 'build/fonts'))
    shutil.copytree(os.path.join(dirname, 'img'), os.path.join('build/img'))
    shutil.copyfile(os.path.join(dirname, 'robots.txt'), os.path.join(dirname, 'build/robots.txt'))
