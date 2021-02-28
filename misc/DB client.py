import psycopg2


hostname = '10.10.20.12'
login = 'application'
password = '5SjMW6Ey'
db_name = 'pkm_dev_classes'


db_connect = psycopg2.connect(host=hostname, user=login, password=password, dbname=db_name)
try:
    cursor = db_connect.cursor()
    cursor.execute("SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tree' ORDER BY ORDINAL_POSITION")
    fields = cursor.fetchall()
    cursor.execute("SELECT * FROM tree WHERE type='folder'")
    results = cursor.fetchall()
    end_result = []
    for data in results:
        current_result = {}
        field_index = 0
        for field_value in data:
            current_result[fields[field_index][0]] = field_value
            field_index += 1
        end_result.append(current_result)
    print(end_result)
finally:
    db_connect.close()