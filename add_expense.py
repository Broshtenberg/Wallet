# add expense handler
from aiogram.filters import Text
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot, wm

import Money.expense as exp
import keyboard as k


mc = MessageCollector()
kb = k.Keyboard()
buttons = [
        {"text": "В главное меню >>>", "callback": "main_menu"}
        ]
router = Router()

class Expense(StatesGroup):
    title = State()
    category = State()
    count = State()



@router.callback_query(Text(text="add_expense"))
async def start_adding_income(callback: types.CallbackQuery, state: FSMContext):
    message = await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text="Введи название расхода")
    mc.set_temp_msg(message_id=message.message_id)
    await state.set_state(Expense.title)

@router.message(Expense.title)
async def set_title(message: types.Message, state: FSMContext):
    mes_id = message.message_id
    await state.update_data(title=message.text)
    await bot.delete_message(chat_id=message.from_user.id, message_id=mes_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=mc.tmp, text="Введи категорию расхода")
    await state.set_state(Expense.category)

@router.message(Expense.category)
async def set_category(message: types.Message, state: FSMContext):
    mes_id=message.message_id
    await state.update_data(category=message.text)
    await bot.delete_message(chat_id=message.from_user.id, message_id=mes_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=mc.tmp, text="Введи сумму расходов")
    await state.set_state(Expense.count)


@router.message(Expense.count)
async def set_count(message: types.Message, state: FSMContext):
    mes_id=message.message_id
    await state.update_data(count=int(message.text))
    await bot.delete_message(chat_id=message.from_user.id, message_id=mes_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=mc.tmp)
    exp_data = await state.get_data()
    new_expense = exp.Expense(title=exp_data['title'], category=exp_data['category'], count=exp_data['count'])
    wallet=wm.get_wallet(wallet_id=message.from_user.id)
    wallet.add_expense(new_expense)
    await bot.send_message(chat_id=message.from_user.id, text=f"Расход добавлен на сумму: -{new_expense.count}р.\nТекущий баланс: {wallet.show_savings()}\nвернуться в главное меню?",
                           reply_markup=kb.go_to(buttons,1).as_markup())

