class Question:
    '''Question class with the questions: point value, question text, choices, correct answer, correct feedback,
    incorrect feedback'''

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

#     Question text formatted like this since on the list box I wanted the question text to identify the question
