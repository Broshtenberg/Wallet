def _format_categories(categories):
    """Show categories as a list"""
    text = ''
    for category in categories:
        text += f'• {category}\n'
    return text.strip()


def main_screen(user, count, income, expense):
    text = f"""
Приветствую тебя, @{user}

На твом счету: {count}

💶 Доходы:
• за сегодня: {income["per_today"]}
• за вчера: {income["per_yesterday"]}
• за неделю:  {income["per_week"]}
• за месяц:  {income["per_month"]}
• за год: {income["per_year"]}

Источники доходов:
{_format_categories(income["way"])}

➖ Расходы:
• за сегодня: {expense["per_today"]}
• за вчера: {expense["per_yesterday"]}
• за неделю:  {expense["per_week"]}
• за месяц:  {expense["per_month"]}
• за год: {expense["per_year"]}

"""
    return text
