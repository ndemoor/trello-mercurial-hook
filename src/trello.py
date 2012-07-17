#!/usr/bin/env python

from mercurial import cmdutil, match, templater, util
import re
import urllib,urllib2
import json

TRELLO_BOARD        = "[YOUR_BOARD_ID]"
TRELLO_KEY          = "[YOUR_KEY]"
TRELLO_TOK_READ     = "[YOUR_READ_TOKEN]"
TRELLO_TOK_WRITE    = "[YOUR_WRITE_TOKEN]"

TRELLO_CARD_URL = "https://api.trello.com/1/boards/%s/cards/%s?key=%s&token=%s"
TRELLO_COMM_URL = "https://api.trello.com/1/cards/%s/actions/comments?key=%s&token=%s"

def comment_changeset(ui, repo, hooktype, node=None, source=None, **kwargs):
    for rev in xrange(repo[node], len(repo)):
        ctx = repo[rev]
        desc = ctx.description()

        cardNumbers = re.findall(r'#([0-9]+)', desc)

        try:
            num = cardNumbers[0]
            ui.status(" changeset: %s \n cardnumber: %s\n" % (ctx, num))

            try:
                resp = urllib2.urlopen(TRELLO_CARD_URL % (TRELLO_BOARD, num, TRELLO_KEY, TRELLO_TOK_READ))
                jsonStr = resp.read()
                data = json.loads(jsonStr)

                if ui.config('paths', 'default', False):
                    bitbUrl = ui.config('paths', 'default') + '/changeset/' + str(ctx)
                else:
                    bitbUrl = 'No default push path'

                params = urllib.urlencode({'text' : 'Commited changeset %s (%s)\nby: %s\nbranch: *%s* \n\n%s' % (ctx, ctx.rev(), ui.username(), ctx.branch(), bitbUrl)})
                req = urllib2.Request(TRELLO_COMM_URL % (data['id'], TRELLO_KEY, TRELLO_TOK_WRITE), params)
                
                resp = jsonStr = data = None
                resp = urllib2.urlopen(req)
                jsonStr = resp.read()
                data = json.loads(jsonStr)

                ui.status('Changeset comment posted to Trello card *%s*\n' % (data['data']['card']['name']))
            except urllib2.HTTPError, KeyError:
                ui.warn("Trello card number not found!\n")
            except:
                ui.warn("Something went wrong while adding trello comment, please check manually.\n")
        except IndexError:
            # No card number provided, do nothing
            pass
    return
