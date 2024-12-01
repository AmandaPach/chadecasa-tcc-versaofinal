from sqlite3 import connect

db = connect("db.sqlite3", check_same_thread=False)
cursor = db.cursor()


class Table:
    transform_data = None

    def __init__(self, table_name, columns, primary_keys=None, foreign_keys=None, **kwargs):
        self.table_name = table_name
        self.pk = primary_keys if primary_keys else ["id"]
        self.fk = foreign_keys if foreign_keys else []
        self.__generate_table(columns)
        if "transform_data" in kwargs:
            self.transform_data = kwargs["transform_data"]

    def __generate_table(self, columns):
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
        columns_queries = []

        if self.pk == ["id"]:
            columns_queries.append("id INTEGER PRIMARY KEY AUTOINCREMENT")

        for column_name, column_type in columns.items():
            columns_queries.append(f"{column_name} {column_type}")

        if self.pk and self.pk != ["id"]:
            primary_key_query = f"PRIMARY KEY ({', '.join(self.pk)})"
            columns_queries.append(primary_key_query)

        for fk in self.fk:
            fk_query = f"FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]}({fk[2]})"
            columns_queries.append(fk_query)

        query += ", ".join(columns_queries) + ")"
        cursor.execute(query)
        db.commit()

    def create(self, data):
        if self.transform_data:
            data = self.transform_data(data)
        column = ", ".join(data.keys())
        values = ["'" + str(value) + "'" for value in data.values()]
        values = ", ".join(values)
        query = f"INSERT INTO {self.table_name} ({column}) VALUES ({values})"
        cursor.execute(query)
        db.commit()

    def __make_where_clause(self, **kwargs):
        clauses = []
        for key, value in kwargs.items():
            if isinstance(value, list):
                value = value[0]
            clauses.append(f"{key} = '{value}'")
        return " WHERE " + " AND ".join(clauses)

    def list(self, **kwargs):
        where_clause = ""
        if kwargs:
            where_clause = self.__make_where_clause(**kwargs)
        query = f"SELECT * FROM {self.table_name}{where_clause}"

        print(f"DB: {query}")
        cursor.execute(query)

        result_list = cursor.fetchall()
        result_list = [
            dict(zip([column[0] for column in cursor.description], row))
            for row in result_list
        ]
        return result_list

    def get(self, id: int):
        result = self.list(**{self.pk[0]: id})
        return result[0] if result else None

    def delete(self, **kwargs):
        where_clause = self.__make_where_clause(**kwargs)
        query = f"DELETE FROM {self.table_name}{where_clause}"
        print(f"DB: {query}")
        cursor.execute(query)
        db.commit()

    def delete_from_id(self, id):
        query = f"DELETE FROM {self.table_name} WHERE {self.pk[0]} = {id}"
        print(f"DB: {query}")
        cursor.execute(query)
        db.commit()

    def mutation(self, query):
        query = query.strip()
        print(f"DB: {query}")
        cursor.execute(query)
        db.commit()

    def query(self, query):
        query = query.strip()
        print(f"DB: {query}")
        cursor.execute(query)
        result_list = cursor.fetchall()
        result_list = [
            dict(zip([column[0] for column in cursor.description], row))
            for row in result_list
        ]
        return result_list

    def __update_date(self, id):
        query = f"UPDATE {self.table_name} SET data_ultima_alteracao = datetime('now', 'localtime') WHERE {self.pk[0]} = {id}"
        print(f"DB: {query}")
        cursor.execute(query)

    def update(self, id, **kwargs):
        set_clause = ", ".join([f"{key} = '{value}'" for key, value in kwargs.items()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.pk[0]} = {id}"
        print(f"DB: {query}")
        cursor.execute(query)
        last_item_id = self.list()[-1]["id"]
        self.__update_date(last_item_id)

        db.commit()
