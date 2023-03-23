from random import randrange
from token_date import user_token, group_token, v, offset, line
import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from database import *

parametr_search = {'city':'',
                   'sex':'',
                   'age_min':'',
                   'age_max':''}


class vk_group:
    def __init__(self):
        print('Vkinder успешно запущен')
        self.vk = vk_api.VkApi(token=group_token)  # Авторизация сообщества
        self.longpoll = VkLongPoll(self.vk)  # Метод работы с сообщениями

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def name(self, user_id):
        """Получение имя пользователя"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': v}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            dict_info = response['response']
            for keys_item in dict_info:
                first_name = keys_item.get('first_name')
                return first_name
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')


    def city(self, user_id):
        """Получение названия города пользователя"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': v}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            dict_info = response['response']
            if parametr_search['city'] != '':
                city = parametr_search['city']
                return city
            else:
                for keys_item in dict_info:
                    if 'city' in keys_item:
                        city_base = keys_item.get('city')
                        city=city_base['title']
                        id=str(city_base.get('id'))
                        return city
                    elif 'city' not in keys_item:
                        self.write_msg(user_id, 'Введите название вашего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city = event.text
                            if city != '' or city != None:
                                return str(city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')

    def city_edit(self,user_id):
        """Изменение названия города пользователя"""
        self.write_msg(user_id, 'Введите название города для поиска: ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                city = event.text
                parametr_search['city']=city
                if city != '' or city != None:
                    return str(city)
                else:
                    break

    def city_id(self, user_id):
        """Получение id города пользователя"""
        url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                  'country_id': 1,
                  'q': f'{self.city(user_id)}',
                  'need_all': 0,
                  'count': 1000,
                  'v': v}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            dict_info = response['response']
            list_city = dict_info['items']
            for i in list_city:
                found_city_id = i.get('id')
                return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')

    def gender(self, user_id):
        """Получение пола человека для поиска"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'sex',
                  'user_ids': user_id,
                  'v': v}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            dict_info = response['response']
            if parametr_search['sex'] != '':
                sex = parametr_search['sex']
                return sex
            else:
                for keys_item in dict_info:
                    sex_gender = keys_item.get('sex')
                    if sex_gender == 1:
                        sex = 2
                    else:
                        sex = 1
                    return sex
        except KeyError:
                self.write_msg(user_id, 'Введен некорректный user_token')


    def gender_edit(self,user_id):
        """Изменение пола человека для поиска"""
        self.write_msg(user_id, 'Введите пол человека для поиска: ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                sex_name = event.text
                if sex_name == 'мужской':
                    sex = 2
                else:
                    sex = 1
                parametr_search['sex']=sex
                if sex != '' or sex != None:
                    return sex
                else:
                    break

    def gender_exec (self,user_id,gender):
        """Вывод названия пола в сообщество"""
        if gender == 'gender_name':
            gender = self.gender(user_id)
            if gender == 1:
                gender_name = 'женский'
            else:
                gender_name = 'мужской'
            return gender_name
        elif gender == 'gender_edit':
            gender = self.gender_edit(user_id)
            if gender == 1:
                gender_edit = 'женский'
            else:
                gender_edit= 'мужской'
            return gender_edit

    def age_min(self, user_id):
        """Получение минимального возраста поиска"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'bdate',
                  'user_ids': user_id,
                  'v': v}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            dict_info = response['response']
            if parametr_search['age_min'] != '':
                age_min = parametr_search['age_min']
                return age_min
            else:
                for keys_item in dict_info:
                    if 'bdate' in keys_item:
                        age = keys_item.get('bdate')
                        age_list = age.split('.')
                        if len(age_list) == 3:
                            year_bdate = int(age_list[2])
                            year_now = int(datetime.date.today().year)
                            age_user = year_now - year_bdate
                            age_min=age_user-5
                            return age_min
                        else:
                            self.write_msg(user_id, 'Введите ваш возраст: ')
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    age_user = event.text
                                    age_min = age_user - 5
                                    return age_min
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')

    def age_min_edit(self,user_id):
        """Изменение минимального возраста"""
        self.write_msg(user_id, 'Введите минимальный возраст для поиска: ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age_min = event.text
                parametr_search['age_min'] = age_min
                if age_min != '' or age_min != None:
                    return str(age_min)
                else:
                    break

    def age_max(self, user_id):
        """Получение максимального возраста поиска"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'bdate',
                  'user_ids': user_id,
                  'v': v}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            dict_info = response['response']
            if parametr_search['age_max'] != '':
                age_max = parametr_search['age_max']
                return age_max
            else:
                for keys_item in dict_info:
                    if 'bdate' in keys_item:
                        age = keys_item.get('bdate')
                        age_list = age.split('.')
                        if len(age_list) == 3:
                            year_bdate = int(age_list[2])
                            year_now = int(datetime.date.today().year)
                            age_user = year_now - year_bdate
                            age_min=age_user + 5
                            return age_min
                        else:
                            self.write_msg(user_id, 'Введите ваш возраст: ')
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    age_user = event.text
                                    age_min = age_user + 5
                                    return age_min
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')

    def age_max_edit(self,user_id):
        """Изменение минимального возраста"""
        self.write_msg(user_id, 'Введите максимальный возраст для поиска: ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age_max = event.text
                parametr_search['age_max'] = age_max
                if age_max!= '' or age_max != None:
                    return str(age_max)
                else:
                    break

    def user_search(self, user_id):
        """Поиск человека по полученным данным"""
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': v,
                  'city': self.city_id(user_id),
                  'sex': self.gender(user_id),
                  'age_from': self.age_min(user_id),
                  'age_to': self.age_max(user_id),
                  'fields': 'is_closed, id, first_name, last_name, bdate',
                  'status': '1' or '6',
                  'count': 500}
        req = requests.get(url, params=params)
        response = req.json()
        try:
            dict_info = response['response']
            list = dict_info['items']
            for user_dict in list:
                if user_dict.get('is_closed') == False:
                    first_name = user_dict.get('first_name')
                    last_name = user_dict.get('last_name')
                    vk_id = str(user_dict.get('id'))
                    vk_link = 'vk.com/id' + str(user_dict.get('id'))
                    bdate = user_dict.get('bdate')
                    insert_users_tab(first_name, last_name, vk_id, vk_link,bdate)
                else:
                    continue
            return f'Поиск завершён'
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')

    def photos_id(self, user_id):
        """Получение фотографий пользователя"""
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': v}
        req = requests.get(url, params=params)
        photo_dict = {}
        response = req.json()
        try:
            dict = response['response']
            list = dict['items']
            for num in list:
                photo_id = str(num.get('id'))
                num_likes = num.get('likes')
                if num_likes.get('count'):
                    likes = num_likes.get('count')
                    photo_dict[likes] = photo_id
            photo_dict_sorted = sorted(photo_dict.items(), reverse=True)
            return photo_dict_sorted
        except KeyError:
            self.write_msg(user_id, 'Введен некорректный user_token')

    def photo_user_1(self, user_id):
        """Получение 1 фотографии"""
        photo_list = self.photos_id(user_id)
        count=0
        for photo in photo_list:
            count += 1
            if count == 1:
                return photo[1]

    def photo_1_priview(self, user_id, message, offset):
        """Вывод 1 фотографии"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.id_user_priview(offset)}_{self.photo_user_1(self.id_user_priview(offset))}',
                                         'random_id': 0})

    def photo_user_2 (self, user_id):
        """Плучение 2 фотографии"""
        photo_list = self.photos_id(user_id)
        count=0
        for photo in photo_list:
            count += 1
            if count == 2:
                return photo[1]

    def photo_2_priview(self, user_id, message, offset):
        """Вывод 2 фотографии"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.id_user_priview(offset)}_{self.photo_user_2(self.id_user_priview(offset))}',
                                         'random_id': 0})

    def photo_user_3 (self, user_id):
        """Получение 3 фотографии"""
        photo_list = self.photos_id(user_id)
        count=0
        for photo in photo_list:
            count += 1
            if count == 3:
                return photo[1]

    def photo_3_priview(self, user_id, message, offset):
        """Вывод 3 фотографии"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.id_user_priview(offset)}_{self.photo_user_3(self.id_user_priview(offset))}',
                                         'random_id': 0})

    def id_user_priview(self, offset):
        """Получение id найденного человека"""
        base = select(offset)
        dict_base = []
        for i in base:
            dict_base.append(i)
        return str(dict_base[2])

    def user_priview_info(self,user_id, offset):
        """Вывод информации по найденноuго человека"""
        base = select(offset)
        dict_base = []
        today = datetime.date.today()
        for i in base:
            dict_base.append(i)
        dict_date = dict_base[4].split('.')
        day = int(dict_date[0])
        month = int(dict_date[1])
        year = int(dict_date[2])
        return f'{dict_base[0]} {dict_base[1]}\n' \
               f'г.{self.city(user_id)}\n' \
               f'Возраст: {today.year - year - ((today.month, today.day) < (month, day))} лет\n' \
               f'Профиль vkontakte - {dict_base[3]}'

vkinder = vk_group()

