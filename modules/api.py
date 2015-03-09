# coding=utf8
"""
api.py - Willie Freies Labor API Module
Licensed under a Mozilla Public License 2.0.
"""
from willie.module import commands
import urllib, urllib2, json


def configure(config):
	"""
	|  [api]       | example  | purpose               |
	| ------------ | -------- | --------------------- |
	| api_user     | testuser | Sets the API user     |
	| api_password | testpw   | Sets the API password |
	"""
	if config.option('Configure API module', False):
		config.add_section('api')
		config.interactive_add('api', 'api_user', 'API user')
		config.interactive_add('api', 'api_password', 'API password')


def api(bot, path, params=None):
	"""Performs an API call."""
	apiUrl = 'https://freieslabor.org/api/%s' % path
	passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
	passman.add_password(None, apiUrl, \
		bot.config.api.api_user, bot.config.api.api_password)
	opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman))
	urllib2.install_opener(opener)
	# POST or GET
	if params:
		data = urllib.urlencode(params)
		req = urllib2.Request(apiUrl, data)
	else:
		req = urllib2.Request(apiUrl)

	response = urllib2.urlopen(req)
	return json.loads(response.read())


def apiError(err, msg):
	"""Generates error messages for API/HTTP errors."""
	try:
		response = json.loads(err.read())
		return '%s (%s)' % (msg, response['status'])
	except ValueError:
		return msg


@commands('open', 'auf')
def openLab(bot, trigger):
	"""Sets the lab status to "open"."""
	try:
		# check whether status has changed
		oldStatus = api(bot, 'room')
		if oldStatus['open']:
			bot.say('Door status already "open".')
		elif not oldStatus['open']:
			# change status
			response = api(bot, 'room', { 'open': True })
			if response['success']:
				bot.say('Door status changed to "open".')
			else:
				# raise error with API error message
				raise ApiException(response['status'])

	except (urllib2.HTTPError, ApiException), e:
		bot.say(apiError(e, "Couldn't set room status"))


@commands('close', 'zu')
def closeLab(bot, trigger):
	"""Sets the lab status to "closed"."""
	try:
		# check whether status has changed
		oldStatus = api(bot, 'room')
		if not oldStatus['open']:
			bot.say('Door status already "closed".')
		elif oldStatus['open']:
			# change status
			response = api(bot, 'room', { 'open': False })
			if response['success']:
				bot.say('Door status changed to "closed".')
			else:
				# raise error with API error message
				raise ApiException(response['status'])

	except (urllib2.HTTPError, ApiException), e:
		bot.say(apiError(e, "Couldn't set room status"))


class ApiException(Exception):
	"""Custom API exception."""
	pass

