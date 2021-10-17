import sqlite3 as sql

class WordBankContructor():
    ''' This class builds the word bank used in typer. 
    It can be run through typer by choosing "build word bank" in the main menu. 
    It only needs to be run a single time for each computer.
    Paragraphs used to build the word bank are stored in data.txt''' 

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
        
