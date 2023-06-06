from aiogram.filters import Text
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot
from formatter import main_screen
from system import rest_of_savings, get_user_income_data, get_user_expense_data
import keyboard as k
from system import has_operations, get_expense_categories, get_expense_items, add_expense, add_savings, \
    get_ways_of_income, format_operation_message
from buttons import main_menu
from message_collector import MessageCollector

kb = k.Keyboard()
mc = MessageCollector()

router = Router()

buttons = [
    {"text": "Добавить расход", "callback": "create_expense"},
    {"text": "Добавить доход", "callback": "create_income"}
]

accept_buttons = [
    {"text": "Подвтердить", "callback": "dump_operation"},
    {"text": "Изменить", "callback": "change_operation"}
]


class Operation(StatesGroup):
    type = State()
    sum_of_money = State()
    income_way = State()
    expense_category = State()
    expense_item = State()


@router.callback_query(Text(text="create_operation"))
async def create_operation(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text="Выбери тип операции", reply_markup=kb.go_to(buttons, 2).as_markup())
    mc.set_user(callback.from_user.username)
    mc.set_chat_id(callback.from_user.id)
    mc.set_temp_msg(callback.message.message_id)
    await state.set_state(Operation.type)


@router.callback_query(Text(text="create_expense"), Operation.type)
async def create_expense(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type="expense")
    if has_operations(mc.user, "expense"):
        text = "Выбери существующую категорию расходов или же напиши новую"
        expense_categories = get_expense_categories(mc.user)
        info = await bot.send_message(chat_id=mc.chat_id, text=text,
                                      reply_markup=kb.set_text_kb(buttons=expense_categories))
    else:
        info = await bot.send_message(chat_id=mc.chat_id, text="Напиши категорию расходов")
    mc.add_more(info)
    await state.set_state(Operation.expense_category)


@router.callback_query(Text(text="create_income"), Operation.type)
async def create_income(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type="income")
    if has_operations(mc.user, "income"):
        text = "Выбери источник дохода из списка или укажи новый"
        ways_of_income = get_ways_of_income(mc.user)
        info = await bot.send_message(chat_id=mc.chat_id, text=text,
                                      reply_markup=kb.set_text_kb(buttons=ways_of_income))
    else:
        text = "Укажи новый источник дохода"
        info = await bot.send_message(chat_id=mc.chat_id, text=text)
    mc.add_more(info)
    await state.set_state(Operation.income_way)


@router.message(Operation.income_way)
async def set_way_of_income(message: types.Message, state: FSMContext):
    mc.add_more(message)
    await state.update_data(way=message.text)
    text = "Напиши сумму дохода"
    info = await bot.send_message(chat_id=mc.chat_id, text=text)
    mc.add_more(info)
    await state.set_state(Operation.sum_of_money)


@router.message(Operation.expense_category)
async def set_expense_category(message: types.Message, state: FSMContext):
    mc.add_more(message)
    await state.update_data(category=message.text.lower())
    if has_operations(mc.user, "expense"):
        text = "ВЫберите название из списка или введите новое"
        expense_items = get_expense_items(mc.user, message.text.lower())
        info = await bot.send_message(chat_id=mc.chat_id, text=text,
                                      reply_markup=kb.set_text_kb(buttons=expense_items))

    else:
        text = "Напиши название траты:"
        info = await bot.send_message(chat_id=mc.chat_id, text=text)
    mc.add_more(info)
    await state.set_state(Operation.expense_item)


@router.message(Operation.expense_item)
async def set_expense_item(message: types.Message, state: FSMContext):
    mc.add_more(message)
    await state.update_data(expense_item=message.text.lower())
    text = "Напиши сумму траты:"
    info = await bot.send_message(chat_id=mc.chat_id, text=text)
    mc.add_more(info)
    await state.set_state(Operation.sum_of_money)


@router.message(Operation.sum_of_money)
async def sum_of_money(message: types.Message, state: FSMContext):
    mc.add_more(message)
    await state.update_data(sum_of_money=int(message.text))
    opeartion_data = await state.get_data()
    formatted_message = format_operation_message(opeartion_data)
    info = await bot.send_message(chat_id=mc.chat_id, text=formatted_message,
                                  reply_markup=kb.go_to(accept_buttons, 2).as_markup())
    mc.add_more(info)


@router.callback_query(Text(text="dump_operation"))
async def dump_user_operation(callback: types.CallbackQuery, state: FSMContext):
    await mc.delete_msg()
    operation = await state.get_data()
    if operation['type'] == "expense":
        add_expense(mc.user, operation["sum_of_money"], operation['category'], operation['expense_item'])
    elif operation['type'] == 'income':
        add_savings(mc.user, operation['sum_of_money'], operation['way'])
    await callback.answer(text="Операция успешно добавлена!")
    operation.clear()
    await state.clear()
    await bot.edit_message_text(chat_id=mc.chat_id, message_id=mc.tmp,
                                text=main_screen(mc.user, rest_of_savings(mc.user), get_user_income_data(mc.user),
                                                 get_user_expense_data(mc.user)),
                                reply_markup=kb.go_to(main_menu, 2).as_markup())
    mc.clear()
