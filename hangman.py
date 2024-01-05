from word_list import words
from sqlalchemy import ForeignKey, Column, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import sessionmaker
import random


Base = declarative_base()

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    score = Column(Integer, nullable=False)

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    player_name = Column(String, nullable=False)

engine = create_engine("sqlite:///hangman_scores.db")
Base.metadata.create_all(engine)

def get_word():
   hangman_words = words()
   random_word = random.choice(hangman_words)
#    print(random_word)
   return random_word
    


def play(word, selected_player):
    print("WORD: ", word)
    total = 0
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    print("Let's play Hangman!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")
    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").lower()
        print(guess)
        print(guess.isalpha())
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Nice,", guess, "is in the word!")
                total = 1
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Not a valid guess.")
        print(display_hangman(tries))
        print(word_completion)
        print("\n")

    if guessed:
        print("Congrats, you guessed the word! Winner Winner Chicken Dinner!")

        
        Session = sessionmaker(bind=engine)
        session = Session()
        score = Score(player_id=selected_player.id, score=total)
        session.add(score)
        session.commit()

        print("Score saved.")
    else:
        print("Sorry, you suck. The word was " + word + ". Maybe next time!")








def display_hangman(tries):
    stages = [
        """
           +-------+
           |       |
           |       O
           |      \\|/
           |       |
           |      / \\
          ===
        """,

        """
           +-------+
           |       |
           |       O
           |      \\|/
           |       |
           |      / 
          ===
        """,

        """
           +-------+
           |       |
           |       O
           |      \\|/
           |       |
           |      
          ===
        """,

        """
           +-------+
           |       |
           |       O
           |      \\|
           |       |
           |      
          ===
        """,

        """
           +-------+
           |       |
           |       O
           |       |
           |       |
           |      
          ===
        """,

        """
           +-------+
           |       |
           |       O
           |      
           |       
           |      
          ===
        """,

        """
           +-------+
           |       |
           |       
           |      
           |       
           |      
          ===
        """,

    

    ]

    return stages[tries]


Session = sessionmaker(bind=engine)
session = Session()
def main():
    player_name = input("Enter your name: ")
    selected_player = session.query(Player).filter(Player.player_name==player_name).first()
    if not selected_player:
        selected_player = Player(
            player_name = player_name
        )
        session.add_all([selected_player])
        session.commit()
    word = get_word()
    play(word, selected_player)
    while True:
        choice = input("Play Again? (P) / Delete Player? (D) / Edit (E) / Quit? (Q): ").upper()
        
        if choice == "P":
            word = get_word()
            play(word, selected_player)
        elif choice == "D":
            delete_player(selected_player)
            print("Your player has been deleted.")
           
        elif choice =="E":
            edit_player_id(selected_player)
            
        elif choice == "Q":
            break
        else:
            print("Invalid choice. Please choose 'P', 'D', 'E' or 'Q'.")

def edit_player_id(selected_player):
    # selected_player = session.query(Player).filter(Player.player_name==player_name).first()
    change = input("What would you like to change your name to?")
    # Session = sessionmaker(bind=engine)
    # session = Session()
    selected_player.player_name = change
    session.add(selected_player)
    session.commit()

def delete_player(selected_player):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    session.query(Player).filter_by(player_name=selected_player.id).delete()
    session.commit()

if __name__ == "__main__":
    # print(words())
    main()
   
