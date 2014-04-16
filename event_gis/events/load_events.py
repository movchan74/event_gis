#!/usr/bin/python
# -*- coding: utf-8 -*-
from grab import Grab
import re
import json
from datetime import datetime
from datetime import timedelta
from models import Event, EventType
from django.core.exceptions import ObjectDoesNotExist
import string
import pytz

types = {
	u'Балет и опера' : 	u'Балет и опера',
	u'Мюзиклы' : u'Мюзиклы',
	u'Балет' : 	u'Балет и опера',
	u'Творческий вечер' : 	u'Творческие вечера',
	u'Спектакли' : 	u'Спектакли',
	u'Концерты' : 	u'Концерты',
	u'Рок' : u'Концерты',
	u'Hip-Hop' : u'Концерты',
	u'Альтернатива' : u'Концерты',
	u'Металл' : u'Концерты',
	u'Популярная музыка' : u'Концерты',
	u'Классика' : u'Концерты',
	u'Акустика' : u'Концерты',
	u'Авторская песня' : u'Концерты',
	u'Фолк' : u'Концерты',
	u'Блюз и джаз' : u'Концерты',
	u'Рок-н-ролл' : u'Концерты',
	u'Мхатовский вечер' : 	u'Творческие вечера',
	u'Международный фестиваль' : u'Фестивали',
	u'Лекции' : 	u'Лекции',
	u'Вечеринки' : 	u'Вечеринки',
	u'Быстрые свидания' : u'Вечеринки',
	u'Фестивали' : 	u'Фестивали',
	u'Спорт' : 	u'Спорт',
	u'Другие виды спорта' : 	u'Спорт',
	u'Водный спорт' : 	u'Спорт',
	u'Турниры' : 	u'Спорт',
	u'Летний спорт' : u'Спорт',
	u'Экстремальный спорт' : u'Спорт',
	u'Зимний спорт' : u'Спорт',
	u'Бег' :  u'Спорт',
	u'Экстремальные развлечения' : u'Спорт',
	u'Шоу' : 	u'Шоу',
	u'Юмористические мероприятия' : u'Шоу',
	u'Спортивно-развлекательное шоу' : 	u'Шоу',
	u'Курсы' : 	u'Обучение',
	u'Экскурсии' : 	u'Экскурсии',
	u'Праздники' : 	u'Праздники',
	u'Мастер-классы' : 	u'Обучение',
	u'Обучение' : u'Обучение',
	u'Тренинги' : u'Обучение',
	u'Презентации' : u'Обучение',
	u'Выставки' : 	u'Выставки',
	u'Ярмарки' : 	u'Ярмарки',
	u'Мода' : 	u'Мода',
	u'Кино' : 	u'Кино',
	u'Комедии' : u'Кино',
	u'Ночи кино' : u'Кино',
	u'Исторические фильмы' : u'Кино',
	u'Семейные фильмы' : u'Кино',
	u'Музыкальные фильмы' : u'Кино',
	u'Фантастика' : u'Кино',
	u'Триллеры' : u'Кино',
	u'Драмы' : u'Кино',
	u'Боевики' : u'Кино',
	u'Фэнтези' : u'Кино',
	u'Приключения' : u'Кино',
	u'Мультфильмы' : u'Кино',
	u'Конференции' : 	u'Конференции',
	u'Прогулки' : u'Прогулки',
	u'Общественные акции' : u'Общественные акции',
	u'Съемки' : u'Съемки',
	u'Встречи' : u'Встречи',
	u'Настольные игры' : u'Игры',
	u'Игры для компаний' : u'Игры',
	u'Ролевые игры' : u'Игры',
	u'Квесты' : u'Игры',
	u'Игры' : u'Игры',
	u'Ночные игры' : u'Игры',
	u'Творческие вечера' : u'Творческие вечера',
	u'Искусство' : u'Искусство',
	u'Распродажи' : u'Распродажи',
	u'Разное' : u'Разное',
}

def string_to_list(s):
	return map(string.strip, s.split(','))

def clear_address(address):
	parser = re.compile(u'этаж$')
	if parser.search(address):
		return ','.join(address.split(',')[0:-1])
	else:
		return address

def detect_event_type(categories_text):
	categories = string_to_list(categories_text)
	for t in types:
		for cat in categories:
			if t == cat:
				return types[t]
	return None

def load_events():
	tz = pytz.timezone('Europe/Moscow')
	g = Grab()
	g_details = Grab()

	month_num = {u'января' : 1, u'февраля' : 2, u'марта' : 3, u'апреля' : 4, u'мая' : 5, u'июня' : 6, u'июля' : 7, 
				u'августа' : 8, u'сентября' : 9, u'октября' : 10, u'ноября' : 11, u'декабря' : 12,}
	for category in list(set(types.values())):
		try:
			EventType.objects.get(name=category)
		except ObjectDoesNotExist:
			EventType.objects.create(name=category, description=category)
	parser1 = re.compile(u'([0-9]+)( )([А-Яа-я]+)( с )([0-9:]+)( по )([0-9:]+)')
	parser2 = re.compile(u'([0-9]+)( )([А-Яа-я]+)( в )([0-9:]+)')
	parser3 = re.compile(u'([0-9]+)( )([А-Яа-я]+)( весь день)')
	page = 1
	while True:
		g.go('http://www.2do2go.ru/msk/events?page=%s' % page)
		if int(g.doc.select('//*[@class="paginator_item paginator_item__selected"]').text()) != page:
			break

		for item in g.doc.select('//*[@class="medium-events-list_item"]'):
			name = item.select('.//*[@class="medium-events-list_title"]').text()
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
			start_datetime = tz.localize(start_datetime)
			end_datetime = tz.localize(end_datetime)
			try:
				Event.objects.get(name=name, start_time=start_datetime, end_time=end_datetime)
			except ObjectDoesNotExist:
				description = item.select('.//*[@class="medium-events-list_description"]').text()
				place = item.select('.//*[@class="medium-events-list_place"]')
				if place:
					place = place.text()
				else:
					place = None
				address = item.select('.//*[@class="medium-events-list_address"]').text()
				full_address = u'Москва, ' + clear_address(address)
				g.go(u'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&language=ru' % full_address.replace(u' ', '%20'))
				result = json.loads(g.response.body)
				location = result['results'][0]['geometry']['location']
				print name

				details = item.select('.//a').attr('href')
				g_details.go(details)
				categories_text = g_details.doc.select('.//*[@class="event-info_labeled js-categories-list"]')[0].text()
				category = detect_event_type(categories_text)
				if not category:
					category = u'Разное'
				type_instance = EventType.objects.get(name=category)
				Event.objects.create(name=name, start_time=start_datetime, end_time=end_datetime, description=description,
					address=address, location='POINT(%s %s)' % (location['lng'], location['lat']), event_type=type_instance, place=place)
		page += 1