import sys

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
from pypokerengine.api.game import setup_config, start_poker
import importlib.util
import json
import re
from .models import Bot, Match, TestBot


def load_bot(filepath):
    try:
        spec = importlib.util.spec_from_file_location("Bot", filepath)
        bot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot)
        if hasattr(bot, 'Bot'):
            return bot.Bot(), True
        else:
            return "The 'Bot' class is not found in the module.", False
    except Exception as e:
        return str(e), False


def parse_poker_output_to_json(input_text):
    poker_data = {
        "street": [],
        "actions": {},
        "communitycards": []
    }

    lines = input_text.strip().splitlines()
    current_street = None

    for line in lines:
        line = line.strip()
        street_match = re.match(r'Street "(.*?)" started\. \(community card = (.*?)\)', line)
        if street_match:
            current_street = street_match.group(1)
            poker_data["street"].append(current_street)
            poker_data["actions"][current_street] = {
                "name": [],
                "action": [],
                "amount": []
            }
            poker_data["communitycards"].append(eval(street_match.group(2)))
            continue

        action_match = re.match(r'"(.*?)" declared "(.*?):(\d+)"', line)
        if action_match:
            poker_data["actions"][current_street]["name"].append(action_match.group(1))
            poker_data["actions"][current_street]["action"].append(action_match.group(2))
            poker_data["actions"][current_street]["amount"].append(int(action_match.group(3)))

    return poker_data


def play_round(bot1_instance, bot2_instance, bot1_name, bot2_name, stack=10000):
    config = setup_config(max_round=1, initial_stack=stack, small_blind_amount=250)
    config.register_player(name=bot1_name, algorithm=bot1_instance)
    config.register_player(name=bot2_name, algorithm=bot2_instance)

    output_file = f"poker_output_{bot1_name}_{bot2_name}.txt"
    result, success = redirect_stdout_to_file(config, output_file)
    replay_data = read_output_file_and_parse(output_file)

    if os.path.exists(output_file):
        os.remove(output_file)

    return result, replay_data, bot1_instance.hole_cards, bot2_instance.hole_cards


def play_match(bot1_path, bot2_path, bot1, bot2, num_rounds=5):
    bot1_instance, chk1 = load_bot(bot1_path)
    bot2_instance, chk2 = load_bot(bot2_path)

    if not chk1 or not chk2:
        return None, None, None, None
    stack = 10000
    total_chips_exchanged = 0
    bot1_wins = 0
    bot2_wins = 0
    rounds_data = []
    results_stack=0;

    for round_num in range(num_rounds):
        result, replay_data, hole_cards1, hole_cards2 = play_round(
            bot1_instance, bot2_instance, bot1.name, bot2.name, stack
        )
        results_stack=result["players"][0]["stack"];
        round_chips = (result["players"][0]["stack"] - result["rule"]["initial_stack"])
        both_chips_exchanged=abs(result["players"][0]["stack"]-result["rule"]["initial_stack"])+abs(result["players"][1]["stack"]-result["rule"]["initial_stack"])
        stack = min(result["players"][0]["stack"], result["players"][1]["stack"])
        winner = ""
        if round_chips > 0:
            bot1_wins += 1
            winner = result["players"][0]["name"]
        else:
            bot2_wins += 1
            winner = result["players"][1]["name"]

        rounds_data.append({
            'round_number': round_num + 1,
            'replay_data': replay_data,
            'hole_cards': [hole_cards1, hole_cards2],
            'chips_exchanged': abs(round_chips),
            'total_chips_exchanged': both_chips_exchanged,
            'winner': winner
        })

        total_chips_exchanged += round_chips

    # Determine match winner
    winner = bot1.name if bot1_wins > bot2_wins else bot2.name

    # Update bot statistics
    update_bot_stats(bot1, bot2, winner, total_chips_exchanged, bot1_wins, num_rounds)

    return winner, abs(results_stack-10000), rounds_data, [bot1_wins, bot2_wins]


def update_bot_stats(bot1, bot2, winner, chips_exchanged, bot1_wins, num_rounds):
    chips_per_round = chips_exchanged / num_rounds
    score_per_round = 20 + 80 * chips_per_round / 10000

    if winner == bot1.name:
        bot1.chips_won += chips_exchanged
        bot2.chips_won -= chips_exchanged
        bot1.wins += 1
        bot1.score += score_per_round * bot1_wins
        bot2.score -= score_per_round * (num_rounds - bot1_wins)
    else:
        bot1.chips_won -= chips_exchanged
        bot2.chips_won += chips_exchanged
        bot2.wins += 1
        bot2.score += score_per_round * (num_rounds - bot1_wins)
        bot1.score -= score_per_round * bot1_wins

    bot1.total_games += 1
    bot2.total_games += 1
    bot1.save()
    bot2.save()


def redirect_stdout_to_file(config, output_file):
    with open(output_file, "w") as file:
        original_stdout = sys.stdout
        try:
            sys.stdout = file
            result = start_poker(config, verbose=1)
            return result, True
        except Exception as e:
            sys.stdout = original_stdout
            with open(output_file, "a") as err_file:
                err_file.write(f"\nError: {str(e)}")
            return str(e), False
        finally:
            sys.stdout = original_stdout


def read_output_file_and_parse(input_file):
    with open(input_file, "r") as file:
        content = file.read()
    return parse_poker_output_to_json(content)
