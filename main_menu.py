# from aiogram.filters import Text
# from aiogram import types, Router
# from config import bot
# import keyboard as k
#
# kb = k.Keyboard()
# buttons = [
#     {"text": "Пополнить", "callback": "add_income"},
#     {"text": "Внести расход", "callback": "add_expense"},
# ]
# roouter = Router()
#
#
# @roouter.callback_query(Text(text='main_menu'))
# async def show_main_menu(callback: types.CallbackQuery):
#     """Show main menu in bot"""
#     await bot.edit_message_text(message_id=callback.message.message_id, chat_id=wallet.id, text=f"""
#
#
# Хочешь пополнить накопления?
#
#                                 """, reply_markup=kb.go_to(buttons, 2).as_markup())
