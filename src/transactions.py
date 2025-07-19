class Transactions:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS transactions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT,
                Amount FLOAT,
                Tag TEXT,
                Description TEXT
            )'''
        )

        self.conn.commit()

    def add_transaction(self, date : str, amount : int, tag : str, description : str):
        self.cursor.execute("INSERT INTO transactions (Date, Amount, Tag, Description) VALUES (?,?,?,?)",(date, amount, tag, description))
        self.conn.commit()

    def remove_transaction(self):
        pass

    def ord_trans_by_date(self):
        pass

    def ord_trans_by_tag(self):
        pass

    def ord_trans_by_expences(self):
        pass
    

    def print_trans(self):
        self.cursor.execute('''SELECT * FROM transactions''')
        for t in self.cursor.fetchall():
            print(t)


