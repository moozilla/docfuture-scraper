# docfuture-scraper
Python tumblr -> epub scraper for [docfuture.tumblr.com](https://docfuture.tumblr.com/).

The author of Doc Future [has commented](https://www.reddit.com/r/rational/comments/k873sy/comment/gf34ttf/) that they may publish the books commerically in the future, so please do not share the epubs created by this scraper publicly.

### Useful Links:
* [List of all Doc Future novels and other stories by W. Dow Rieder](https://docfuture.tumblr.com/post/62787551366/stories)
* https://riderius.dreamwidth.org/ - The author's new blog, has some revised chapters of Princess (not supported by this scraper yet)
* [pytumblr](https://github.com/tumblr/pytumblr)
* [EbookLib](https://github.com/aerkalov/ebooklib)
* [tumblr API reference](https://www.tumblr.com/docs/en/api/v2)
* [Lithium ebook reader](https://play.google.com/store/apps/details?id=com.faultexception.reader) (recommended ebook app for Android)

## Setup

### Install dependencies

* Make sure you have a valid python installation (tested on python 3.12)
* Create a virtual environment
```bash
python3.12 -m venv venv
source venv/bin/activate
```
* Install requirements
```bash
pip install -r requirements.txt
```

### Create tumblr API key

* Login/register to tumblr
* Create new application here: https://www.tumblr.com/oauth/register
    * Most options should be self-explanatory
    * For callback URL you can use any URL, I used [postbin](https://www.toptal.com/developers/postbin/)
* At https://www.tumblr.com/oauth/apps you can get your `OAuth Consumer Key` and `Secret Key`
* Create a file at `~/.tumblr` that looks like this:
```yaml
consumer_key: YOUR_CONSUMER_KEY_HERE
consumer_secret: YOUR_CONSUMER_SECRET_HERE
oauth_token: # not necessary
oauth_token_secret: # not necessary
```
(Note: if you want an oauth token/secret you can use the [interactive console script from pytumblr](https://github.com/tumblr/pytumblr/blob/master/interactive_console.py), but I don't think this is actually necessary for only reading posts)

## Running the scraper

```bash
python3 scrape.py
```

This will scrape each post and compile the contents into an epub under `output/docfuture.epub`.
