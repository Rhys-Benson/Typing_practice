import sqlite3 as sql
import random
import timeit

from construct_wordbank import WordBankContructor

class WordBank():
    # A class to manage interactions with the database
    def __init__(self):
        self.connecter = sql.connect('typerData.db')
        self.cursor = self.connecter.cursor()
        self.constructor = WordBankContructor()

        # Specifies to the program which user to save to and select from.
        self.user = None

    def random_paragraph(self):
        # Returns a random paragraph from the wordbank table
        self.cursor.execute('SELECT paragraph FROM wordbank WHERE id = ?', (random.randint(0, 8),))
        return self.cursor.fetchall()[0][0]

    def build_bank(self):
        # Calls the WordBankConstructor class to build the word bank
        self.constructor.populate_wordbank()

    def new_user(self):
        # Create a new user. Each user is represented by a unique table in the data base
        username = input("Username: ")
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {username} (
            correct INTEGER,
            incorrect INTEGER,
            wpm REAL)''')
        
        self.connecter.commit()
        self.user = username

    def select_user(self):
        # Displays all users and prompts for a user to be selected. self.user will then be updated
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for index, user in enumerate(self.cursor.fetchall()):
            if index != 0:
                print(user[0])

        user = input('Which user would you like to select? ')
        self.user = user


    def delete_user(self):
        # Displays all users and prompts for a user to be deleted. The table for that user will be dropped
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for index, user in enumerate(self.cursor.fetchall()):
            if index != 0:
                print(user[0])

        user = input('Which user would you like to delete? ')
        self.cursor.execute(f'DROP TABLE {user};')
        self.connecter.commit()

    def save_practice(self, correct, incorrect, wpm):
        # Update the selected user's table with the data from the current practice session
        self.cursor.execute(f'INSERT INTO {self.user}(correct, incorrect, wpm) VALUES(?,?,?)', (correct, incorrect, wpm))
        self.connecter.commit()

    def display_stats(self):
        # Prints all saved data for the selected user including the fastest words/minute recorded and average mistakes per session.
        self.cursor.execute(f'SELECT * FROM {self.user}')
        all_data = self.cursor.fetchall()
        for attempt in all_data:
            print(f'Correct: {attempt[0]} | Incorrect: {attempt[1]} | words/minute: {attempt[2]}')

        self.cursor.execute(f'SELECT MAX(wpm) FROM {self.user}')
        print(f'Personal record: {self.cursor.fetchall()[0][0]} words/minute')

        self.cursor.execute(f'SELECT AVG(incorrect) FROM {self.user}')
        print(f'Average mistakes: {self.cursor.fetchall()[0][0]}')

    
class Coach():
    # The Coach class handles interactions with the user, and calls on WordBank to make transactions with the database.
    def __init__(self):
        self.wordbank = WordBank()

    def main_menu(self):
        # Display the main menu and prompt the user to choose an option. 
        # Returns a function that will fulfill the request made by the user.
        print(f'''\nChoose an option:
        Current user is {self.wordbank.user}
        (1) Build word bank
        (2) Manage users
        (3) Practice
        (4) View user stats
        (5) Quit
        ''')

        choice = int(input(''))
        if choice == 1:
            return self.wordbank.build_bank
        elif choice == 2:
            return self.user_menu
        elif choice == 3:
            if self.wordbank.user is not None:
                return self.practice
            else:
                print('You must select a user first')
                return self.user_menu
        elif choice == 4:
            if self.wordbank.user is not None:
                return self.wordbank.display_stats
            else:
                print('You must select a user first')
                return self.user_menu
        elif choice == 5:
            return exit

    def user_menu(self):
        # Displays the user management menu and prompts user to choose an option.
        # This function will make a function call based on the user's choice.
        print('''\nChoose an option:
        (1) New User
        (2) Select User
        (3) Delete User
        (4) Main menu
        ''')

        choice = int(input(''))
        if choice == 1:
            self.wordbank.new_user()
        elif choice == 2:
            self.wordbank.select_user()
        elif choice == 3:
            self.wordbank.delete_user()
        elif choice == 4:
            pass

    def practice(self):
        # Handles all the logic of a typing practice session

        # Grabs a random paragraph and displays to the user
        paragragh = self.wordbank.random_paragraph()
        print(paragragh)
        # Give the user a second to read the paragraph and choose when they begin
        input('Press enter to begin. Remember, punctuation matters.')
        # record how long it takes for the user to finish typing
        start = timeit.default_timer()
        attempt = input('')
        attempt_time = timeit.default_timer() - start
        mins = attempt_time / 60

        # Checks for how many of the words typed by the user match words in the paragraph. Mispelled words are added to a list.
        reference = set(paragragh.split())
        correct = 0
        incorrect = []
        for word in attempt.split():
            if word in reference:
                correct += 1
            else:
                incorrect.append(word)

        wpm = correct / mins

        # Display session data
        print(f'\nCorrect words: {correct}\nIncorrect words: {len(incorrect)}')
        for word in incorrect:
            print(word)
        print(f'words/minute: {wpm}')

        # save user's session data
        save = input("Would you like to save this session's data? [y/n]")
        if save == 'y':
            self.wordbank.save_practice(correct, len(incorrect), wpm)
               

    

def main():
    coach = Coach()
    while True:
        choice = coach.main_menu()
        choice()


if __name__ == '__main__':
    main()
