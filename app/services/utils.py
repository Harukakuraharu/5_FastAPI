import json
from datetime import date, datetime


async def model_to_string(data: list) -> str:
    """
    Converter model object on string for set in cache

    :param data: data with model object

    :return: str object
    """
    converter_data = [field.to_dict() for field in data]
    for field in converter_data:
        for key, value in field.items():
            if isinstance(value, date):
                field[key] = value.strftime("%Y-%m-%d")
    return json.dumps(converter_data)


async def date_to_string(data: list) -> str:
    """
    Converter datetime type on string for set in cache

    :param data: data with date

    :return: str object
    """
    converter_data = [{"date": day.strftime("%Y-%m-%d")} for day in data]
    return json.dumps(converter_data)


async def string_to_date(data: list) -> list:
    """
    Converter date with string type on date format

    :param data: data with string

    :return: list with date object
    """
    converter_data = [
        {"date": datetime.strptime(day["date"], "%Y-%m-%d").date()}
        for day in data
    ]
    return converter_data
