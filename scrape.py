import re
from pathlib import Path

import pytumblr
import yaml
from ebooklib import epub
from tqdm import tqdm

blog_id = "docfuture"


# TODO: support for sequels + other related posts
def get_client():
    yaml_path = Path.home() / ".tumblr"

    with open(yaml_path, "r") as yaml_file:
        tokens = yaml.safe_load(yaml_file)

    client = pytumblr.TumblrRestClient(
        tokens["consumer_key"],
        tokens["consumer_secret"],
        tokens["oauth_token"],
        tokens["oauth_token_secret"],
    )
    return client


def get_toc(client):
    # https://docfuture.tumblr.com/post/82363551272/fall-of-doc-future-contents
    print("Fetching TOC...")
    toc_post = client.posts(blog_id, id="82363551272")["posts"][0]
    toc_body = toc_post["body"]
    # extract links out of post body
    pattern = re.compile(
        r'href="http://docfuture.tumblr.com/post/(\d+)/[^"]*"\s*target="_blank">([^<]+)</a>'
    )
    matches = pattern.findall(toc_body)
    posts_dict = {int(post_id): link_text for post_id, link_text in matches}

    return posts_dict


def get_post_content(client, post_id):
    # Fetches the content of a single post by its ID
    post = client.posts(blog_id, id=str(post_id))["posts"][0]
    try:
        # Assumes the post is in HTML format
        content = post["body"]
    except KeyError:
        # Fallback for posts without a 'body' field, e.g., photo or video posts
        content = "<h1>Content not available</h1>"
    return content


def create_epub(client, posts_dict):
    book_id = "docfuture"  # TODO: support other books
    # Initialize the EPUB book
    book = epub.EpubBook()
    book.set_identifier(book_id)
    # TODO: get name from TOC
    book.set_title("The Fall of Doc Future")
    book.set_language("en")
    book.add_author("W. Dow Rieder")

    # List to hold all the chapter objects for the EPUB's TOC
    chapters = []

    print("Fetching posts...")
    for post_id, title in tqdm(posts_dict.items(), unit="post"):
        # Fetch post content
        content = get_post_content(client, post_id)

        # Create an EPUB chapter
        chapter = epub.EpubHtml(title=title, file_name=f"{post_id}.xhtml", lang="en")
        chapter.content = content

        # Add chapter to the book and TOC list
        book.add_item(chapter)
        chapters.append(chapter)

    # Define book structure
    book.toc = chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define the book spine
    book.spine = ["nav"] + chapters

    # Write the EPUB file
    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)
    epub_path = output_path / f"{book_id}.epub"
    print(f"Writing {epub_path}...")
    epub.write_epub(epub_path, book, {})


def main():
    client = get_client()
    toc = get_toc(client)
    print(toc)

    # Create and save the EPUB
    create_epub(client, toc)


if __name__ == "__main__":
    main()
