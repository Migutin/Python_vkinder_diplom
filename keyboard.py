from function import vkinder
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def sending(user_id, text,keyboard=None):
    per={'user_id': user_id,
         'message': text,
          'random_id': 0,
         'button': keyboard}
    if keyboard != None:
        per['keyboard']=keyboard.get_keyboard()
    else: per = per
    vkinder.vk.method('messages.send', per)
keyboard = VkKeyboard()
keyboard.add_button('Vkinder', VkKeyboardColor.PRIMARY,"{\"button\": \"" + "1" + "\"}")
keyboard.add_button('Next', VkKeyboardColor.SECONDARY,"{\"button\": \"" + "1" + "\"}")
keyboard.add_button('Edit', VkKeyboardColor.SECONDARY,"{\"button\": \"" + "1" + "\"}")
keyboard.add_button('Exit', VkKeyboardColor.PRIMARY,"{\"button\": \"" + "1" + "\"}")
