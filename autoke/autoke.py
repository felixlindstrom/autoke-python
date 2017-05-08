import re
import util
from collections import defaultdict


class Engine:
    def __init__(self, stop_list):
        self.stop_list = stop_list

    def get_phrases(self, text):
        """Create 'phrases' by splitting a sentence by stop-words"""
        sentences = util.get_sentences(text)
        phrases = []
        for sentence in sentences:
            phrases += self.stop_list.split(sentence)
        return phrases

    def score_words(self, phrases):
        """Score words across multiple phrases"""
        frequencies = defaultdict(float)
        degrees = defaultdict(float)
        scores = defaultdict(float)

        for phrase in phrases:
            words = util.get_words(phrase)
            for word in words:
                frequencies[word] += 1
                degrees[word] += len(words) - 1

        for word, frequency in frequencies.items():
            scores[word] = (degrees[word] + frequency) / frequency

        return dict(scores)

    def score_phrases(self, phrases):
        """Score phrases based on word-scores"""
        word_scores = self.score_words(phrases)
        scores = defaultdict(float)
        for phrase in phrases:
            for word in util.get_words(phrase):
                scores[phrase] += word_scores[word]
        return dict(scores)

    def analyse(self, text, min_score=0):
        phrases = self.get_phrases(text)
        scores = self.score_phrases(phrases)

        # Remove phrases with too low scores
        scores = dict((key, value) for key, value in scores.items() if value >= min_score)

        return scores


class StopList:
    def __init__(self, file_path=None):
        self.words = []
        self.pattern = ''
        if file_path is not None:
            self.load_file(file_path)

    def load_file(self, file_path):
        with open(file_path) as fh:
            for line in fh.readlines():
                if not line.strip():
                    continue
                self.add(line)

    def get_compiled_pattern(self):
        if len(self.words) < 1:
            raise ValueError('No words loaded')

        words = list(map(lambda word: '\\b' + word + '\\b', self.words))
        return re.compile('|'.join(words), re.IGNORECASE)

    def add(self, word):
        self.words.append(word.lower().strip())

    def has(self, word):
        return str(word).strip().lower() in self.words

    def split(self, string):
        result = re.sub(self.get_compiled_pattern(), '|', string).split('|')
        return util.clean_list(result)
