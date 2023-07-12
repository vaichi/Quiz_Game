import tkinter as tk
import mysql.connector
from datetime import datetime
from tkinter import messagebox

# Establish MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vaiga1234",
    database="quiz"
)

# Create cursor
cursor = connection.cursor()

# Global variables
questions = []
question_num = 0
score = 0
username = ""

def load_questions():
    global questions
    query = "SELECT * FROM questions"
    cursor.execute(query)
    questions = cursor.fetchall()

def display_question():
    question_label.config(text=questions[question_num][1])
    options_label.config(text=f"A. {questions[question_num][2]}\n"
                             f"B. {questions[question_num][3]}\n"
                             f"C. {questions[question_num][4]}\n"
                             f"D. {questions[question_num][5]}")

    marks_label.config(text=f"Marks: {questions[question_num][7]}")
    score_label.config(text=f"Current Score: {score}")

def check_answer():
    global question_num, score, username
    guess = input_entry.get().upper()
    input_entry.delete(0, tk.END)

    if guess not in ['A', 'B', 'C', 'D']:
        messagebox.showwarning("Warning", "Invalid input! Please enter A, B, C, or D.")
        return

    if guess == questions[question_num][6]:
        score += questions[question_num][7]

    question_num += 1

    if question_num == len(questions):
        save_result()
        quiz_window.destroy()
        display_leaderboard()
    else:
        display_question()

def save_result():
    global username, score
    attempted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    result_query = "SELECT * FROM quiz_results WHERE username = %s"
    cursor.execute(result_query, (username,))
    existing_record = cursor.fetchone()

    if existing_record:
        messagebox.showwarning("Warning", "Username already exists!")
    else:
        insert_query = "INSERT INTO quiz_results (username, score) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, score))
        connection.commit()

def display_leaderboard():
    leaderboard_window = tk.Tk()
    leaderboard_window.title("Quiz Leaderboard")
    leaderboard_window.geometry("300x200")
    leaderboard_window.configure(bg="black")

    leaderboard_query = "SELECT username, score FROM quiz_results ORDER BY score DESC"
    cursor.execute(leaderboard_query)
    leaderboard_data = cursor.fetchall()

    leaderboard_text = "Leaderboard:\n"
    for index, row in enumerate(leaderboard_data, start=1):
        leaderboard_text += f"{index}. {row[0]} - Score: {row[1]}\n"

    leaderboard_label = tk.Label(leaderboard_window, text=leaderboard_text, font=("Arial", 14), fg="white", bg="black")
    leaderboard_label.pack(pady=10)

# Create the main window
window = tk.Tk()
window.title("Quiz Game")
window.geometry("500x400")
window.configure(bg="black")

def start_quiz():
    global username
    username = username_entry.get().strip()

    if username == "":
        messagebox.showwarning("Warning", "Please enter a valid username!")
        return

    username_entry.delete(0, tk.END)

    result_query = "SELECT * FROM quiz_results WHERE username = %s"
    cursor.execute(result_query, (username,))
    existing_record = cursor.fetchone()

    if existing_record:
        messagebox.showwarning("Warning", "Username already exists!")
        return

    username_label.grid_forget()
    username_entry.grid_forget()
    start_button.grid_forget()

    load_questions()
    display_question()

    # Create the submit button
    submit_button = tk.Button(quiz_window, text="Submit", font=("Arial", 14), command=check_answer)
    submit_button.grid(row=4, column=0, padx=10, pady=10, sticky="W")

    quiz_window.deiconify()

# Create the username window
username_window = tk.Frame(window, bg="black")
username_window.pack(pady=50)

# Create the username label
username_label = tk.Label(username_window, text="Enter your username:", font=("Arial", 14), fg="white", bg="black")
username_label.grid(row=0, column=0, padx=10, pady=10)

# Create the username entry box
username_entry = tk.Entry(username_window, font=("Arial", 14), fg="black")
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the start button
start_button = tk.Button(username_window, text="Start Quiz", font=("Arial", 14), command=start_quiz)
start_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create the quiz window
quiz_window = tk.Toplevel(window)
quiz_window.title("Quiz")
quiz_window.geometry("500x400")
quiz_window.configure(bg="black")
quiz_window.withdraw()

# Create the question label
question_label = tk.Label(quiz_window, text="", font=("Helvetica", 18, "bold"), wraplength=400, fg="white", bg="black")
question_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create the options label
options_label = tk.Label(quiz_window, text="", font=("Arial", 14), fg="white", bg="black")
options_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create the marks label
marks_label = tk.Label(quiz_window, text="", font=("Arial", 14), fg="white", bg="black")
marks_label.grid(row=2, column=0, padx=10, pady=10)

# Create the score label
score_label = tk.Label(quiz_window, text="", font=("Arial", 14), fg="white", bg="black")
score_label.grid(row=2, column=1, padx=10, pady=10)

# Create the input box
input_entry = tk.Entry(quiz_window, font=("Arial", 14), fg="black")
input_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the tkinter event loop
window.mainloop()

# Close cursor and connection
cursor.close()
connection.close()