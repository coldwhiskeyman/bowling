from collections import defaultdict

from bowling import Bowling, BowlingNew


class TournamentParser:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.stats = {}
        self.game_count = defaultdict(int)
        self.winners = defaultdict(int)

    def read_file(self):
        with open(self.input_file, encoding='utf8') as file, open(self.output_file, 'w') as output:
            for line in file:
                if line.startswith('###'):
                    self.stats = {}
                    output.write(line)
                elif line == '\n':
                    output.write('\n')
                elif line.startswith('winner'):
                    winner = self.get_winner()
                    if not winner:
                        output.write('Все дисквалифицированы\n')  # в исходном файле очень много невалидных строк...
                    else:
                        output.write('winner is ' + winner + '\n')
                else:
                    try:
                        name, score = self.parse_line(line)
                        self.stats[name] = score
                        output.write(f'{line.rstrip():<32}' + str(score) + '\n')
                    except ValueError as err:
                        output.write(f'{line.rstrip():<32}' + str(err) + '\n')

    def parse_line(self, line):
        name, game_result = line.split()
        self.game_count[name] += 1
        bowl_engine = Bowling(game_result)
        score = bowl_engine.get_score()
        return name, score

    def get_winner(self):
        if not self.stats:
            return None

        name, _ = max(self.stats.items(), key=lambda x: x[1])
        self.winners[name] += 1
        return name

    def print_table(self):
        print('+----------+------------------+--------------+')
        print('| Игрок    |  сыграно матчей  |  всего побед |')
        print('+----------+------------------+--------------+')
        for name, wins in sorted(self.winners.items(), key=lambda x: x[1], reverse=True):
            games = self.game_count[name]
            print(f'| {name:<9}|{games:^18}|{wins:^14}|')
        print('+----------+------------------+--------------+')


class TournamentParserNew(TournamentParser):
    def parse_line(self, line):
        name, game_result = line.split()
        self.game_count[name] += 1
        bowl_engine = BowlingNew(game_result)
        score = bowl_engine.get_score()
        return name, score


if __name__ == '__main__':
    tp = TournamentParser('tournament.txt', 'out.txt')
    tp.read_file()
    tp.print_table()

    tp2 = TournamentParserNew('tournament.txt', 'out2.txt')
    tp2.read_file()
    tp2.print_table()
