import unittest
import os
from autoke.autoke import Engine, StopList
from autoke import util


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = Engine(StopList())
        self.engine.stop_list.load_file(os.path.dirname(os.path.realpath(__file__)) + '/data/stoplist.txt')
        self.text = "I do not think there is any thrill that can go through the human heart like that felt by the inventor as he sees some creation of the brain unfolding to success. Such emotions make a man forget food, sleep, friends, love, everything."

    def test_get_words(self):
        self.assertListEqual(
            util.get_words(self.text),
            ['i', 'do', 'not', 'think', 'there', 'is', 'any', 'thrill', 'that', 'can', 'go', 'through', 'the', 'human', 'heart', 'like', 'that', 'felt', 'by', 'the', 'inventor', 'as', 'he', 'sees', 'some', 'creation', 'of', 'the', 'brain', 'unfolding', 'to', 'success', 'such', 'emotions', 'make', 'a', 'man', 'forget', 'food', 'sleep', 'friends', 'love', 'everything']
        )

    def test_get_sentences(self):
        self.assertListEqual(
            util.get_sentences(self.text),
            ['i do not think there is any thrill that can go through the human heart like that felt by the inventor as he sees some creation of the brain unfolding to success', 'such emotions make a man forget food', 'sleep', 'friends', 'love', 'everything']
        )

    def test_get_phrases(self):
        self.assertListEqual(
            self.engine.get_phrases(self.text),
            ['think', 'thrill', 'can go', 'human heart like', 'felt', 'inventor', 'sees', 'creation', 'brain unfolding', 'success', 'emotions make', 'man forget food', 'sleep', 'friends', 'love', 'everything']
        )

    def test_score_words(self):
        phrases = self.engine.get_phrases(self.text)
        result = self.engine.score_words(phrases)

        self.assertEqual(len(result), 23)
        self.assertEqual(result['heart'], 3.0)
        self.assertEqual(result['human'], 3.0)
        self.assertEqual(result['make'], 2.0)
        self.assertEqual(result['thrill'], 1.0)

    def test_score_phrases(self):
        phrases = self.engine.get_phrases(self.text)
        result = self.engine.score_phrases(phrases)

        self.assertEqual(len(result), 16)
        self.assertIn('human heart like', result)
        self.assertEqual(result['human heart like'], 9.0)

    def test_analyse(self):
        result = self.engine.analyse(self.text, 4)

        self.assertEqual(len(result), 5)
        self.assertIn('human heart like', result)
        self.assertEqual(result['human heart like'], 9.0)
        self.assertEqual(result['can go'], 4.0)

    def test_analyse_not_found(self):
        result = self.engine.analyse(self.text, 5)

        self.assertNotIn('love', result)
        self.assertNotIn('think', result)
        self.assertNotIn('success', result)


class StopListTests(unittest.TestCase):
    def setUp(self):
        self.stop_list = StopList()

    def test_add(self):
        self.stop_list.add('test')
        self.assertTrue(self.stop_list.has('test'))

    def test_has_not(self):
        self.assertFalse(self.stop_list.has('test'))

    def test_sting_split(self):
        test_string = 'word1 word2 word3'
        self.stop_list.add('word2')
        self.assertListEqual(self.stop_list.split(test_string), ['word1', 'word3'])

    def test_load_file(self):
        self.stop_list.load_file(os.path.dirname(os.path.realpath(__file__)) + '/data/stoplist.txt')

    def test_load_invalid_file(self):
        with self.assertRaises(IOError):
            self.stop_list.load_file(os.path.dirname(os.path.realpath(__file__)) + '/data/invalid-file.txt')

    def test_compiled_no_words(self):
        with self.assertRaises(ValueError):
            self.stop_list.words = []
            self.stop_list.get_compiled_pattern()


class UtilTests(unittest.TestCase):
    def test_clean_list(self):
        test_list = ['', 'a', 'b', ' 1 ', 2]
        result = util.clean_list(test_list)

        self.assertListEqual(result, ['a', 'b', '1', '2'])


if __name__ == '__main__':
    unittest.main()