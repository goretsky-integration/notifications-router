from pymongo import MongoClient

import config
import models

connection = MongoClient(config.MONGODB_URL)
db = connection.dodo


def get_reports_by_report_type(report_type: str) -> tuple[models.ReportFromMongoDB, ...]:
    return tuple(db.reports.find({'report_type': report_type}, {'report_type': 0, '_id': 0}))


def close_mongodb_connection():
    connection.close()
