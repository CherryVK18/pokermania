from pypokerengine.players import BasePokerPlayer
from typing import final


class CountingBot(BasePokerPlayer):

    def __init__(self):
        self.hole_cards_log = []

    def declare_action(self, valid_actions, hole_card, round_state):
        pass

    def receive_game_start_message(self, game_info):
        pass

    @final
    def receive_round_start_message(self, round_count, hole_card, seats):
        round_info = {"round": round_count, "hole_cards": {}}
        for player in seats:
            if player['uuid'] == self.uuid:
                round_info["hole_cards"] = hole_card
        self.hole_cards_log.append(round_info)

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
