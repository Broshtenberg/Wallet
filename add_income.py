from aiogram.filters import Text
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot, wm
import keyboard as k

kb = k.Keyboard()
mc = MessageCollector()


router = Router()

class Savings(StatesGroup):
    title = State()
    source = State()
    count = State()



@router.message(Savings.title)
async def set_title(message: types.Message, state: FSMContext):
    mes = message
    await state.update_data(title=message.text)
    await bot.delete_message(message_id = mes.message_id, chat_id=message.from_user.id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=mc.tmp, text="Веди источник дохода")
    await state.set_state(Savings.source)
    
@router.message(Savings.source)
async def set_source(message: types.Message, state: FSMContext):
    mes = message
    await state.update_data(source=message.text)
    await bot.delete_message(message_id=mes.message_id, chat_id=message.from_user.id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=mc.tmp, text="Введи сумму")
    await state.set_state(Savings.count)
    
@router.message(Savings.count)
async def set_count(message: types.Message, state: FSMContext):
    wallet = wm.get_wallet(wallet_id=message.from_user.id)
    mes = message
    await state.update_data(count=message.text)
    await bot.delete_message(message_id=mes.message_id, chat_id=message.from_user.id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=mc.tmp)
    income = await state.get_data()
    new_income = inc.Income(title=income['title'], source=income['source'], count=income['count'])
    wallet.add_income(new_income)
    await bot.send_message(chat_id=message.from_user.id,text=f"Счет пополнен на сумму: {new_income.count}.\n Ha счету: {wallet.show_savings()}", reply_markup=kb.go_to([
        {"text":"В главное меню >>>", "callback": "main_menu"},
    ], 1).as_markup())


