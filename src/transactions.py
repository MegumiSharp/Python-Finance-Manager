import datetime

# Convert a date string from 'YYYY-MM-DD' format to 'DD/MM/YYYY' format.
def norm_today():
    date = str(datetime.date.today())
    return f'{date[8:10]}/{date[5:7]}/{date[:4]}'


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

    def add_transaction(self, date = None, amount = None, tag = None, description = None):
        if date is None:
            date = norm_today()  # default dinamico per la data

        if amount is None:
            amount = 0
    
        if tag is None:
            tag = "None"
            
        if description is None:
            description = ""

        self.cursor.execute("INSERT INTO transactions (Date, Amount, Tag, Description) VALUES (?,?,?,?)",(date, amount, tag, description))
        self.conn.commit()

    def remove_transaction(self, id : int):
        self.cursor.execute("DELETE FROM transactions WHERE ID = ?",(id,))
        self.conn.commit()
        

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


