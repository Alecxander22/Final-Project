import json
from questions import *
# The file handler module is supposed to get a list of question objects, and then break that list down into
# a dictionary within a dictionary, or turn the inner dictionary into a question object to be appended
# to a list and returned


def save_questions(question_list):
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
    return_question_list = list()
    with open('questions.JSON', 'r') as fp:
        question_load = json.load(fp)
        for question_load in question_load.values():
            temp_question = Question(point_value=question_load['Point Value'],
                                     question_text=question_load['Question Text'],
                                     correct_feedback=question_load['Correct Feedback'],
                                     incorrect_feedback=question_load['Incorrect Feedback'],
                                     correct_choice=question_load['Correct Choice'], choices=question_load['Choices'])
            return_question_list.append(temp_question)
    return return_question_list


if __name__ == "__main__":
    question1 = Question(point_value=2, question_text='Who is the main character of ATLA?',
                         correct_feedback='Yes, you clearly know your pop culture',
                         incorrect_feedback='Watch the show. Thank me later',
                         choices=['Sokka', 'Katara', 'Zuko', 'Aang'], correct_choice='Aang')

    question2 = Question(point_value=2, question_text="Who is Rey's Grandpa?",
                         correct_feedback='Indeed, the force is strong with this one',
                         incorrect_feedback='Not quite.',
                         choices=['Palpatine', 'Anakin', 'Han Solo', 'Chewbacca'], correct_choice='Palpatine')
    this_list = list()
    this_list.append(question1)
    this_list.append(question2)

    save_questions(this_list)

    q_list = retrieve_questions()

    for question in q_list:
        print(question.question_text)
