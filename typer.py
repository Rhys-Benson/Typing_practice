import sqlite3 as sql
import random

from construct_wordbank import WordBankContructor

class WordBank():

    def __init__(self):
        self.connecter = sql.connect('typerData.db')
        self.cursor = self.connecter.cursor()
        self.constructor = WordBankContructor()

    def random_paragraph(self):
        self.cursor.execute('SELECT paragraph FROM wordbank WHERE id = ?', (random.randint(0, 8),))
        return self.cursor.fetchall()[0][0]

    def build_bank(self):
        self.constructor.populate_wordbank()

    
class Coach():
    def __init__(self):
        self.wordbank = WordBank()

    def display_menu(self):
        print('''\nChoose an option:
        (1) Build word bank
        (2) Manage user
        (3) Practice
        (4) View user stats
        (5) Quit
        ''')
        
    def get_choice(self):
        choice = int(input(''))
        if choice == 1:
            return self.wordbank.build_bank
        elif choice == 2:
            return exit
        elif choice == 3:
            return self.practice
        elif choice == 4:
            return exit

    def practice(self):
        paragragh = self.wordbank.random_paragraph()
        print(paragragh)
        input('Press enter to begin. Remember, punctuation matters.')
        attempt = input('')

        reference = set(paragragh.split())
        correct = 0
        incorrect = []
        for word in attempt.split():
            if word in reference:
                correct += 1
            else:
                incorrect.append(word)

        print(f'\nCorrect words: {correct}\nIncorrect words: {len(incorrect)}')
        for word in incorrect:
            print(word)

def main():
    coach = Coach()
    while True:
        coach.display_menu()
        choice = coach.get_choice()
        choice()


if __name__ == '__main__':
    main()
