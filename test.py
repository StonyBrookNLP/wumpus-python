from nltk import tokenize
from wumpus import wumpus as wp
from utils import string_utils

__author__ = 'chetannaik'


def filter_sentences(str_list, filter_list=None):
    filtered_sentences = []
    for string in str_list:
        sent_list = tokenize.sent_tokenize(string)
        for sentence in sent_list:
            tokens = tokenize.word_tokenize(sentence)
            if string_utils.is_valid_sentence(sentence, tokens):
                if filter_list:
                    if any(fltr_wrd in sentence for fltr_wrd in filter_list):
                        filtered_sentences.append(sentence)
                else:
                    filtered_sentences.append(sentence)
    return filtered_sentences


def main():
    wumpus = wp.Wumpus()
    wumpus.connect()

    wumpus_query = """(("Giraffe^neck")<[20])"""
    count = 500
    context = 20
    filter_list = ["giraffe", "long", "neck"]

    gcl_query = "@gcl[{}] {}".format(count, wumpus_query)
    print "\n> WUMPUS QUERY:\n\t{}".format(gcl_query)
    sentences = wumpus.query(gcl_query, context)
    print "\n> LIST OF SENTENCES FROM WUMPUS:"
    for sentence in sentences:
        print "\t {}".format(sentence)
    print "\n"
    wumpus.disconnect()

    filterd_sentences = filter_sentences(sentences, filter_list)
    print "\n> LIST OF FILTERED SENTENCES:"
    for sentence in filterd_sentences:
        print "\t {}".format(sentence)


if __name__ == '__main__':
    main()
