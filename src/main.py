from markdown_blocks import markdown_to_html_node
from helpers import extract_title
from pathlib import Path

import os
import shutil

def copy_directory_contents(source_dir, destination_dir):
    if os.path.isfile(source_dir):
        shutil.copy(source_dir, destination_dir)
        print(destination_dir)
        return
    
    content_list = os.listdir(source_dir)
    os.mkdir(destination_dir)
    for content in content_list:
        copy_directory_contents(os.path.join(source_dir, content), os.path.join(destination_dir, content))
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        from_path_content = file.read()
    with open(template_path, "r", encoding="utf-8") as file:
        template_path_content = file.read()
    
    html_string = markdown_to_html_node(from_path_content).to_html()
    page_title = extract_title(from_path_content)

    new_template_path_content = template_path_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)
    dir_name = os.path.dirname(dest_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(new_template_path_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)




def main():
    # text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node.__repr__())
    # print(copy_directory_contents("../static/images"))

    destination_path = os.path.expanduser("~/static-site-generator/public")
    source_path = os.path.expanduser("~/static-site-generator/static")
    from_path = os.path.expanduser("~/static-site-generator/content/")
    template_path = os.path.expanduser("~/static-site-generator/template.html")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    
    copy_directory_contents(source_path, destination_path)
    generate_pages_recursive(from_path, template_path, destination_path)
    print(from_path)
    


main()
