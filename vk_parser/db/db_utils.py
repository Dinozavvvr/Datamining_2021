# -*- coding: utf-8 -*-
# Created by dinar at 02.03.2021

import psycopg2


class PostgreSql:
    __SQL_GET_COLUMNS = "SELECT column_name FROM information_schema.columns " \
                        "WHERE table_schema = '{schema_name}' AND table_name = '{table}'"

    __SQL_TRUNCATE_TABLE = "TRUNCATE TABLE {table}"

    def __init__(self, db_name, user,
                 password, host, schema_name):
        self.autocommit = True
        self.connection = PostgreSql.get_connection(db_name, user,
                                                    password, host)
        self.schema_name = schema_name

    # custom save method into db
    def save(self, table_name, generated_columns=(), return_id=False, **values):

        with self.connection.cursor() as cursor:

            columns = self.get_columns(self, table_name)
            for col in generated_columns:
                columns.remove(col)

            vals = ''
            for (column_name, value) in values.items():
                if type(value) is str:
                    values[column_name] = f"'{value}'"
                vals += '{' + column_name + '},'
            vals = vals[:-1]

            insert_sql = ('INSERT INTO "{table}"({params}) VALUES (' + vals + ')').format(
                table=table_name,
                params=','.join(columns),
                **values)

            if return_id:
                insert_sql += f"RETURNING {generated_columns[0]}"

            cursor.execute(insert_sql)
            self.connection.commit()

            if return_id:
                return cursor.fetchone()[0]

    @staticmethod
    def get_connection(db_name, user,
                       password, host):
        return psycopg2.connect(dbname=db_name, user=user,
                                password=password, host=host)

    @staticmethod
    def get_columns(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(str(self.__SQL_GET_COLUMNS).format(schema_name=self.schema_name,
                                                          table=table_name))
        result_set = cursor.fetchall()
        result_list = list(map(lambda row: row[0], result_set))
        cursor.close()
        return result_list

    def clear_table(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute(str(self.__SQL_TRUNCATE_TABLE).format(table=table_name))


class PreparedStatement:
    # insert into user(name, surname) values (?, ?)

    # prepared_statement = connection.prepared_statement(sql)
    # prepared_statement.set_str(1, 'word')
    # prepared_statement.set_int(2, 7)
    # prepared_statement.set_int(3, 9)
    # prepared_statement.return_id('id_name')
    # result_set = prepared_statement.execute()

    # prepared_statement = connection.prepared_statement(SQL)
    #
    # for i in range(10):
    #   prepared_statement.set_int(1, int_value)
    #   prepared_statement.execute()
    pass
