import re
import util
from collections import defaultdict


class Engine:
    """
    Keyword Extractor Engine
    
    Args:
        stop_list (StopList): StopList instance to use
    """
    def __init__(self, stop_list):
        self.stop_list = stop_list

    def get_phrases(self, text):
        """
        Extract 'phrases' from text by splitting a sentence by stop-words.
        
        Args:
            text (string): Text to extract phrases from
            
        Returns:
            dict of phrases
        """
        sentences = util.get_sentences(text)
        phrases = []
        for sentence in sentences:
            phrases += self.stop_list.split(sentence)
        return phrases

    def score_words(self, phrases):
        """
        Score words across multiple phrases
        
        Args:
            phrases (dict): Phrases to score
            
        Returns:
            dict of scored words
        """
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
        """
        Score phrases based on word-scores
        
        Args:
            phrases (dict): Phrases to score
            
        Returns:
            dict of scored phrases
        """
        word_scores = self.score_words(phrases)
        scores = defaultdict(float)
        for phrase in phrases:
            for word in util.get_words(phrase):
                scores[phrase] += word_scores[word]
        return dict(scores)

    def analyse(self, text, min_score=0):
        """
        Analyse a text, generating scored phrases
        
        Args:
             text (string): Text to analyse
             min_score (integer): Minimum score of result-items to include
             
        Returns:
            Dictionary of phrases and their scores
        """
        phrases = self.get_phrases(text)
        scores = self.score_phrases(phrases)

        # Remove phrases with too low scores
        scores = dict((key, value) for key, value in scores.items() if value >= min_score)

        return scores


class StopList:
    """
    Stop-list
    
    Args:
        file_path (string) (optional): File-path to load
    """
    def __init__(self, file_path=None):
        self.words = []
        if file_path is not None:
            self.load_file(file_path)

    def load_file(self, file_path):
        """
        Load a file of stop-list and append to the list of words
        
        Args:
            file_path (string): Path to the file to load
        """
        with open(file_path) as fh:
            for line in fh.readlines():
                if not line.strip():
                    continue
                self.add(line)

    def get_compiled_pattern(self):
        """
        Get compiled regex for the words
        
        Returns:
            retype
        """
        if len(self.words) < 1:
            raise ValueError('No words loaded')

        words = list(map(lambda word: '\\b' + word + '\\b', self.words))
        return re.compile('|'.join(words), re.IGNORECASE)

    def add(self, word):
        """
        Add a word to the list of stop-words
        
        Args:
            word (string): Word to add
        """
        self.words.append(str(word).lower().strip())

    def has(self, word):
        """
        Check if a word is included in the current instance
        
        Args:
            word (string): Word to check for
            
        Returns:
            True if word exists, otherwise False
        """
        return str(word).strip().lower() in self.words

    def split(self, string):
        """
        Split a given string by stop-words
        
        Args:
            string (string): String to split
            
        Returns:
            A list of strings
        """
        result = re.sub(self.get_compiled_pattern(), '|', string).split('|')
        return util.clean_list(result)
