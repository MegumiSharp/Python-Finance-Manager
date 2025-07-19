class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Transactions:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS transactions (
                date TEXT,
                amount FLOAT,
                tag TEXT,
                desc TEXT
            )'''
        )

        self.conn.commit()

    def add_transaction(self, date : str, amount : int, tag : str, description : str):
        self.cursor.execute("INSERT INTO transactions (date, amount, tag, desc) VALUES (?,?,?,?)",(date, amount, tag, description))
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


