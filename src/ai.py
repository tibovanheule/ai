"""@package AI
The Ai module implements the core ai functions

More details....
"""
import NLP


def analyse_text(text):
    return str(NLP.text_precessing(text))


def validate():
    return "Hello, the ai thanks you for the lesson!"
