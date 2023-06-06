# keyboards
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


class Keyboard:
    def go_to(self, buttons, row):
        keyboard = InlineKeyboardBuilder()
        for button in buttons:
            keyboard.add(types.InlineKeyboardButton(text=button['text'], callback_data=button['callback']))

        keyboard.adjust(row)

        return keyboard

    def set_text_kb(self, buttons):
        """Создает текстовый кнопки из списка списков кнопок"""
        keyboard = [[types.KeyboardButton(text=button)] for button in buttons]
        kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        return kb
