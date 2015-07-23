# coding=utf8
"""
deop.py - Willie Auto DeOp Module
Licensed under a Mozilla Public License 2.0.
"""

from willie.module import event, rule


@event('MODE')
@rule('.*')
def deop(bot, trigger):
    if bot.nick in trigger.args and '+o' in trigger.raw:
        bot.msg('ChanServ', 'deop %s %s' % (trigger.args[0], bot.nick))
