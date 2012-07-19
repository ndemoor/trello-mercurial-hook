Trello Mercurial Hook
=====================

By adding this hook, every commit with a card number hashtag (eg. #345) will add a comment with changeset details of this commit.

Usage
-----

### Enable hook

- Put the src/trello.py script somewhere outside of your project document
- Open the .hg/hgrc document of the repository where you want to use this hook
- Under the <code>[hooks]</code> section add `pretxncommit.trello = python:/path/to/trello.py:comment_changeset`

### Configure hook

Now create a <code>[trello]</code> section and configure your board specific settings:

- <code>user</code>: Your trello username (put an @ in front to get notifications)
- <code>board</code>: The id of your board (found in the URL when viewing your Trello board)
- <code>key</code>: Generate a key on the [Trello key generation page](https://trello.com/1/appKey/generate), while being logged in
- <code>token_read</code>: A read token, in your browser go to this URL and accept: <code>https://trello.com/1/authorize?key=[TRELLO_KEY]&name=[CHOOSE_APP_NAME]&expiration=never&response_type=token</code> You'll find your key on the next page.
- <code>token_write</code>: A write token, in your browser go to this URL and accept: <code>https://trello.com/1/authorize?key=[TRELLO_KEY]&name=[CHOOSE_APP_NAME]&expiration=never&response_type=token&scope=read,write</code> You'll find your key on the next page.