import unittest
import random
import tempfile
import os.path

from bowling import Bowling, BowlingNew
from tournament_parser import TournamentParser


class BowlingTests(unittest.TestCase):
    def test_returns_score(self):
        bowl_engine = Bowling('X4/34-4')
        score = bowl_engine.get_score()
        self.assertEqual(score, 46)

    def test_split(self):
        bowl_engine = Bowling('X4/34-4')
        result = bowl_engine.split_score()
        self.assertEqual(result, ['X', '4/', '34', '-4'])

    def test_strike(self):
        bowl_engine = Bowling('X')
        score = bowl_engine.get_score()
        self.assertEqual(score, 20)

    def test_spare(self):
        digit = str(random.randint(1, 9))
        bowl_engine = Bowling(digit + '/')
        score = bowl_engine.get_score()
        self.assertEqual(score, 15)

    def test_two_hits(self):
        bowl_engine = Bowling('34')
        score = bowl_engine.get_score()
        self.assertEqual(score, 7)

    def test_one_miss(self):
        bowl_engine = Bowling('-4')
        score = bowl_engine.get_score()
        self.assertEqual(score, 4)

    def test_two_miss(self):
        bowl_engine = Bowling('--')
        score = bowl_engine.get_score()
        self.assertEqual(score, 0)

    def test_length(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('X234')
            bowl_engine.get_score()

    def test_wrong_char(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('X23W4')
            bowl_engine.get_score()

    def test_misplaced_slash(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('X23/4')
            bowl_engine.get_score()

    def test_max_score(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('77')
            bowl_engine.get_score()


class BowlingNewTests(unittest.TestCase):
    def test_returns_score(self):
        bowl_engine = BowlingNew('XX4/34-4X')
        score = bowl_engine.get_score()
        self.assertEqual(score, 78)

    def test_split(self):
        bowl_engine = BowlingNew('X4/34-4')
        result = bowl_engine.split_score()
        self.assertEqual(result, ['X', '4/', '34', '-4'])

    def test_strike(self):
        bowl_engine = BowlingNew('X')
        score = bowl_engine.get_score()
        self.assertEqual(score, 10)

    def test_strike_and_regular(self):
        bowl_engine = BowlingNew('X34')
        score = bowl_engine.get_score()
        self.assertEqual(score, 24)

    def test_three_strikes(self):
        bowl_engine = BowlingNew('XXX')
        score = bowl_engine.get_score()
        self.assertEqual(score, 60)

    def test_spare(self):
        digit = str(random.randint(1, 9))
        bowl_engine = BowlingNew(digit + '/')
        score = bowl_engine.get_score()
        self.assertEqual(score, 10)

    def test_spare_and_strike(self):
        bowl_engine = BowlingNew('4/X')
        score = bowl_engine.get_score()
        self.assertEqual(score, 30)

    def test_spare_and_regular(self):
        bowl_engine = BowlingNew('4/34')
        score = bowl_engine.get_score()
        self.assertEqual(score, 20)

    def test_two_hits(self):
        bowl_engine = BowlingNew('34')
        score = bowl_engine.get_score()
        self.assertEqual(score, 7)

    def test_one_miss(self):
        bowl_engine = BowlingNew('-4')
        score = bowl_engine.get_score()
        self.assertEqual(score, 4)

    def test_two_miss(self):
        bowl_engine = BowlingNew('--')
        score = bowl_engine.get_score()
        self.assertEqual(score, 0)

    def test_length(self):
        with self.assertRaises(ValueError):
            bowl_engine = BowlingNew('X234')
            bowl_engine.get_score()

    def test_wrong_char(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('X23W4')
            bowl_engine.get_score()

    def test_misplaced_slash(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('X23/4')
            bowl_engine.get_score()

    def test_max_score(self):
        with self.assertRaises(ValueError):
            bowl_engine = Bowling('77')
            bowl_engine.get_score()


class ParserTests(unittest.TestCase):
    tmpfilepath = os.path.join(tempfile.gettempdir(), 'tmp-tournament.txt')

    def setUp(self):
        with open(self.tmpfilepath, 'w', encoding='utf8') as file:
            file.write('### Tour 1\n')
            file.write('Алексей 35612/----2/8-6/3/4/\n')
            file.write('Татьяна 62334/6/4/44X361/X\n')
            file.write('Давид   --8/--8/4/8/-224----\n')
            file.write('Павел   ----15623113-95/7/26\n')
            file.write('Роман   7/428/--4-533/34811/\n')
            file.write('winner is .........\n')

    def test_collect_names(self):
        names = ['Алексей', 'Татьяна', 'Давид', 'Павел', 'Роман']
        parser = TournamentParser(self.tmpfilepath, 'x.txt')
        parser.read_file()
        self.assertEqual(names, list(parser.stats.keys()))

    def test_parse_line(self):
        parser = TournamentParser(self.tmpfilepath, 'x.txt')
        name, score = parser.parse_line('Алексей 35612/----2/8-6/3/4/')
        self.assertEqual(name, 'Алексей')
        self.assertEqual(score, 98)

    def test_calc_winner(self):
        parser = TournamentParser(self.tmpfilepath, 'x.txt')
        parser.stats['Алексей'] = 40
        parser.stats['Татьяна'] = 50
        parser.stats['Давид'] = 30
        winner = parser.get_winner()
        self.assertEqual(winner, 'Татьяна')

    def test_win_count(self):
        parser = TournamentParser(self.tmpfilepath, 'x.txt')
        parser.stats['Алексей'] = 40
        parser.stats['Татьяна'] = 50
        parser.stats['Давид'] = 30
        winner = parser.get_winner()
        self.assertEqual(parser.winners['Татьяна'], 1)


if __name__ == '__main__':
    unittest.main()
