from pathlib import Path
from aiogram import types
import json
import time


def load_data(filename):
    """Load json data from server"""

    file = Path.cwd() / f"{filename}.json"
    with file.open(mode="r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    return data


def save_data(data, filename):
    """Load json data from server"""

    file = Path.cwd() / f"{filename}.json"
    with file.open(mode="w", encoding="utf-8") as data_file:
        json.dump(data, data_file)
    return


def set_today():
    return {
        "today": time.localtime().tm_mday,
        "weekday": time.localtime().tm_wday,
        "month": time.localtime().tm_mon,
        "year": time.localtime().tm_year
    }


def add_expense(user, sum_of_money, category, product_name):
    """Создает расход пользователя"""
    all_users: dict = load_data("users")
    if not all_users.get(user):
        all_users[user] = [
            ["expense", -sum_of_money, category, product_name, set_today()]
        ]
    else:
        all_users[user].append(["expense", -sum_of_money, category, product_name, set_today()])
    save_data(all_users, "users")


def add_savings(user, sum_of_money, way_of_income):
    """Создает расход пользователя"""
    all_users: dict = load_data("users")
    if not all_users.get(user):
        all_users[user] = [
            ["income", sum_of_money, way_of_income, set_today()]
        ]
    else:
        all_users[user].append(["income", sum_of_money, way_of_income, set_today()])

    save_data(all_users, "users")


def get_user_operations(user, operation_type):
    """Получить все операции пользователя"""
    operations = []
    if not is_new(user):
        operations = [operation for operation in load_data("users").get(user) if operation[0] == operation_type]
    return operations


def count_operations_by_period(user, operation_type, period="all"):
    """ПОлучить определенный вид операций пользователя за определенный период"""
    sum_of_money = 0
    operations = get_user_operations(user, operation_type)
    if len(operations) > 0:
        if period == "all":
            sum_of_money = sum([money_count[1] for money_count in operations])
        elif period == "per_today":
            today = set_today()['today']
            sum_of_money = sum([money_count[1] for money_count in operations if money_count[-1]['today'] == today])

        elif period == "per_yesterday":
            yesterday = set_today()['today'] - 1
            sum_of_money = sum([money_count[1] for money_count in operations if money_count[-1]['today'] == yesterday])

        elif period == "per_week":
            date = set_today()
            sum_of_money = sum([money_count[1] for money_count in operations if
                                money_count[-1]['today'] in range(date["today"] - date["weekday"], date["today"] + 1)])
        elif period == "per_month":
            sum_of_money = sum(
                [money_count[1] for money_count in operations if money_count[-1]['month'] == set_today()["month"]])

        elif period == "per_year":
            sum_of_money = sum(
                [money_count[1] for money_count in operations if money_count[-1]['year'] == set_today()["year"]])

    return sum_of_money


def rest_of_savings(user):
    """Остаток на балансе пользователя"""
    return count_operations_by_period(user, "income") + count_operations_by_period(user, "expense")


def get_expense_categories(user):
    """Получить список категорий трат"""
    categories = []
    for category in [expense[2].strip() for expense in get_user_operations(user, "expense")]:
        if category not in categories:
            categories.append(category)
    return categories


def get_expense_items(user, category='all'):
    """Получить список названий всех упомянутых трат или внутри категории"""
    expense_items = []
    if category == "all":
        for expense_item in [expense[3].strip() for expense in get_user_operations(user, "expense")]:
            if expense_item not in expense_items:
                expense_items.append(expense_item)
    else:
        for expense_item in [expense[3].strip() for expense in get_user_operations(user, "expense") if
                             expense[2] == category]:
            if expense_item not in expense_items:
                expense_items.append(expense_item)

    return expense_items


def get_ways_of_income(user):
    """ПОлучить список истоников дохода"""
    ways = []
    for income_way in [income[2] for income in get_user_operations(user, "income")]:
        if income_way not in ways:
            ways.append(income_way)
    return ways


def has_operations(user, operation_type):
    """Есть ли у данного пользователя какие либо операции"""
    result = None
    all_users = load_data("users")
    if all_users.get(user):
        result = len(get_user_operations(user, operation_type))

    return bool(result)


def _create_expense_text(operation_data):
    """СОздает отформатированую запись нового расхода"""
    text = f"""
Категория: {operation_data["category"].title()}
Название: {operation_data["expense_item"].title()}
Сумма: -{operation_data["sum_of_money"]}руб.
"""
    return text


def _create_income_text(operation_data):
    """СОздает отформатированую запись нового расхода"""
    text = f"""
Источнк дохода: {operation_data["way"].title()}
Сумма: {operation_data["sum_of_money"]}руб.
"""
    return text


def format_operation_message(operation_data):
    text = ''
    if operation_data['type'] == "expense":
        text = _create_expense_text(operation_data)
    elif operation_data["type"] == "income":
        text = _create_income_text(operation_data)
    return text


def has_username(message: types.Message):
    if message.__getattribute__("from_user"):
        if message.from_user.__getattribute__("username"):
            return True


def is_new(user):
    all_users = load_data("users")
    if not all_users.get(user):
        return True


def get_user_income_data(user):
    user_income_data = {
        "per_today": count_operations_by_period(user, "income", "per_today"),
        "per_yesterday": count_operations_by_period(user, "income", "per_yesterday"),
        "per_week": count_operations_by_period(user, "income", "per_week"),
        "per_month": count_operations_by_period(user, "income", "per_month"),
        "per_year": count_operations_by_period(user, "income", "per_year"),
        "way": get_ways_of_income(user)
    }
    return user_income_data


def get_user_expense_data(user):
    user_expense_data = {
        "per_today": count_operations_by_period(user, "expense", "per_today"),
        "per_yesterday": count_operations_by_period(user, "expense", "per_yesterday"),
        "per_week": count_operations_by_period(user, "expense", "per_week"),
        "per_month": count_operations_by_period(user, "expense", "per_month"),
        "per_year": count_operations_by_period(user, "expense", "per_year"),
        "way": get_ways_of_income(user)
    }
    return user_expense_data