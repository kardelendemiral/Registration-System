from django.db import connection

def run_statement(statement):
    cursor= connection.cursor()
    cursor.execute(statement)
    return cursor.fetchall()
def catch_statement(statement):
    cursor= connection.cursor()
    cursor.execute(statement)
    return cursor.fetchone()[0]

