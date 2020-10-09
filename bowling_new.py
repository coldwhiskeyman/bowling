def get_score(game_result):
    score = 0
    if len(game_result.replace('X', '')) % 2 != 0:
        raise ValueError('Неправильная длина строки', game_result)
    for char in game_result:
        if not char.isdigit() and char != 'X' and char != '/' and char != '-':
            raise ValueError('Недопустимый символ', char)
    split_result = split_score(game_result)
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
                    score += (10 + regular_frame(next_frame))
            elif next_frame == 'X' and index == len(split_result) - 2:
                score += 20
            elif next_frame == 'X' and split_result[index + 2] == 'X':
                score += 30
            else:
                score += (20 + int(split_result[index + 2][0]))
                # начинаю понимать, почему решение через последовательные броски лучше
                # расчет на 3 броска вперед будет уже слишком сложным
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
            score += regular_frame(frame)
    return score


def regular_frame(frame):
    frame_score = 0
    for char in frame:
        if char.isdigit():
            frame_score += int(char)
    if frame_score > 9:
        raise ValueError('Счет превышает возможный', frame)
    else:
        return frame_score


def split_score(game_result):
    split_result = []
    while len(game_result) >= 2:
        if game_result[0] == 'X':
            split_result.append('X')
            game_result = game_result[1:]
        else:
            split_result.append(game_result[:2])
            game_result = game_result[2:]
    if len(game_result) == 1:
        split_result.append('X')
    return split_result


if __name__ == '__main__':
    s = 'X' * 9 + '55'
    s = 'X' * 9 + '/1'
    print(get_score(s))
