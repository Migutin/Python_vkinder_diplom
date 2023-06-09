from keyboard import *
from function import *

for event in vkinder.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            user_id = str(event.user_id)
            text_button = event.text.lower()
            sending(user_id, text_button.lower(),keyboard)
            if request == "vkinder":
                database()
                vkinder.user_get(user_id)
                vkinder.write_msg(event.user_id, f"Здравствуйте, {vkinder.name(user_id)}. "
                                                 f"Добро пожаловать в чат vkinder.\n"
                                                 f"\n"
                                                 f"Данные для поиска по умолчанию:\n"
                                                 f"- Город поиска: {vkinder.city(user_id)}\n"
                                                 f"- Пол для поиска: {vkinder.gender_exec(user_id,'gender_name')}\n"
                                                 f"- Минимальный возраст для поиска: {vkinder.age_min(user_id)}\n"
                                                 f"- Максимальный возраст для поиска: {vkinder.age_max(user_id)}\n"
                                                 f"\n"
                                                 f"Начать поиск - нажать кнопку Next\n"
                                                 f"Изменить данные поиска - нажать кнопку Edit\n"
                                                 f"Выход - нажать кнопку Exit")
                dict_search.clear()
                select_id_database(offset)
                vkinder.user_search(user_id)
            elif request == "next":
                vkinder.user_search_id(user_id)
                vkinder.id_user_priview()
                vkinder.write_msg(event.user_id,f'{vkinder.user_priview_info(user_id)}')
                vkinder.photos_id(vkinder.id_user_priview())
                vkinder.photo_priview(user_id, 'Фото 1',1)
                vkinder.photo_priview(user_id, 'Фото 2',2)
                vkinder.photo_priview(user_id, 'Фото 3',3)
                insert_users_tab_viewed(vkinder.id_user_priview(),offset)
                vkinder.write_msg(event.user_id, f"Поиск следующей анкеты - нажать кнопку Next\n"
                                                 f"Изменить данные поиска - нажать кнопку Edit\n"
                                                 f"Выход - нажать кнопку Exit")
            elif request == "edit":
                dict_search.clear()
                vkinder.city_edit(user_id)
                vkinder.gender_exec(user_id, 'gender_edit')
                vkinder.age_min_edit(user_id)
                vkinder.age_max_edit(user_id)
                vkinder.write_msg(event.user_id, f"Измененные данные для поиска:\n"
                                                 f"- Город поиска: {vkinder.city(user_id)}\n"
                                                 f"- Пол для поиска: {vkinder.gender_exec(user_id,'gender_name')}\n"
                                                 f"- Минимальный возраст для поиска: {vkinder.age_min(user_id)}\n"
                                                 f"- Максимальный возраст для поиска: {vkinder.age_max(user_id)}\n"
                                                 f"\n"
                                                 f"Начать поиск - нажать кнопку Next\n"
                                                 f"Изменить данные поиска - нажать кнопку Edit\n"
                                                 f"Выход - нажать кнопку Exit")
                database()
                vkinder.user_search(user_id)

            elif request == "exit":
                vkinder.write_msg(event.user_id, "До свиданья!")
            else:
                vkinder.write_msg(event.user_id, "Запрос не найден")