import json
import random
import shutil
import os
import re
import string
import subprocess
from urllib.parse import urlparse
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.codehilite import CodeHiliteExtension
import stat

classes = {}
ids = {}

class Compiler:
    def __init__(self, contents, destination=None):
        self.contents = contents
        self.destination = destination

    def condense_html(self):
        # self.contents = self.contents.replace('\n', ' ')
        # self.contents = self.contents.replace('  ', ' ')
        # self.contents = self.contents.replace('  ', ' ')
        # self.contents = self.contents.replace('  ', ' ')
        # self.contents = self.contents.replace('/> <', '/><')
        pass

    def random_string(self, length=6):
        return random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))

    def class_list(self):
        class_pattern = re.compile(r'class="([^"]+)"')
        matches = class_pattern.findall(self.contents)
        for match in matches:
            if match not in classes:
                classes[match] = self.random_string()
        for key, value in classes.items():
            self.contents = self.contents.replace(f'class="{key}"', f'class="{value}"')
            self.contents = self.contents.replace(f'.{key}', f'.{value}')
    
    def id_list(self):
        id_pattern = re.compile(r'id="([^"]+)"')
        matches = id_pattern.findall(self.contents)
        for match in matches:
            if match not in ids:
                ids[match] = self.random_string()
        for key, value in ids.items():
            self.contents = self.contents.replace(f'id="{key}"', f'id="{value}"')
            self.contents = self.contents.replace(f'#{key}', f'#{value}')

    def encrypt_html(self):
        self.class_list()
        self.id_list()
        self.condense_html()

    def apply_include_rule(self):
        include_pattern = re.compile(r'<INCLUDE src="([^"]+)" ?\/>')
        matches = include_pattern.findall(self.contents)

        for match in matches:
            file = File(f"source/{match}")
            self.contents = self.contents.replace(f'<INCLUDE src="{match}"/>', file.contents)

    def apply_wrap_rule(self):
        embed_pattern = re.compile(r'<WRAP type="([^"]+)"/>')
        matches = embed_pattern.findall(self.contents)
        self.contents = re.sub(r'<WRAP type="[^"]+"/>', '', self.contents)
        if(len(matches) == 0): return
        
        self.apply_template(matches[0])
    
    def extract_meta_tags(self):
        # Regex to match <META> tags and capture key-value pairs
        meta_pattern = re.compile(r'<META\s+([^>]+)\/>')
        attribute_pattern = re.compile(r'(\w+)="([^"]+)"')

        meta_tags = meta_pattern.findall(self.contents)
        meta_dict = {}

        for tag in meta_tags:
            attributes = attribute_pattern.findall(tag)
            for key, value in attributes:
                meta_dict[key] = value

        self.contents = re.sub(meta_pattern, '', self.contents)

        return meta_dict

    def apply_template(self, template):
        tags = self.extract_meta_tags()

        self.contents = markdown.markdown(self.contents, extensions=[TableExtension(), 'fenced_code'])

        # Regex to match <img> tags with any attributes
        img_pattern = re.compile(r'<p>(<img[^>]+/>)</p>')
        self.contents = re.sub(img_pattern, r'\1', self.contents)

        wrapper = File(f'source\\templates\\{template}.html')
        wrapper.contents = wrapper.contents.replace('<CONTENT/>', self.contents)
        self.contents = wrapper.contents

        for key, value in tags.items():
            self.contents = self.contents.replace(f'<PARAM type="{key}"/>', value)
        if self.destination is not None:
            self.destination = self.destination.replace('.md', '.html')
        
    def apply_rules(self):
        self.contents = self.contents.replace(' />', '/>')
        self.apply_include_rule()
        self.apply_wrap_rule()
        self.encrypt_html()
        return self.destination

class File:
    contents: str
    dependencies: list
    src_path: str
    dst_path: str

    def __init__(self, src_path, dst_path=None):
        self.src_path = src_path
        self.dst_path = dst_path
        print("Reading file from", src_path)
        self.read()
        self.compile()
        self.compose_dependencies()
        
    def save(self, dst_path=None):
        if dst_path is None:
            dst_path = self.dst_path
        print(f"Copying file from {self.src_path} to {dst_path}")
        with open(dst_path, 'w') as file:
            file.write(self.contents)
        for dependency in self.dependencies:
            dependency = dependency.replace('/', '\\')
            print(f"Copied dependency from {dependency} to {dependency.replace('source\\', 'build\\')}")
            shutil.copy(dependency, dependency.replace('source\\', 'build\\'))
    
    def read(self):
        with open(self.src_path, 'r') as file:
            self.contents = file.read()
    
    def compose_dependencies(self):
        # Regular expression to find relative paths
        path_pattern = re.compile(r'(?i)((?:[a-zA-Z]+(?:\/?[a-zA-Z]+)+)\.[a-zA-Z]+)', re.I)
        all_dependencies = re.findall(path_pattern, self.contents)

        src_root = os.path.dirname(self.src_path)

        source_folder = 'source'

        self.dependencies = []
        for dep in all_dependencies:
            relative_path = src_root + '\\' + dep
            global_path = source_folder + '\\' + dep

            if os.path.exists(relative_path):
                self.dependencies.append(relative_path)
            elif os.path.exists(global_path):
                self.dependencies.append(global_path)
        

    def compile(self):
        compiler = Compiler(self.contents, self.dst_path)
        self.dst_path = compiler.apply_rules()
        self.contents = compiler.contents


def read_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def handle_file(source, destination):
    if not source.split('.')[-1] in ['md', 'html']:
        return
    file = File(source, destination)
    file.save()


def handle_directory(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isfile(s):
            handle_file(s, d)
        elif os.path.isdir(s):
            handle_directory(s, d)

def is_github_repo_link(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme in ["http", "https"] and "github.com" in parsed_url.netloc:
        return True
    return False

def copy_files(config):
    for destination, source in config.items():
        source = source.replace('/', '\\')
        destination = destination.replace('/', '\\')

        if is_github_repo_link(source):
            print(f"Source {source} is a GitHub repository link.")
            subprocess.run(["git", "clone", source, "build\\" + destination], check=True)
            continue

        source = "source\\" + source
        destination = "build\\" + destination

        if(source[-1] == '*'):
            #copy the whole directory
            source = source[:-1]
            shutil.copytree(source, destination, dirs_exist_ok=True)

        if os.path.isfile(source):
            handle_file(source, destination)
        elif os.path.isdir(source):
            handle_directory(source, destination)

def handle_remove_readonly(func, path, exc_info):
    # Attempt to change the file permissions and retry the operation
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clear_build():
    if os.path.exists('build'):
        shutil.rmtree('build', onexc=handle_remove_readonly)
    os.makedirs('build')

if __name__ == "__main__":
    config_path = 'config.json'
    config = read_config(config_path)
    clear_build()
    copy_files(config)