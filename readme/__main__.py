from jinja2 import Environment, FileSystemLoader, select_autoescape
from .utils.zenn import fetch_articles
from datetime import datetime


env = Environment(
    loader=FileSystemLoader("readme/templates"), autoescape=select_autoescape()
)
template = env.get_template("README.md")


def update_readme() -> None:
    dt = datetime.now()
    articles = fetch_articles()
    with open("README.md", "w") as f:
        f.write(
            template.render(
                articles=articles[:5], last_updated=dt.strftime("%Y/%m/%d %H:%M:%S.%f")
            )
        )


if __name__ == "__main__":
    update_readme()
