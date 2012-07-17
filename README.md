Trello Mercurial Hook
=====================

By adding this hook, every commit with a card number hashtag (eg. #345) will add a comment with changeset details of this commit.

Usage
-----

Change the correct parameters for you trello board:

* TRELLO_BOARD -- THe id of your board, found in the URL when viewing your board
* TRELLO_KEY -- Generate a key on the [trello key generation](https://trello.com/1/appKey/generate) page, while being logged in
* TRELLO_TOK_READ -- A read token, in your browser go to this URL and accept: `https://trello.com/1/authorize?key=[TRELLO_KEY]&name=[CHOOSE_APP_NAME]&expiration=never&response_type=token`
You'll find your key on the next page.
* TRELLO_TOK_WRITE -- A write token, in your browser go to this URL and accept: `https://trello.com/1/authorize?key=[TRELLO_KEY]&name=[CHOOSE_APP_NAME]&expiration=never&response_type=token&scope=read,write`
You'll find your key on the next page.

Once you changed your credentials you can configure the script as a hook:

* Go to your .hg/hgrc file and add this line under the [hooks] section: `pretxncommit.trello = python:/path/to/trello.py:comment_changeset`