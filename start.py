from aiogram import types, Router
from aiogram.filters import Command
from config import bot
import keyboard as kb_start
from buttons import main_menu
from system import has_username, is_new, get_user_expense_data, get_user_income_data, rest_of_savings
from formatter import main_screen

kb = kb_start.Keyboard()
buttons = [
    {"text": "Создать операцию", "callback": "create_operation"},

]

router = Router()


@router.message(Command(commands=['start']))
async def register_new_wallet(message: types.Message):
    mes_del = message
    if has_username(mes_del):
        user = message.from_user.username
        await bot.delete_message(chat_id=message.from_user.id, message_id=mes_del.message_id)
        if is_new(message.from_user.username):
            await bot.send_message(chat_id=message.from_user.id, text="Создать первую операцию?",
                                   reply_markup=kb.go_to(buttons, 1).as_markup())
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=main_screen(user, rest_of_savings(user),
                                                    get_user_income_data(user), get_user_expense_data(user)),
                                   reply_markup=kb.go_to(main_menu, 2).as_markup())
