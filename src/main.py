from textnode import TextNode, TextType
from to_node import markdown_to_html_node
import re
import os
import shutil

source_path = "static/"
target_path = "public/"
markdown_path = "content/"
template_path = "./template.html"

def to_public():
    #Clear target file directory
    shutil.rmtree(target_path)
    os.mkdir(target_path)

    #Get source file directory
    full_path_list = get_path(source_path)

    for full_path in full_path_list:
        target = os.path.join(target_path, full_path[7:])
        shutil.copy(full_path, target)



def get_path(path, file = None):
    if file == None:
        file_list = os.listdir(path)
        if len(file_list) == 0:
            return []
        else:
            return get_path(path, file_list)
    else:
        file_path = []
        for f in file:
            if os.path.isfile(os.path.join(path,f)):
                file_path.append(os.path.join(path,f))
            else:
                new_path = os.path.join(path,f)
                os.mkdir(os.path.join(target_path, new_path[7:]))
                file_path += get_path(new_path, os.listdir(new_path))
        return file_path


def get_path_and_not_mkdir(path, file = None):
    if file == None:
        file_list = os.listdir(markdown_path)
        if len(file_list) == 0:
            return []
        else:
            return get_path(path, file_list)
    else:
        file_path = []
        for f in file:
            if os.path.isfile(os.path.join(path,f)):
                file_path.append(os.path.join(path,f))
            else:
                new_path = os.path.join(path,f)
                file_path += get_path(new_path, os.listdir(new_path))
        return file_path


def extract_title(markdown):
    target_text = re.match("^# (.*?)\n", markdown)
    if not target_text:
        raise Exception("not Title")
    else:
        return target_text.group(1).strip()
    
def generate_page(from_path, template_path, dest_path):
    print("Generating page from from_path to dest_path using template_path")
    markdown = ""
    template = ""
    with open(f"{from_path}", "r") as file:
        markdown = file.read()
    
    with open(f"{template_path}", "r") as file:
        template = file.read()
    
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(f"{dest_path}", "w") as file:
        file.write(template)



def main():
    to_public()
    generate_page("content/index.md", template_path, "public/index.html")

    print("ok")
main()
