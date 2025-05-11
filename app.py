import random
import time
import threading
import csv

class QuizGame:
    def __init__(self):
        self.questions_per_round = 4
        self.time_limit = 10  # seconds
        self.score = 0
        self.timer_expired = False
        self.current_answer = None
        self.questions = self.load_questions_from_csv("questions.csv") 

    def load_questions_from_csv(self, file_path):
        """Load questions from a CSV file."""
        questions = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    questions.append({
                        "question": row["question"],
                        "choices": row["choices"].split(","),
                        "answer": row["answer"]
                    })
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except KeyError:
            print("Error: The CSV file is missing required columns (question, choices, answer).")
        return questions

    def run_timer(self):
        """Shows the timer countdown dynamically."""
        self.timer_expired = False
        start_time = time.time()

        while True:
            if self.current_answer is not None or self.timer_expired:
            
                print("\r" + " " * 30, end="\r")
                return

            elapsed = time.time() - start_time
            remaining_time = self.time_limit - int(elapsed)

            if remaining_time <= 0:
                self.timer_expired = True
                print("\nTime's up! Moving to next question.")
                return

            print(f"\rTime remaining: {remaining_time} seconds", end="")
            time.sleep(1)

    def run_quiz(self):
        """Main quiz logic with clean timer display"""
        print("\nWelcome to the Quiz Game!")
        time.sleep(1)

        round_questions = random.sample(self.questions, self.questions_per_round)

        for q in round_questions:
            self.current_answer = None
            self.timer_expired = False

            print(f"\n{q['question']}")
            for choice in q["choices"]:
                print(choice)

            timer_thread = threading.Thread(target=self.run_timer)
            timer_thread.start()

            try:
                
                print("\r" + " " * 30, end="\r")
                self.current_answer = input("Your answer (A, B, C, D): ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted. Exiting...")
                return

            timer_thread.join()

         
            if self.timer_expired:
                print(f"Too slow! Correct answer was {q['answer']}.")
            elif self.current_answer == q["answer"]:
                print("Correct!")
                self.score += 1
            else:
                print(f"Wrong! Correct answer was {q['answer']}.")

            time.sleep(1)

        
        print(f"\nYour score: {self.score}/{self.questions_per_round}")

def main():
    quiz = QuizGame()
    
    while True:
        print("\n1. Start Quiz\n2. Exit")
        choice = input("Choose: ").strip()
        
        if choice == '1':
            quiz.run_quiz()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()