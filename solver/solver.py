from solver.game_functions import five_card_draw, omaha_holdem_preprocessing, texas_holdem_preprocessing


class Solver(object):

    def process(self, line: str) -> str:
        # splitting by whitespaces into a list
        sliced_line = line.split()

        if sliced_line[0] == 'five-card-draw':
            out = five_card_draw(sliced_line[1:], sliced_line[1:])

        if sliced_line[0] == 'omaha-holdem':
            hands, combinations = omaha_holdem_preprocessing(sliced_line[1:])
            out = five_card_draw(hands, combinations)

        if sliced_line[0] == 'texas-holdem':
            hands, combinations = texas_holdem_preprocessing(sliced_line[1:])
            out = five_card_draw(hands, combinations)

        return out
