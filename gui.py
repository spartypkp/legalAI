from tkinter import *

import createAbe

def main():
    pass

def clear_all():
    question_field.delete(0, END)
    question_field.focus_set()

def call_abe(question):
    if question != "":
        final_answer, relevant_sections = createAbe(question)
        output_field.insert(10, final_answer)
        relevant_section_field.insert(10, relevant_sections)


if __name__ == "__main__":
    root = Tk()
    root.configure(bg="white")
    root.title("Ask AI Abe")
    root.geometry("920x640")
    label1 = Label(root, text="Enter a legal question here: ")
    question_field = Entry(root) 
    label1.grid(row=1, column=0, padx=10, pady=10)
    question_field.grid(row=1, column=1, padx=10, pady=10)
    button1 = Button(root, text = "Submit", command = call_abe(question_field.get()))
    button2 = Button(root, text = "Reset", command = clear_all)
    button1.grid(row = 1, column = 2, padx=10, pady=10)

    output_field = Entry(root)
    relevant_section_field = Entry(root)
    label4 = Label(root, text="AI Abe's Output")
    label5 = Label(root, text="Relevant Legal Sections")

    label4.grid(row=2, column=0, padx=10, pady=10)
    output_field.grid(row=2, column=1)

    label5.grid(row=3, column=0, padx=10, pady=10)
    relevant_section_field.grid(row=3, column=1, padx=10, pady=10)
    root.mainloop()
