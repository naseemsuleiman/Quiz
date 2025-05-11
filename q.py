import csv


questions = [
    {
        "question": "What is the capital of Kenya?",
        "choices": "A) Nairobi,B) Mombasa,C) Kisumu,D) Nakuru",
        "answer": "A"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": "A) Earth,B) Mars,C) Jupiter,D) Venus",
        "answer": "B"
    },
    {
        "question": "What is the chemical symbol for water?",
        "choices": "A) H2O,B) CO2,C) O2,D) NaCl",
        "answer": "A"
    },
    {
        "question": "Who wrote 'Hamlet'?",
        "choices": "A) Charles Dickens,B) William Shakespeare,C) J.K. Rowling,D) Jane Austen",
        "answer": "B"
    }
]


file_path = "questions.csv"
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["question", "choices", "answer"])
    writer.writeheader()  
    writer.writerows(questions)  

print(f"CSV file '{file_path}' created successfully!")