import os
import datetime
import logging

ORDER = 999
HOTELS_PATH = 'hotels/'
HOTELS = []
FEATURED_HOTEL_NAMES = ['Inya Lake Hotel', 'Savoy Hotel', 'Sedona Hotel', 'Strand Hotel']
FEATURED_HOTELS = []
CLASSIFIED_HOTEL_NAMES = ['Summit Park View Hotel', 'Traders Hotel', 'Park Royal Hotel', 'Kandawgyi Palace Hotel']
CLASSIFIED_HOTELS = []

FEATURED_ITEM_TITLE = 'Myanmar Life Hotel'

from django.template import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode

def getNode(template, context=Context(), name='subject'):
	"""
	Get django block contents from a template.
	http://stackoverflow.com/questions/2687173/
	django-how-can-i-get-a-block-from-a-template
	"""
	for node in template:
		if isinstance(node, BlockNode) and node.name == name:
			return node.render(context)
		elif isinstance(node, ExtendsNode):
			return getNode(node.nodelist, context, name)
	raise Exception("Node '%s' could not be found in template." % name)


def preBuild(site):

	global HOTELS
	global FEATURED_HOTELS
	global FEATURED_ITEM
	global CLASSIFIED_HOTELS

	# Build all the posts
	for page in site.pages():
		if page.path.startswith(HOTELS_PATH):

			# Skip non html posts for obious reasons
			if not page.path.endswith('.html'):
				continue

			# Find a specific defined variable in the page context,
			# and throw a warning if we're missing it.
			def find(name):
				c = page.context()
				if not name in c:
					logging.info("Missing info '%s' for hotel %s" % (name, page.path))
					return ''
				return c.get(name, '')

			# Build a context for each hotel
			hotelContext = {}
			hotelContext['title'] = find('title')
			hotelContext['title_flatten'] = find('title').replace(" ", "");
			hotelContext['path'] = page.path
			hotelContext['special_tag'] = find('special_tag')
			hotelContext['address'] = find('address')
			hotelContext['city'] = find('city')
			hotelContext['description'] = find('description')
			hotelContext['description1'] = find('description1')
			hotelContext['description2'] = find('description2')
			hotelContext['phone'] = find('phone')
			hotelContext['email'] = find('email')
			hotelContext['URL'] = find('URL')

			HOTELS.append(hotelContext)

			if hotelContext['title'] in FEATURED_HOTEL_NAMES:
				FEATURED_HOTELS.append(hotelContext)

			if hotelContext['title'] == FEATURED_ITEM_TITLE:
				FEATURED_ITEM = hotelContext

			if hotelContext['title'] in CLASSIFIED_HOTEL_NAMES:
				CLASSIFIED_HOTELS.append(hotelContext)



def preBuildPage(site, page, context, data):
	"""
	Add the list of hotels to every page context so we can
	access them from wherever on the site.
	"""
	context['hotels'] = HOTELS
	context['featured_hotels'] = FEATURED_HOTELS
	context['featured_item'] = FEATURED_ITEM
	context['classified_hotels'] = CLASSIFIED_HOTELS

	for hotel in HOTELS:
		if hotel['path'] == page.path:
			context.update(hotel)
			context['this_hotel'] = hotel

	return context, data