import os
from shutil import copyfile

from jinja2 import Environment, select_autoescape, FileSystemLoader


def main():
    os.makedirs("prototype/_site", exist_ok=True)
    copyfile("prototype/templates/app.css", "prototype/_site/app.css")

    env = Environment(
        loader=FileSystemLoader("prototype/templates"),
        autoescape=select_autoescape()
    )

    template_files = [file for file in os.listdir("prototype/templates") if not file.startswith("_")]

    for file in template_files:
        template = env.get_template(file)
        rendered_template = template.render()

        with open(f"prototype/_site/{file}", "w") as opened_file:
            opened_file.write(rendered_template)


if __name__ == "__main__":
    main()
