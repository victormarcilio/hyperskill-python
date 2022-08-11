import random


class Domino:
    def __init__(self):
        self.stock = []
        self.computer = []
        self.player = []
        self.snake = []
        self.status = ""
        dealt_double = False
        while not dealt_double:
            self.shuffle_and_deal()
            dealt_double = self.try_play_highest_double()

    def shuffle_and_deal(self):
        self.stock = []
        self.computer = []
        self.player = []
        self.snake = []
        for x in range(7):
            for y in range(x, 7):
                self.stock.append([x, y])
        random.shuffle(self.stock)
        for _ in range(7):
            self.player.append(self.stock.pop())
            self.computer.append(self.stock.pop())

    def try_play_highest_double(self):
        for i in range(6, -1, -1):
            doubled_piece = [i, i]
            if doubled_piece in self.player:
                self.snake.append(doubled_piece)
                self.player.remove(doubled_piece)
                self.status = "computer"
                return True
            if doubled_piece in self.computer:
                self.snake.append(doubled_piece)
                self.computer.remove(doubled_piece)
                self.status = "player"
                return True
        return False

    def game_loop(self):
        result = self.game_result()
        while not result:
            self.print_info()
            self.print_turn()
            if self.status == "player":
                self.make_valid_move()
            else:
                self.get_computer_move()
            self.switch_turns()
            result = self.game_result()
        self.print_info()
        print(result)

    def game_result(self):
        if len(self.player) == 0:
            return "The game is over. You won!"
        if len(self.computer) == 0:
            return "The game is over. The computer won!"
        if self.draw():
            return "The game is over. It's a draw!"

    def draw(self):
        corner = self.snake[0][0]
        total = 0
        if corner == self.snake[-1][1]:
            for a, b in self.snake:
                if a == corner:
                    total += 1
                if b == corner:
                    total += 1
        return total == 8

    def print_info(self):
        print("======================================================================")
        print(f"Stock size: {len(self.stock)}")
        print(f"Computer pieces: {len(self.computer)}")
        print()
        self.print_snake()
        print()
        self.print_pieces()
        print()

    def print_snake(self):
        if len(self.snake) < 7:
            for piece in self.snake:
                print(piece, end='')
            print()
        else:
            s = self.snake
            print(f"{s[0]}{s[1]}{s[2]}...{s[-3]}{s[-2]}{s[-1]}")

    def print_pieces(self):
        print("Your pieces:")
        for i in range(len(self.player)):
            print(f"{i + 1}:{self.player[i]}")

    def print_turn(self):
        if self.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
        else:
            print("Status: Computer is about to make a move. Press Enter to continue...")

    def make_valid_move(self):
        while True:
            try:
                index = int(input())
                if index == 0:
                    self.get_piece_from_stock(self.player)
                    return
                if abs(index) > len(self.player):
                    print("Invalid input. Please try again.")
                    continue
                if self.is_valid_move(index, self.player):
                    self.play_piece(index, self.player)
                    return

                print("Illegal move. Please try again.")
            except:
                print("Invalid input. Please try again.")

    def is_valid_move(self, index, who):
        if abs(index) > len(who):
            return False
        if index < 0:
            return self.is_valid_on_left(abs(index) - 1, who)
        return self.is_valid_on_right(index - 1, who)

    def is_valid_on_left(self, index, who):
        return self.snake[0][0] in who[index]

    def is_valid_on_right(self, index, who):
        return self.snake[-1][1] in who[index]

    def play_piece(self, index, who):
        piece = who[abs(index) - 1]
        who.remove(piece)
        if index < 0:
            self.snake.insert(0, piece)
            self.adjust_left()
        else:
            self.snake.append(piece)
            self.adjust_right()

    def adjust_left(self):
        if self.snake[0][1] != self.snake[1][0]:
            self.snake[0] = [self.snake[0][1], self.snake[0][0]]

    def adjust_right(self):
        if self.snake[-1][0] != self.snake[-2][1]:
            self.snake[-1] = [self.snake[-1][1], self.snake[-1][0]]

    def ai_sorting_strategy(self):
        repetitions = {x: 0 for x in range(0, 7)}
        for a, b in self.computer:
            repetitions[a] += 1
            repetitions[b] += 1
        for a, b in self.snake:
            repetitions[a] += 1
            repetitions[b] += 1
        self.computer.sort(key=lambda x: repetitions[x[0]] + repetitions[x[1]], reverse=True)

    def get_computer_move(self):
        _ = input()
        piece_count = len(self.computer)
        self.ai_sorting_strategy()
        for index in range(1, piece_count + 1):
            if self.is_valid_move(index, self.computer):
                self.play_piece(index, self.computer)
                return
            if self.is_valid_move(-index, self.computer):
                self.play_piece(-index, self.computer)
                return
        self.get_piece_from_stock(self.computer)

    def get_piece_from_stock(self, who):
        if len(self.stock):
            who.append(self.stock.pop())

    def switch_turns(self):
        if self.status == "player":
            self.status = "computer"
        else:
            self.status = "player"


Domino().game_loop()
