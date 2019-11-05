from collections import deque


def cache(func):
    def _cache(*args, **kwargs):
        pass
    pass

def cached_questions(func):
    def cache():
        return None
    return cache

def to_history(func):
    def history():
        current_question = func()
        previous_questions = deque([])
        previous_questions.appendleft(current_question)
        return current_question
    return history()
