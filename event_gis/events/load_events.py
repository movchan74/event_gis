#!/usr/bin/python
# -*- coding: utf-8 -*-
from grab import Grab
import re
import json
from datetime import datetime
from datetime import timedelta

def clear_address(address):
	parser = re.compile(u'этаж$')
	if parser.search(address):
		return ','.join(address.split(',')[0:-1])
	else:
		return address

g = Grab()

month_num = {u'января' : 1, u'февраля' : 2, u'марта' : 3, u'апреля' : 4, u'мая' : 5, u'июня' : 6, u'июля' : 7, u'августа' : 8, u'сентября' : 9, u'октября' : 10, u'ноября' : 11, u'декабря' : 12,}

events = []
parser1 = re.compile(u'([0-9]+)( )([А-Яа-я]+)( с )([0-9:]+)( по )([0-9:]+)')
parser2 = re.compile(u'([0-9]+)( )([А-Яа-я]+)( в )([0-9:]+)')
parser3 = re.compile(u'([0-9]+)( )([А-Яа-я]+)( весь день)')
page = 1
while True:
	g.go('http://www.2do2go.ru/msk/events?page=%s' % page)
	if int(g.doc.select('//*[@class="paginator_item paginator_item__selected"]').text()) != page:
		break

	for item in g.doc.select('//*[@class="medium-events-list_item"]'):
		event = {}
		event['name'] = item.select('.//*[@class="medium-events-list_title"]').text()
		event['description'] = item.select('.//*[@class="medium-events-list_description"]').text()
		datetime_string = item.select('.//*[@class="medium-events-list_datetime"]').text()
		start_datetime = None
		end_datetime = None
		datetime_parse_result = parser1.findall(datetime_string)
		if datetime_parse_result != []:
			day = datetime_parse_result[0][0]
			month = month_num[datetime_parse_result[0][2]]
			start_time = datetime_parse_result[0][4]
			end_time = datetime_parse_result[0][6]
			year = datetime.today().year
			if datetime(year, int(month), int(day)) < datetime.today():
				year += 1
			start_datetime = datetime.strptime('%s %s %s %s' % (year, month, day, start_time), '%Y %m %d %H:%M')
			end_datetime = datetime.strptime('%s %s %s %s' % (year, month, day, end_time), '%Y %m %d %H:%M')
			if end_datetime < start_datetime:
				end_datetime += timedelta(days=1)
		else:
			datetime_parse_result = parser2.findall(datetime_string)
			if datetime_parse_result != []:
				day = datetime_parse_result[0][0]
				month = month_num[datetime_parse_result[0][2]]
				start_time = datetime_parse_result[0][4]
				year = datetime.today().year
				if datetime(year, int(month), int(day)) < datetime.today():
					year += 1
				start_datetime = datetime.strptime('%s %s %s %s' % (year, month, day, start_time), '%Y %m %d %H:%M')
				end_datetime = start_datetime + timedelta(hours=4)
			else:
				datetime_parse_result = parser3.findall(datetime_string)
				if datetime_parse_result != []:
					day = datetime_parse_result[0][0]
					month = month_num[datetime_parse_result[0][2]]
					year = datetime.today().year
					if datetime(year, int(month), int(day)) < datetime.today():
						year += 1
					start_datetime = datetime.strptime('%s %s %s 06:00' % (year, month, day), '%Y %m %d %H:%M')
					end_datetime = datetime.strptime('%s %s %s 00:00' % (year, month, day), '%Y %m %d %H:%M') + timedelta(days=1)
				else:
					print 'Error!!!'
		event['start_datetime'] = start_datetime
		event['end_datetime'] = end_datetime
		place = item.select('.//*[@class="medium-events-list_place"]')
		if place:
			event['place'] = place.text()
		else:
			event['place'] = ''
		address = item.select('.//*[@class="medium-events-list_address"]').text()
		full_address = u'Москва, ' + clear_address(address)
		print full_address
		g.go(u'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&language=ru' % full_address.replace(u' ', '%20'))
		result = json.loads(g.response.body)
		print result['results'][0]['geometry']['location']
		events.append(event)
		print event['name']
		print event['start_datetime']
		print event['end_datetime']
	page += 1


		# next_page = g.doc.select('//*[@class="paginator_next"]')
		# if next_page:
		# 	print "next"
		# 	next_page_link = next_page[0].select('.//a')[0].attr('href')
		# else:
		# 	break
		# break