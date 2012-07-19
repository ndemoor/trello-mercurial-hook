#!/usr/bin/env python

from mercurial import cmdutil, match, templater, util
import re
import urllib,urllib2
import json

TRELLO_CARD_URL = "https://api.trello.com/1/boards/%s/cards/%s?key=%s&token=%s"
TRELLO_COMM_URL = "https://api.trello.com/1/cards/%s/actions/comments?key=%s&token=%s"

def comment_changeset(ui, repo, hooktype, node=None, source=None, **kwargs):
    TRELLO_USER = ui.config('trello', 'user', 'none')
    TRELLO_BOARD = ui.config('trello', 'board', False)
    TRELLO_KEY = ui.config('trello', 'key', False)
    TRELLO_TOK_READ = ui.config('trello', 'token_read', False)
    TRELLO_TOK_WRITE = ui.config('trello', 'token_write', False)

    if TRELLO_BOARD and TRELLO_KEY and TRELLO_TOK_READ and TRELLO_TOK_WRITE:
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

                    params = urllib.urlencode({'text' : 'Commited changeset %s (%s)\nby: %s\nbranch: *%s* \n\n%s' % (ctx, ctx.rev(), TRELLO_USER, ctx.branch(), bitbUrl)})
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
    else:
        ui.warn("[trello] settings not configured in hgrc\n")
    return