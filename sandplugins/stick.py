from sand.plugin import SandPlugin
import re
import os

VERSION = "2024.10.1.1"
CHAPTER_PATTERN = re.compile(r"project/chapters/(.+)\.md")
CLEAN_BITS = re.compile(r"[-_+.]+")


def standard_page(site, content, path):
    page_dict = {'source': None, 'target': path,
                 "config": {
                     "static_content": content,
                     "template": "page.html"}
                 }
    site.add_page(page_dict)

def index_page(site):
    index_dict = {'source': None, 'target': "./index.html",
                  "config": {
                      "static_content": "",
                      "template": "index.html"}
                  }
    site.add_page(index_dict)

def clean_title(chapter_source):
    filename_minus_ext = CHAPTER_PATTERN.findall(chapter_source)[0]
    return CLEAN_BITS.sub(" ", filename_minus_ext).capitalize()


class Plugin(SandPlugin):
    def __init__(self):
        super().__init__()
        self.chapters = []
        self.site = None

    def version(self):
        return VERSION

    def word_count(self, content):
        if content is None:
            return 0
        return len(content.split(" "))

    def configure(self, site_data, site):
        self.site = site

    def parse(self, site_data, site):
        self.chapters = [page for page in site.pages if CHAPTER_PATTERN.match(page.source)]
        for chapter in self.chapters:
           chapter.title = clean_title(chapter.source)
        stitched_book = "\n\n".join([c.raw_content for c in self.chapters])
        standard_page(site, stitched_book, "./project.html")
        index_page(site)

    def add_render_context(self, page, environment, data):
        data["S"] = {
            "version": VERSION,
            "word_count": self.word_count(page.raw_content),
            "chapters": self.chapters
        }
