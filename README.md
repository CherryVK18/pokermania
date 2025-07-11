# 🃏 PokerMania - Poker Bot Showdown

Welcome to **PokerMania**, an intelligent poker simulation and competition platform built using **Python** and **Django**. Players design their own poker-playing bots and face off against others in a Texas Hold’em-style match using the **PyPokerEngine** framework.

---

## 📁 Project Structure

```
PokerMania/
├── bots/                      # Contains sample bot strategies
│   ├── aggressive_bot.py
│   ├── cautious_bot.py
│   ├── random_bot.py
│   └── probability_based_bot.py
├── poker/                    # Django project settings
│   ├── settings.py
│   └── urls.py
├── poker_tournament/        # Django app for managing tournaments
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── utils.py
├── templates/               # HTML templates (frontend)
├── static/                  # Static assets (CSS, JS)
├── test_bots/               # Bots for testing and benchmarking
├── poker_output.txt         # Sample output of bot gameplay
├── index.html               # Guide to building bots & strategies
├── manage.py
└── requirements.txt         # Python dependencies
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Subhakanta09/POKER_GUIDE
cd POKER_GUIDE
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate (on Windows)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Django server

```bash
python manage.py runserver
```

---

## 🤖 How to Create a Poker Bot

1. Inherit from the `CountingBot` base class.
2. Override the `declare_action()` method.
3. Register your bot and simulate games using `setup_config()` and `start_poker()`.

### Example: Random Bot

```python
class RandomBot(CountingBot):
    def declare_action(self, valid_actions, hole_card, round_state):
        # Randomly selects call, raise or fold
        ...
```

---

## 🧠 Advanced Bot Strategies

* **AggressiveBot**: Always raises with max possible amount.
* **CautiousBot**: Calls if pot is small, otherwise folds.
* **GeneralPlayer**: Uses Monte Carlo simulation to estimate hand strength.
* **AggressivePlayer**: Learns from opponent's behavior to counter bluffing.

---

## 📊 Features

* Real-time bot battles using PyPokerEngine.
* Web interface for instructions and documentation.
* Extendable bot API for creating custom strategies.
* Historical data capture for replays and performance analysis.

---

## 📚 Documentation

Check out the detailed guide at [`Documentation`](./doc.html) which includes:

* How bots are built and customized.
* Sample strategies with code.
* Explanation of win rate estimation, bluffing detection, and counters.
* Visual examples of gameplay rounds.

---

## 🧑‍💻 Authors

* T. Sai Charan – [LinkedIn](https://www.linkedin.com/in/sai-charan-tarra)
---
