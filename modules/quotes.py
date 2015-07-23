# coding=utf8
"""
quotes.py - Willie Freies Labor Quotes Module
Licensed under a Mozilla Public License 2.0.
"""
from willie.module import commands, interval
import os, random


def setup(self):
	"""Loads quotes from files."""
	self.quotes = { }
	quoteFiles = [ 'fefe', 'bofh' ]
	for quoteFile in quoteFiles:
		self.quotes[quoteFile] = []
		for quote in file(os.path.join(self.config.dotdir, quoteFile)):
			self.quotes[quoteFile].append(quote[:-1])


@commands('fefe')
def fefe(bot, trigger):
	"""Returns a Fefe quote."""
	bot.say(random.choice(bot.quotes['fefe']))


@commands('wtf')
def wtf(bot, trigger):
	"""Returns a Fefe quote."""
	quote = random.choice(bot.quotes['fefe'])
	bot.say('Was täte Fefe? Fefe: %s' % quote)


@commands('bofh', 'excuse')
def bofh(bot, trigger):
	"""Returns a BOFH excuse."""
	bot.say(random.choice(bot.quotes['bofh']))

