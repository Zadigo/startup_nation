"""This module regroups a list of definitions and functions useful for
operating the Startup Nation quizz within a Django environment or not.

Description
-----------

    The module is composed of x main definitions to help create
    questions for the application:
        
        - Json creator
        - Create question

    One main definition to open the questions files and retrieve
    the questions:

        - Questions

    And, finally a different set of definitions to get list of questions
    in different manners:

        - Group files
        - Randomized questions
        - N questions
        - Each N questions

author: pendenquejohn@gmail.com
"""

import secrets
import os
import json
from django.conf import settings
from random import shuffle, sample, choice


try:
    if settings.MEDIA_ROOT:
        QUESTIONS_ROOT = os.path.join(settings.MEDIA_ROOT, 'questions')
except:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    QUESTIONS_ROOT = os.path.join(BASE_DIR, 'data')


def set_request(request, questions_list):
    """Sets the questions in the user session"""
    request.session['user_session_questions'] = questions_list
    return request

def json_creator(subject, outputfile_name, tag=None, write_to_file=False):
    """A helper function for creating a JSON files containing
    a set of questions
    """
    questions = []
    text_file = os.path.join(QUESTIONS_ROOT, 'test.txt')
    output_path = os.path.join(QUESTIONS_ROOT, outputfile_name + '.json')
    if not tag:
        tag = subject.replace(' ', '-')
    with open(text_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for i, question in enumerate(data):
            reference = secrets.token_hex(nbytes=8)
            base = {
                'id': i + 1,
                "reference": reference,
                "subject": subject,
                "question": question.strip(),
                "illustration": "",
                "answers": [],
                "tag": tag
            }
            questions.append(base)

        if write_to_file:
            with open(output_path, 'w', encoding='utf-8') as p:
                data = {'questions': questions}
                json.dump(data, p, indent=4)
    return questions

def create_question(file_name, subject, question, answers:list, answered=False):
    tag = subject.replace(' ', '-')
    if not file_name.endswith('.json'):
        file_name = file_name + '.json'
    path = os.path.join(QUESTIONS_ROOT, file_name)
    for answer in answers:
        if not isinstance(answer, dict):
            raise TypeError('%s should a dictionnary' % answer)
    with open(path, 'r+', encoding='utf-8') as f:
        data = json.load(f)['questions']
        if data:
            last_question_id = data[-1]['id']
        else:
            last_question_id = 1

        question_base = {
                'id': last_question_id + 1,
                'reference': secrets.token_hex(nbytes=6),
                'subject': subject,
                'question': question.strip(),
                'answers': [],
                'tag': tag
            }
        data.append(question_base)
        base = {
            'questions': data
        }
        json.dump(base, f, indent=4)
    return data


# QUERY

def questions(file_name, limit:int=0):
    """Returns the questions from a question file"""
    if isinstance(file_name, list):
        raise TypeError('This definition only accepts a file name as string: %s' % file_name)
    
    # Allows for greater flexibility
    if not file_name.endswith('.json'):
        file_name = file_name + '.json'

    path = os.path.join(QUESTIONS_ROOT, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data['questions'] if limit == 0 else data['questions'][:limit]

def get_question(file_name, reference_or_id):
    """Get a specific question from the list"""
    for question in questions(file_name):
        if question['reference'] == reference_or_id:
            matched_question = question
            break
    return matched_question or {}

def get_question_answers(file_name, reference_or_id):
    """Return the answers of a given question"""
    return get_question(file_name, reference_or_id)['answers']

def group_files(file_names:list):
    """Groups a set of question files together into a list
    and shuffles the list in place
    """
    questions_list = []
    for file_name in file_names:
        questions_list = questions_list + questions(file_name)
    shuffle(questions_list)
    for i, question in enumerate(questions_list):
        question['id'] = i + 1
    return questions_list


# DECOTATORS

# def reindex(items:list):
#     """Reindexes questions or answers when they have been shuffled"""
#     return [item.update({'id': index}) for index, item in enumerate(items)]

def randomizer(func):
    """A decorator that shuffles a list in place"""
    def create(file_name):
        # Func should a definition that
        # opens the files and returns the
        # JSON data from it
        questions_list = func(file_name)
        shuffle(questions_list)
        return questions_list
    return create

def population(func):
    """A decorator that return k sample questions from a list"""
    def choose(k, file_names:list):
        questions_list = func(file_names)
        return sample(questions_list, k)
    return choose

def shuffle_answers(func):
    """A decorator that takes a list of questions, shuffles the
    answers wuthin each question, reindexes them and returns
    the questions
    """
    def create_shuffle(file_name):
        questions = func(file_name)
        for question in questions:
            answers = question['answers']

            shuffle(answers)

            for index, answer in enumerate(answers):
                answer['id'] = index + 1
        return questions
    return create_shuffle


# ALGORITHMS

@randomizer
def randomized_questions(file_name):
    """Returns the questions after shuffling them in place"""
    return questions(file_name)

@population
def nquestions(file_names:list):
    """Return n amount of questions from a list"""
    questions = group_files(file_names)
    return questions

def random_question(questions_list:list):
    """Returrns a random question from a list of questions"""
    return choice(questions_list)

def each_n_questions(file_names:list, n=1):
    """Gets each files and return n amount of questions from each of them"""
    final_questions = []
    for file_name in file_names:
        data = questions(file_name)
        if data:
            shuffle(data)
            n_questions = sample(data, n)
            final_questions = final_questions + n_questions
    return final_questions

def n_percent(file_names:list, pcts:list):
    """Returns a certain percentage of questions base on the percentages
    that were provided as list
    """
    if len(file_names) != len(pcts):
        return []
    questions_list = []

    # Let's make sure that the percentage
    # provided is not below 10% and not
    # above 100%.
    # The 10% mark is to make sure that we
    # at least get one question.
    for pct in pcts:
        if pct < 10 or pct > 100:
            raise TypeError()

    for index, file_name in enumerate(file_names):
        data = questions(file_name)
        number_of_questions = len(data)
        if number_of_questions > 0:
            # This part gets the number of questions to get from
            # each file based on the percentage that was provided
            # .. 10 questions * (10% / 100) = 1 question
            k = round(number_of_questions * (pcts[index] / 100))
            sample_questions = sample(data, k)
            questions_list = questions_list + sample_questions
        else:
            questions_list = []
    shuffle(questions_list)
    return questions_list

def questions_by_theme(files_names:list, theme, strict=False, limit=0):
    """Returns a set of questions based on a predefined theme"""
    questions_list = []
    questions = group_files(files_names)
    for question in questions:
        if not strict:
            if theme in question['tag']:
                questions_list.append(question)
        else:
            pass
    shuffle(questions_list)
    
    if limit > 0:
        questions_list = questions_list[:limit]
    return questions_list
