import datetime

from sqlalchemy import and_

from app.models.database.base import Sale
from app.utils.utils import datetime_parse


def time_range_condition_builder(condition, start_date, end_date):
    if start_date:
        if start_date.isdigit():
            start_date = datetime.datetime.fromisoformat(start_date)
        else:
            start_date = datetime_parse(start_date)

        condition = Sale.sold_at >= start_date

    if end_date:
        if end_date.isdigit():
            end_date = datetime.datetime.fromisoformat(end_date)
        else:
            end_date = datetime_parse(end_date)
        condition = and_(condition, Sale.sold_at <= end_date)

    return condition
