import sqlite3 as sql

class WordBankContructor():

    def __init__(self):
        self.connecter = sql.connect('typerData.db')
        self.cursor = self.connecter.cursor()

    def populate_wordbank(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS wordbank (
                id INTEGER,
                paragraph TEXT)''')


        with open('paragraphs.txt') as p:
            paragraphs = p.readlines()

            for index, paragraph in enumerate(paragraphs):
                self.cursor.execute('INSERT INTO wordbank VALUES (?, ?)', (index, paragraph))
            self.connecter.commit()
        

wbc = WordBankContructor()
wbc.populate_wordbank()