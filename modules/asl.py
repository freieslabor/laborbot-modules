# coding=utf8
"""
asl.py - Willie Freies Labor Activity Streams Lite Module
Licensed under a Mozilla Public License 2.0.
"""
from willie.module import commands, interval
import urllib2, json, datetime, os, pickle

ASL_QUERY = '-wiki.*&-sensor.traffic-light&-sensor.mate-o-meter&-twitter.retweet'


def setup(self):
	"""Performs startup tasks."""
	fn = self.nick + '-' + self.config.host + '.asl.p'
	self.asl_filename = os.path.join(self.config.dotdir, fn)
	if not os.path.exists(self.asl_filename):
		try:
			f = open(self.asl_filename, 'wb')
		except OSError:
			pass
		else:
			# write current id as last id
			lastId = asl(self.config.asl.asl_query)[0]['id']
			pickle.dump(lastId, f)
			f.close()


def configure(config):
	"""
	|  [asl]    | example             | purpose         |
	| ----------| ------------------- | --------------- |
	| asl_query | last_id=%d%sensor.* | Sets ASL filter |
	"""
	if config.option('Configure ASL module', False):
		config.add_section('asl')
		config.interactive_add('asl', 'asl_query', 'ASL query')


def asl(argStr=''):
	"""Returns ASL results matching the filter arg string."""
	try:
		request = urllib2.Request('http://asl.hickerspace.org/asl.json?%s' \
			% argStr)
		response = json.load(urllib2.urlopen(request))
		return response['results']
	except urllib2.URLError as e:
		return []
	return messages


def getAslUpdates(bot):
	"""Checks for new ASL messages and announces them."""
	with open(bot.asl_filename) as f:
		lastId = pickle.load(f)
		for item in asl('%s&%s' % ("last_id=%d" % lastId, bot.config.asl.asl_query)):
			lastId = item['id'] if item['id'] > lastId else lastId

			# ignore updates older than 90 minutes
			date = datetime.datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')
			if date < datetime.datetime.now() - datetime.timedelta(minutes=90):
				continue

			author = 'by %s ' % item['person'] if item['person'] else ''
			message = '[%s] %s %s(%s)' % (item['service'].title(), item['content'], author, item['url'])

			# announce in all channels
			for chan in bot.channels:
				bot.msg(chan, message)

		pickle.dump(lastId, open(bot.asl_filename, 'wb'))


@interval(30)
def intervalAsl(bot):
	"""Queries ASL updates automatically."""
	getAslUpdates(bot)


@commands('events')
def queryEvents(bot, trigger):
	"""Returns last 5 ASL updates (https://asl.hickerspace.org)."""
	for item in reversed(asl(bot.config.asl.asl_query)[:5]):
		author = 'by %s ' % item['person'] if item['person'] else ''
		message = '%s: [%s] %s %s(%s)' % (item['datetime'], \
			item['service'].title(), item['content'], author, item['url'])
		bot.say(message)


class ApiException(Exception):
	"""Custom API exception."""
	pass

