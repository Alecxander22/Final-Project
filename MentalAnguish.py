# Alecxander Butler CIS 345 T/Th 12:00 Mental Anguish
from tkinter import *
from random import sample
import json
from difflib import get_close_matches
from tkinter import messagebox


class Question:
    """Question class with the questions: point value, question text, choices, correct answer, correct feedback,
    incorrect feedback"""

    def __init__(self, point_value=0, question_text='', choices=None, correct_feedback='',
                 incorrect_feedback='', correct_choice=''):
        self.point_value = point_value
        self.question_text = question_text
        self.correct_feedback = correct_feedback
        self.incorrect_feedback = incorrect_feedback
        self.correct_choice = correct_choice
        if choices is None:
            self.choices = list()
        else:
            self.choices = choices

    @property
    def point_value(self):
        return self.__point_value

    @point_value.setter
    def point_value(self, new_value):
        if isinstance(new_value, int) and new_value >= 1:
            self.__point_value = new_value
        else:
            self.__point_value = 1

    @property
    def question_text(self):
        return self.__question_text

    @question_text.setter
    def question_text(self, new_question):
        if len(new_question) > 5:
            self.__question_text = new_question
        else:
            self.__question_text = 'Question text'

    @property
    def correct_feedback(self):
        return self.__correct_feedback

    @correct_feedback.setter
    def correct_feedback(self, new_c_feedback):
        if len(new_c_feedback) > 5:
            self.__correct_feedback = new_c_feedback
        else:
            self.__correct_feedback = 'Correct!'

    @property
    def incorrect_feedback(self):
        return self.__incorrect_feedback

    @incorrect_feedback.setter
    def incorrect_feedback(self, new_i_feedback):
        if len(new_i_feedback) > 5:
            self.__incorrect_feedback = new_i_feedback
        else:
            self.__incorrect_feedback = 'Incorrect!'

    @property
    def correct_choice(self):
        return self.__correct_choice

    @correct_choice.setter
    def correct_choice(self, new_choice):
        if len(new_choice) > 2:
            self.__correct_choice = new_choice
        else:
            self.__correct_choice = 'Correct choice'

    @property
    def choices(self):
        return self.__choices

    @choices.setter
    def choices(self, new_choices):
        self.__choices = new_choices

    def __str__(self):
        return f'{self.question_text}'


class BlankEntryError(Exception):
    def __init__(self, msg):
        self.msg = msg


class PointValueError(Exception):
    def __init__(self, msg):
        self.msg = msg


def save_questions(question_list):
    """Takes a list of question objects and then gets the values of the variables to
    store into a dictionary, which is them saved to a JSON file using dump"""

    question_dict = dict()
    question_number = 0

    for question_object in question_list:
        question_number += 1
        question_dict[question_number] = dict()
        question_dict[question_number]['Point Value'] = question_object.point_value
        question_dict[question_number]['Question Text'] = question_object.question_text
        question_dict[question_number]['Correct Feedback'] = question_object.correct_feedback
        question_dict[question_number]['Incorrect Feedback'] = question_object.incorrect_feedback
        question_dict[question_number]['Correct Choice'] = question_object.correct_choice
        question_dict[question_number]['Choices'] = question_object.choices

    with open('questions.json', 'w') as fp:
        json.dump(question_dict, fp)


def retrieve_questions():
    """Turns the inner dictionary from the JSON file into a question object, appends to a question list,
    and returns that list"""

    return_question_list = list()
    with open('questions.JSON', 'r') as fp:
        question_load = json.load(fp)
        for question_load in question_load.values():
            temp_question = Question(point_value=question_load['Point Value'],
                                     question_text=question_load['Question Text'],
                                     correct_feedback=question_load['Correct Feedback'],
                                     incorrect_feedback=question_load['Incorrect Feedback'],
                                     correct_choice=question_load['Correct Choice'],
                                     choices=question_load['Choices'])
            return_question_list.append(temp_question)
    return return_question_list


def edit_question(event):
    """Fills the entry widgets with the selected questions information, saves the index of the question you
    are editing and sets the edit mode to True so that the add_question function deletes the appropriate
    old question, and sets the new question in its place"""
    global win, question_text, point_value, correct_feedback, incorrect_feedback, \
        correct_choice, choice1, choice2, choice3, list_box, edit_menu, edit_mode, \
        edit_index, edit_ques, delete_btn

    add_frame.pack()

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
    """Takes out the question from the question list, deletes from the listbox
    and then saves the question list"""

    global list_box, question_list, edit_index

    edit_index = list_box.curselection()[0]
    question_list.pop(edit_index)
    list_box.delete(edit_index)
    save_questions(question_list)

    clear_text_variables()


def start_quiz():
    """Forgets the question management frame and packs the quiz frame / exit_quiz_button,
    gets a sample of 3 random, non-repeating questions from the question list and
    turns the list into an iterable, calls the next question function to populate the quiz"""

    global question_text, question_list, quiz_questions, quiz_question
    list_box.forget()
    add_frame.forget()
    list_label.forget()
    win.geometry('600x300')
    quiz_frame.pack(fill='both', padx=5, pady=5)
    quiz_frame.pack_propagate(0)
    exit_quiz_btn.grid(row=7, column=0)
    quiz_questions = sample(question_list, 3)
    quiz_questions = iter(quiz_questions)
    next_question_button.grid(row=7, column=1)
    next_question()


def evaluate_question():
    """Gets the index number of the correct question, and evaluates that against the value
    of the radio button which has been set to mimic index numbers (0, 1, 2, 3).
    If the correct number index and value of the correct radio button match up, sets
    feedback to correct, else incorrect. Stops gridding the next question button
    after 3 questions to prevent the user from clicking next question when there are no more questions"""

    global question_selection, question_list, feedback, point_total, question_total, next_question_button,\
        quiz_question, submit_question_btn, quiz_question, feedback_label, randomized_choices

    correct_question_index = 10
    '''10 is an arbitrary number, chosen because it is unattainable, 0 is a valid value 
    already and this variable needs to be set in outer scope'''
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

    out_of_points.set(out_of_points.get()+quiz_question.point_value)
    feedback_label.grid(row=6, column=3)
    submit_question_btn['state'] = 'disabled'

    if question_total.get() != 3:
        next_question_button.grid(row=7, column=3)


def exit_quiz():
    """Reverts the totals to 0, and forgets the quiz frame, brings back the question management
    frame / widgets"""
    list_label.pack()
    list_box.pack()
    add_frame.pack()
    quiz_frame.forget()
    search_question_frame.forget()
    win.geometry(win_size)

    question_total.set(value=0)
    point_total.set(value=0)
    clear_text_variables()


def next_question():
    """Brings up the next question and sets the text varaibles to its values, randomizes the
    order of the question choices"""
    global quiz_question, quiz_questions, next_question_button, randomized_choices

    quiz_question = next(quiz_questions)

    next_question_button.grid_forget()
    feedback_label.grid_forget()
    submit_question_btn.grid(row=5, column=0)
    submit_question_btn['state'] = 'normal'
    question_total.set(value=question_total.get() + 1)

    question_text.set(quiz_question.question_text)
    point_value.set(quiz_question.point_value)
    randomized_choices = sample(quiz_question.choices, 4)
    choice0.set(randomized_choices[0])
    choice1.set(randomized_choices[1])
    choice2.set(randomized_choices[2])
    choice3.set(randomized_choices[3])


def add_question():
    """Creates a new form underneath the list for the user to fill in, and submit,
    the submit process actually happens in the next method, this is to "open" the form
    and gather the data"""
    global point_value, correct_feedback, incorrect_feedback, \
        correct_choice, choice1, choice2, choice3, question_list, \
        add_frame, question_text, edit_index, edit_mode
    try:

        if (len(correct_choice.get()) == 0 or len(choice1.get()) == 0 or len(choice2.get()) == 0 or
                len(choice3.get()) == 0 or len(question_text.get()) == 0
                or len(correct_feedback.get()) == 0 or len(incorrect_feedback.get()) == 0):
            raise BlankEntryError('There is an unfilled field, please fill all the fields before submitting')

        if point_value.get() > 3 or point_value.get() < 1:
            raise PointValueError('Only point values between 1 and 3 are acceptable')

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
    except BlankEntryError as excp:
        messagebox.showinfo('Blank Entry', excp)
    except ValueError:
        messagebox.showinfo('Error', 'Please enter the points field as a digit between 1 and 3, i.e. "2"')
    except PointValueError as excp:
        messagebox.showinfo('Invalid point value', excp)
    except TclError:
        messagebox.showinfo('blank entry', 'Please enter a value between 1 and 3  as an integer'
                                           '(i.e. "3") for the point value')


def clear_text_variables():
    """Clears the values of the text variables"""
    question_text.set('')
    point_value.set(0)
    correct_feedback.set('')
    incorrect_feedback.set('')
    correct_choice.set('')
    choice0.set('')
    choice1.set('')
    choice2.set('')
    choice3.set('')


def pack_search_question():
    list_box.forget()
    add_frame.forget()
    list_label.forget()
    search_question_frame.pack(ipadx='60', ipady='50', anchor=N)
    search_question_frame.pack_propagate(0)


def search_question():
    """Retrieves search parameter from search_text variable and compares it to list of question text"""
    search_parameter = search_text.get()
    question_text_list = list()
    close_matches_list_box.delete(0, 'end')
    for question in question_list:
        question_text_list.append(question.question_text)
    close_matches = get_close_matches(search_parameter, question_text_list, cutoff=.4)
    for close_match in close_matches:
        close_matches_list_box.insert(END, close_match)


def pack_add_frame():
    clear_text_variables()
    add_frame.pack(pady=5)
    add_frame.pack_propagate(0)


def forget_add_frame():
    add_frame.forget()


win = Tk()
win_size = '750x625'
win.geometry(win_size)
win.iconbitmap('MentalAnguishIcon.ico')

question_text = StringVar()
point_value = IntVar()
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
search_text = StringVar()
out_of_points = IntVar()
out_of_questions = StringVar(value='/3')

edit_question_color = 'PeachPuff'


edit_index = 0
edit_ques = None
edit_mode = False

menu_bar = Menu(win)
win.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=False)
edit_menu = Menu(menu_bar, tearoff=False)

menu_bar.add_command(label='Take a Quiz', command=start_quiz)
menu_bar.add_command(label='Search for a question', command=pack_search_question)
menu_bar.add_command(label='Add a question', command=pack_add_frame)

list_label = Label(win, text='Double click to edit a question')
list_label.pack()

list_box = Listbox(win, width=80, height=20)
list_box.pack()
list_box.bind('<Double-Button-1>', edit_question)
question_list = retrieve_questions()
for question in question_list:
    list_box.insert(END, question)

add_frame = Frame(win, width=300, height=150, borderwidth=5, bg=edit_question_color, relief='raised')

text_lbl = Label(add_frame, text='Question text:', bg=edit_question_color)
text_lbl.grid(row=0, column=0, sticky='w')

text_entry = Entry(add_frame, textvariable=question_text, width=50)
text_entry.grid(row=0, column=1, sticky='e')

point_lbl = Label(add_frame, text='Point value: ', bg=edit_question_color)
point_lbl.grid(row=1, column=0, sticky='w')

point_entry = Entry(add_frame, textvariable=point_value, width=10)
point_entry.grid(row=1, column=1, sticky='e')

cor_fb_lbl = Label(add_frame, text='Correct feedback: ', bg=edit_question_color)
cor_fb_lbl.grid(row=2, column=0, sticky='w')

cor_fb_entry = Entry(add_frame, textvariable=correct_feedback, width=40)
cor_fb_entry.grid(row=2, column=1, sticky='e')

incor_fb_lbl = Label(add_frame, text='Incorrect feedback:', bg=edit_question_color)
incor_fb_lbl.grid(row=3, column=0, sticky='w')

incor_fb_entry = Entry(add_frame, textvariable=incorrect_feedback, width=40)
incor_fb_entry.grid(row=3, column=1, sticky='e')

cor_choice_lbl = Label(add_frame, text='Correct answer:', bg=edit_question_color)
cor_choice_lbl.grid(row=4, column=0, sticky='w')

cor_choice_entry = Entry(add_frame, textvariable=correct_choice, width=40)
cor_choice_entry.grid(row=4, column=1, sticky='e')

choice_1_lbl = Label(add_frame, text='Incorrect answer:', bg=edit_question_color)
choice_1_lbl.grid(row=5, column=0, sticky='w')

choice_1_entry = Entry(add_frame, textvariable=choice1, width=40)
choice_1_entry.grid(row=5, column=1, sticky='e')

choice_2_lbl = Label(add_frame, text='Incorrect answer:', bg=edit_question_color)
choice_2_lbl.grid(row=6, column=0, sticky='w')

choice_2_entry = Entry(add_frame, textvariable=choice2, width=40)
choice_2_entry.grid(row=6, column=1, sticky='e')

choice_3_lbl = Label(add_frame, text='Incorrect answer:', bg=edit_question_color)
choice_3_lbl.grid(row=7, column=0, sticky='w')

choice_3_entry = Entry(add_frame, textvariable=choice3, width=40)
choice_3_entry.grid(row=7, column=1, sticky='e')

submit_btn = Button(add_frame, text='Submit', command=add_question, width=30)
submit_btn.grid(row=8, column=0)

return_btn = Button(add_frame, text='Return', command=forget_add_frame, width=30)
return_btn.grid(row=9, column=0)

delete_btn = Button(add_frame, text='Delete', command=delete_question, width=40)

quiz_frame = Frame(win, width=600, height=600, bg='Azure', relief='raised', borderwidth=3)

quiz_question_label = Label(quiz_frame, textvariable=question_text, bg='Azure', justify='left')
quiz_question_label.grid(row=0, column=0, sticky='w')

quiz_point_label = Label(quiz_frame, textvariable=point_total, bg='Azure', justify='right')
quiz_point_label.grid(row=0, column=1, sticky='w')

out_of_lbl = Label(quiz_frame, text='Points out of', bg='azure')
out_of_lbl.grid(row=0, column=2)

out_of_point_lbl = Label(quiz_frame, textvariable=out_of_points, justify='left', bg='azure')
out_of_point_lbl.grid(row=0, column=3, sticky='w')

question_number_label = Label(quiz_frame, textvariable=question_total, bg='Azure', justify='right')
question_number_label.grid(row=1, column=1, sticky='w')

out_of_question_lbl = Label(quiz_frame, textvariable=out_of_questions, bg='azure', justify='left')
out_of_question_lbl.grid(row=1, column=2, sticky='w')

quiz_choice_1 = Radiobutton(quiz_frame, textvariable=choice0, variable=question_selection, value=0, bg='Azure')
quiz_choice_1.grid(row=1, column=0, sticky='w')

quiz_choice_2 = Radiobutton(quiz_frame, textvariable=choice1, variable=question_selection, value=1, bg='Azure')
quiz_choice_2.grid(row=2, column=0, sticky='w')

quiz_choice_3 = Radiobutton(quiz_frame, textvariable=choice2, variable=question_selection, value=2, bg='Azure')
quiz_choice_3.grid(row=3, column=0, sticky='w')

quiz_choice_4 = Radiobutton(quiz_frame, textvariable=choice3, variable=question_selection, value=3, bg='Azure')
quiz_choice_4.grid(row=4, column=0, sticky='w')

submit_question_btn = Button(quiz_frame, command=evaluate_question, text='Submit Question')

feedback_label = Label(quiz_frame, textvariable=feedback, bg='Azure')

next_question_button = Button(quiz_frame, command=next_question, text='Next question')

exit_quiz_btn = Button(quiz_frame, command=exit_quiz, text='Exit quiz')

search_question_frame = Frame(win, background='PeachPuff', width=300, height=400, borderwidth=5, relief='raised')

search_question_btn = Button(search_question_frame, text='Search questions', command=search_question, width=23)
search_question_btn.grid(row=0, column=0, sticky='w')

search_question_entry = Entry(search_question_frame, textvariable=search_text, width='60')
search_question_entry.grid(row=0, column=1)

exit_search_btn = Button(search_question_frame, command=exit_quiz, text='Back to question management')
exit_search_btn.grid(row=1, column=0)

close_matches_list_box = Listbox(search_question_frame, width=40, height=20)
close_matches_list_box.grid(row=2, column=0, columnspan=2)

win.mainloop()
