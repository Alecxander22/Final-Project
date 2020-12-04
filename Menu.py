# Alecxander Butler CIS 345 T/Th 12:00 Mental Anguish
from tkinter import *
from file_handle import *
from random import sample


def edit_question(event):

    global win, question_text, point_value, correct_feedback, incorrect_feedback, \
        correct_choice, choice1, choice2, choice3, list_box, edit_menu, edit_mode, \
        edit_index, edit_ques, delete_btn

    edit_index = list_box.curselection()[0]
    edit_ques = question_list[edit_index]
    edit_mode = True

    question_text.set(edit_ques.question_text)
    point_value.set(edit_ques.point_value)
    correct_feedback.set(edit_ques.correct_feedback)
    incorrect_feedback.set(edit_ques.incorrect_feedback)
    correct_choice.set(edit_ques.correct_choice)
    choice1.set(edit_ques.choices[1])
    choice2.set(edit_ques.choices[2])
    choice3.set(edit_ques.choices[3])

    delete_btn.grid(row=8, column=1)


def delete_question():
    global list_box, question_list, edit_index

    edit_index = list_box.curselection()[0]
    question_list.pop(edit_index)
    list_box.delete(edit_index)
    save_questions(question_list)

    clear_text_variables()


def start_quiz():
    global question_text, point_value, question_list, quiz_questions, quiz_question
    list_box.forget()
    add_frame.forget()
    list_label.forget()
    quiz_frame.pack()
    quiz_frame.pack_propagate(0)
    exit_quiz_btn.grid(row=7, column=0)
    quiz_questions = sample(question_list, 3)
    quiz_questions = iter(quiz_questions)
    next_question_button.grid(row=7, column=1)
    next_question()


def evaluate_question():
    global question_selection, question_list, feedback, point_total, question_total, next_question_button,\
        quiz_question, submit_question_btn, quiz_question, feedback_label, randomized_choices

    correct_question_index = 10
    submit_question_btn.forget()

    for i in range(4):
        if quiz_question.correct_choice == randomized_choices[i]:
            correct_question_index = i
            break

    if question_selection.get() == correct_question_index:
        point_total.set(point_total.get() + quiz_question.point_value)
        feedback.set(value=quiz_question.correct_feedback)
    else:
        feedback.set(value=quiz_question.incorrect_feedback)
    question_total.set(value=question_total.get() + 1)

    feedback_label.grid(row=6, column=1)
    submit_question_btn['state'] = 'disabled'

    if question_total.get() != 3:
        next_question_button.grid(row=7, column=1)


def exit_quiz():
    list_label.pack()
    list_box.pack()
    add_frame.pack()
    quiz_frame.forget()

    question_total.set(value=0)
    point_total.set(value=0)
    clear_text_variables()


def next_question():
    global quiz_question, quiz_questions, next_question_button, randomized_choices

    quiz_question = next(quiz_questions)

    next_question_button.grid_forget()
    feedback_label.grid_forget()
    submit_question_btn.grid(row=5, column=0)
    submit_question_btn['state'] = 'normal'

    question_text.set(quiz_question.question_text)
    point_value.set(quiz_question.point_value)
    randomized_choices = sample(quiz_question.choices, 4)
    choice0.set(randomized_choices[0])
    choice1.set(randomized_choices[1])
    choice2.set(randomized_choices[2])
    choice3.set(randomized_choices[3])


def add_question():
    '''Creates a new form underneath the list for the user to fill in, and submit,
    the submit process actually happens in the next method, this is to "open" the form
    and gather the data'''
    global point_value, correct_feedback, incorrect_feedback, \
        correct_choice, choice1, choice2, choice3, question_list, add_frame, question_text, edit_index, edit_mode

    # \ is not allowed

    choices = [correct_choice.get(), choice1.get(), choice2.get(), choice3.get()]
    temp_question = Question(point_value=int(point_value.get()), question_text=question_text.get(),
                             correct_feedback=correct_feedback.get(), incorrect_feedback=incorrect_feedback.get(),
                             correct_choice=correct_choice.get(), choices=choices)
    if edit_mode:
        question_list[edit_index] = temp_question
        list_box.delete(edit_index)
        list_box.insert(edit_index, temp_question)
        edit_mode = False
    else:
        list_box.insert(END, temp_question)
        question_list.append(temp_question)

    save_questions(question_list)
    clear_text_variables()


def clear_text_variables():
    question_text.set('')
    point_value.set('')
    correct_feedback.set('')
    incorrect_feedback.set('')
    correct_choice.set('')
    choice0.set('')
    choice1.set('')
    choice2.set('')
    choice3.set('')


def search_question():
    pass
#     for question in question_list:
#         Loop through question list and append question text to a search_question_text list
#     close matches list  = get close matches(question_search.get(), search_question_text_list, cutoff=.3)
# Have to search through question text, choices, and feedback
#
#     Bring up search question frame
#     Similar_questions = get_close_matches(search word, quest
#       for similar question in similar_questions
#           append to end of a listbox




win = Tk()
win.geometry('800x700')

question_text = StringVar()
point_value = StringVar()
correct_feedback = StringVar()
incorrect_feedback = StringVar()
correct_choice = StringVar()
choice0 = StringVar()
choice1 = StringVar()
choice2 = StringVar()
choice3 = StringVar()
question_selection = IntVar()
point_total = IntVar(value=0)
question_total = IntVar(value=0)
feedback = StringVar()
quiz_questions = list()
quiz_question = None
randomized_choices = list()

edit_index = 0
edit_ques = None
edit_mode = False

menu_bar = Menu(win)
win.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=False)
edit_menu = Menu(menu_bar, tearoff=False)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
menu_bar.add_command(label='Take a Quiz', command=start_quiz)
file_menu.add_command(label='Exit', command=win.quit)
edit_menu.add_command(label='Add Question', command=add_question)
edit_menu.add_command(label='Delete Question', command=delete_question)

list_label = Label(win, text='Double click to edit a question')
list_label.pack()

list_box = Listbox(win, width=40, height=20)
list_box.pack()
list_box.bind('<Double-Button-1>', edit_question)
question_list = retrieve_questions()
for question in question_list:
    list_box.insert(END, question)

add_frame = Frame(win, width=300, height=150, borderwidth=5, bg='PeachPuff')
add_frame.pack()
add_frame.pack_propagate(0)
# The add_frame is packed here so it appears when the user clicks to access the add_form

text_lbl = Label(add_frame, text='Question text:')
text_lbl.grid(row=0, column=0)
text_entry = Entry(add_frame, textvariable=question_text, width=50)
text_entry.grid(row=0, column=1)

point_lbl = Label(add_frame, text='Point value: ')
point_lbl.grid(row=1, column=0, sticky='e')
point_entry = Entry(add_frame, textvariable=point_value, width=10)
point_entry.grid(row=1, column=1, sticky='w')

cor_fb_lbl = Label(add_frame, text='Correct feedback: ', width=40)
cor_fb_lbl.grid(row=2, column=0)
cor_fb_entry = Entry(add_frame, textvariable=correct_feedback, width=40)
cor_fb_entry.grid(row=2, column=1)

incor_fb_lbl = Label(add_frame, text='Incorrect feedback:', width=40)
incor_fb_lbl.grid(row=3, column=0)
incor_fb_entry = Entry(add_frame, textvariable=incorrect_feedback, width=40)
incor_fb_entry.grid(row=3, column=1)

cor_choice_lbl = Label(add_frame, text='Correct answer:')
cor_choice_lbl.grid(row=4, column=0)
cor_choice_entry = Entry(add_frame, textvariable=correct_choice, width=40)
cor_choice_entry.grid(row=4, column=1)

choice_1_label = Label(add_frame, text='Incorrect answer:')
choice_1_label.grid(row=5, column=0)
choice_1_entry = Entry(add_frame, textvariable=choice1, width=40)
choice_1_entry.grid(row=5, column=1)

choice_2_label = Label(add_frame, text='Incorrect answer:')
choice_2_label.grid(row=6, column=0)
choice_2_entry = Entry(add_frame, textvariable=choice2, width=40)
choice_2_entry.grid(row=6, column=1)

choice_3_label = Label(add_frame, text='Incorrect answer:')
choice_3_label.grid(row=7, column=0)
choice_3_entry = Entry(add_frame, textvariable=choice3, width=40)
choice_3_entry.grid(row=7, column=1)

submit_btn = Button(add_frame, text='Submit', command=add_question, width=40)
submit_btn.grid(row=8, column=0)

delete_btn = Button(add_frame, text='Delete', command=delete_question, width=40)

# Build quiz frame guts here
quiz_frame = Frame(win, width=600, height=400, bg='purple')

quiz_question_label = Label(quiz_frame, textvariable=question_text, padx=20)
quiz_question_label.grid(row=0, column=0)

quiz_point_label = Label(quiz_frame, textvariable=point_total, padx=20)
quiz_point_label.grid(row=0, column=1, sticky='e')

question_number_label = Label(quiz_frame, textvariable=question_total)
question_number_label.grid(row=1, column=1)

quiz_choice_1 = Radiobutton(quiz_frame, textvariable=choice0, variable=question_selection, value=0)
quiz_choice_1.grid(row=1, column=0)

quiz_choice_2 = Radiobutton(quiz_frame, textvariable=choice1, variable=question_selection, value=1)
quiz_choice_2.grid(row=2, column=0)

quiz_choice_3 = Radiobutton(quiz_frame, textvariable=choice2, variable=question_selection, value=2)
quiz_choice_3.grid(row=3, column=0)

quiz_choice_4 = Radiobutton(quiz_frame, textvariable=choice3, variable=question_selection, value=3)
quiz_choice_4.grid(row=4, column=0)

submit_question_btn = Button(quiz_frame, command=evaluate_question, text='Submit Question')

feedback_label = Label(quiz_frame, textvariable=feedback)

next_question_button = Button(quiz_frame, command=next_question, text='Next question')

exit_quiz_btn = Button(quiz_frame, command=exit_quiz, text='Exit quiz')

win.mainloop()
