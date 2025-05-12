import random
import time
import threading
import csv

QUESTIONS_PER_ROUND = 4
TIME_LIMIT = 10
score = 0
timer_expired = False
current_answer = None

def load_questions_from_csv(file_path):
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

def run_timer():
    """Shows the timer countdown dynamically."""
    global timer_expired
    timer_expired = False
    start_time = time.time()

    while True:
        if current_answer is not None or timer_expired:
            print("\r" + " " * 30, end="\r")
            return

        elapsed = time.time() - start_time
        remaining_time = TIME_LIMIT - int(elapsed)

        if remaining_time <= 0:
            timer_expired = True
            print("\nTime's up! Moving to next question.")
            return

        print(f"\rTime remaining: {remaining_time} seconds", end="")
        time.sleep(1)

def run_quiz():
    """Main quiz logic with clean timer display"""
    global score, current_answer, timer_expired
    questions = load_questions_from_csv("questions.csv")

    if not questions:
        return

    print("\nWelcome to the Quiz Game!")
    time.sleep(1)

    round_questions = random.sample(questions, QUESTIONS_PER_ROUND)

    for q in round_questions:
        current_answer = None
        timer_expired = False

        print(f"\n{q['question']}")
        for choice in q["choices"]:
            print(choice)

        timer_thread = threading.Thread(target=run_timer)
        timer_thread.start()

        try:
            print("\r" + " " * 30, end="\r")
            current_answer = input("Your answer (A, B, C, D): ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted. Exiting...")
            return

        timer_thread.join()

        if timer_expired:
            print(f"Too slow! Correct answer was {q['answer']}.")
        elif current_answer == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer was {q['answer']}.")

        time.sleep(1)

    print(f"\nYour score: {score}/{QUESTIONS_PER_ROUND}")

def main():
    while True:
        print("\n1. Start Quiz\n2. Exit")
        choice = input("Choose: ").strip()

        if choice == '1':
            run_quiz()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
