import tkinter as tk
from tkinter import messagebox
from questions import questions # type: ignore

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Scientist Quiz - Pega Knowledge Test")
        self.master.geometry("800x500")
        self.master.configure(bg="#f0f0f0")
        self.score = 0
        self.current_question = 0
        self.answers_selected = {}  # To store selected answers for each question
        self.elapsed_time = 0  # Time elapsed in seconds
        self.timer_running = False  # To control the timer

        # Welcome message
        self.welcome_label = tk.Label(
            self.master,
            text="Welcome to the Data Scientist Quiz!\n"
                "Answer the questions by selecting the correct option(s).\n"
                "Let's begin!",
            font=("Arial", 16),
            justify="center",
            bg="#f0f0f0"
        )
        self.welcome_label.pack(pady=50)

        # Start button
        self.start_button = tk.Button(
            self.master,
            text="Start Quiz",
            command=self.start_quiz,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        self.start_button.pack(pady=20)

    def start_quiz(self):
        # Clear welcome screen
        self.welcome_label.destroy()
        self.start_button.destroy()

        # Initialize timer
        self.timer_label = tk.Label(
            self.master,
            text="Time Elapsed: 00:00",
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="black"
        )
        self.timer_label.pack(pady=10)
        self.timer_running = True
        self.update_timer()

        # Frame for the question
        self.question_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.question_frame.pack(pady=20)
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            wraplength=650,
            font=("Arial", 14),
            bg="#f0f0f0"
        )
        self.question_label.pack()

        # Frame for the options
        self.options_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.options_frame.pack(pady=10)
        self.vars = []  # List to store Checkbutton variables
        self.check_buttons = []

        # Feedback label
        self.feedback_label = tk.Label(
            self.master,
            text="",
            font=("Arial", 14),
            bg="#f0f0f0"
        )
        self.feedback_label.pack(pady=20)

        # Buttons
        self.feedback_button = tk.Button(
            self.master,
            text="Show Feedback",
            command=self.show_feedback,
            font=("Arial", 12),
            bg="#008CBA",
            fg="white",
            padx=10,
            pady=5
        )
        self.feedback_button.pack(pady=10)

        self.previous_button = tk.Button(
            self.master,
            text="Previous Question",
            command=self.previous_question,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=5
        )
        self.previous_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(
            self.master,
            text="Next Question",
            command=self.next_question,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # Load the first question
        self.load_question()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"Time Elapsed: {minutes:02}:{seconds:02}")
            self.master.after(1000, self.update_timer)

    def load_question(self):
        if self.current_question < len(questions):
            q = questions[self.current_question]
            self.question_label.config(text=f"Q{self.current_question + 1}: {q['question']}")
            self.vars = []  # Reset variables
            for widget in self.options_frame.winfo_children():
                widget.destroy()  # Clear previous options
            for idx, option in enumerate(q['options']):
                var = tk.BooleanVar()
                if self.current_question in self.answers_selected:
                    var.set(option[0].lower() in self.answers_selected[self.current_question])
                self.vars.append(var)
                cb = tk.Checkbutton(
                    self.options_frame,
                    text=option,
                    variable=var,
                    font=("Arial", 12),
                    bg="#f0f0f0"
                )
                cb.pack(anchor='w')
                self.check_buttons.append(cb)

            # Disable Previous Button on the first question
            if self.current_question == 0:
                self.previous_button.config(state=tk.DISABLED)
            else:
                self.previous_button.config(state=tk.NORMAL)
        else:
            self.show_score()

    def show_feedback(self):
        selected = [opt[0] for opt, var in zip(questions[self.current_question]['options'], self.vars) if var.get()]
        if not selected:
            self.feedback_label.config(text="Please select at least one option before proceeding.", fg="red")
            return

        correct_answers = questions[self.current_question]['answer']
        if isinstance(correct_answers, list):  # Multiple correct answers
            if set(selected) == set(correct_answers):
                self.feedback_label.config(text="Correct!", fg="green")
            else:
                correct_options = [opt for opt in questions[self.current_question]['options'] 
                        if any(opt.startswith(ans) for ans in correct_answers)]
                self.feedback_label.config(text=f"Wrong! The correct answers are: {', '.join(correct_options)}", fg="red")
        else:  # Single correct answer
            if len(selected) == 1 and selected[0] == correct_answers:
                self.feedback_label.config(text="Correct!", fg="green")
            else:
                correct_option = next(opt for opt in questions[self.current_question]['options'] 
                        if opt.startswith(correct_answers))
                self.feedback_label.config(text=f"Wrong! The correct answer is: {correct_option}", fg="red")

    def next_question(self):
        # Save the current selection
        selected = [opt[0] for opt, var in zip(questions[self.current_question]['options'], self.vars) if var.get()]
        self.answers_selected[self.current_question] = selected

        # Clear feedback
        self.feedback_label.config(text="", fg="green")

        # Move to the next question
        self.current_question += 1
        self.load_question()

    def previous_question(self):
        # Save the current selection
        selected = [opt[0] for opt, var in zip(questions[self.current_question]['options'], self.vars) if var.get()]
        self.answers_selected[self.current_question] = selected

        # Clear feedback
        self.feedback_label.config(text="", fg="green")

        # Move to the previous question
        if self.current_question > 0:
            self.current_question -= 1
        self.load_question()

    def show_score(self):
        # Stop the timer
        self.timer_running = False

        for widget in self.master.winfo_children():
            widget.destroy()

        # Calculate time taken
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60

        score_percentage = (self.score / len(questions)) * 100
        score_text = f"You scored {self.score} out of {len(questions)} ({score_percentage:.2f}%)\n"
        time_text = f"Time Taken: {minutes:02}:{seconds:02}"

        # Score label
        score_label = tk.Label(
            self.master,
            text=score_text + time_text,
            font=("Arial", 18),
            bg="#f0f0f0",
            fg="black"
        )
        score_label.pack(pady=30)

        # Feedback label
        if self.score == len(questions):
            feedback = "Excellent! You have a strong grasp of the material."
        elif self.score >= len(questions) // 2:
            feedback = "Good job! You might want to review a few concepts."
        else:
            feedback = "Keep studying! Revisit the material for better understanding."
        feedback_label = tk.Label(
            self.master,
            text=feedback,
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="black"
        )
        feedback_label.pack(pady=20)

        # Restart button
        restart_button = tk.Button(
            self.master,
            text="Restart Quiz",
            command=self.restart_quiz,
            font=("Arial", 12),
            bg="#008CBA",
            fg="white",
            padx=10,
            pady=5
        )
        restart_button.pack(pady=20)

    def restart_quiz(self):
        self.score = 0
        self.current_question = 0
        self.answers_selected = {}
        self.elapsed_time = 0  # Reset elapsed time
        self.__init__(self.master)

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()