class Bowling:
    def __init__(self, game_result):
        self.game_result = game_result

    def get_score(self):
        score = 0
        self.check_errors_in_raw_string()
        split_result = self.split_score()
        for frame in split_result:
            if frame == 'X':
                score += 20
            elif '/' in frame:
                if frame[0] == '/':
                    raise ValueError('Неверное написание', frame)
                score += 15
            else:
                score += self.regular_frame(frame)
        return score

    def split_score(self):
        split_result = []
        to_split = self.game_result
        while len(to_split) >= 2:
            if to_split[0] == 'X':
                split_result.append('X')
                to_split = to_split[1:]
            else:
                split_result.append(to_split[:2])
                to_split = to_split[2:]
        if len(to_split) == 1:
            split_result.append('X')
        return split_result

    def regular_frame(self, frame):
        frame_score = 0
        for char in frame:
            if char.isdigit():
                frame_score += int(char)
        if frame_score > 9:
            raise ValueError('Счет превышает возможный', frame)
        else:
            return frame_score

    def check_errors_in_raw_string(self):
        if len(self.game_result.replace('X', '')) % 2 != 0:
            raise ValueError('Неправильная длина строки', self.game_result)
        for char in self.game_result:
            if not char.isdigit() and char != 'X' and char != '/' and char != '-':
                raise ValueError('Недопустимый символ', char)


class BowlingNew(Bowling):
    def get_score(self):
        score = 0
        self.check_errors_in_raw_string()
        split_result = self.split_score()
        for index, frame in enumerate(split_result):
            if frame == 'X':
                if index == len(split_result) - 1:
                    score += 10
                    continue
                next_frame = split_result[index + 1]
                if next_frame != 'X':
                    if '/' in next_frame:
                        score += 20
                    else:
                        score += (10 + self.regular_frame(next_frame))
                elif next_frame == 'X' and index == len(split_result) - 2:
                    score += 20
                elif next_frame == 'X' and split_result[index + 2] == 'X':
                    score += 30
                else:
                    score += (20 + int(split_result[index + 2][0]))
            elif '/' in frame:
                if frame[0] == '/':
                    raise ValueError('Неверное написание', frame)
                if index == len(split_result) - 1:
                    score += 10
                else:
                    next_frame = split_result[index + 1]
                    if next_frame == 'X':
                        score += 20
                    elif next_frame[0] == '-':
                        score += 10
                    else:
                        score += (10 + int(next_frame[0]))
            else:
                score += self.regular_frame(frame)
        return score
