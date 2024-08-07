from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

tot = 1000
key = {"Steal": 1, "Split": 0}

def random_choice(ds):
    return random.choice([0, 1])

def always_split(ds):
    return 0

def always_steal(ds):
    return 1

def tit_for_tat(ds):
    if ds:
        return 1 if ds[-1] == 1 else 0
    return 0

def opposite_tit_for_tat(ds):
    if ds:
        return 0 if ds[-1] == 1 else 1
    return 1

strategies = {
    "Tit for Tat": tit_for_tat,
    "Opposite Tit for Tat": opposite_tit_for_tat,
    "Always Split": always_split,
    "Always Steal": always_steal,
    "Random": random_choice
}

def game(choice1, choice2):
    if choice1 == 0 and choice2 == 0:
        return tot // 2, tot // 2
    elif choice1 == 1 and choice2 == 0:
        return tot, 0
    elif choice1 == 0 and choice2 == 1:
        return 0, tot
    else:
        return 0, 0

@app.route('/api/strategies', methods=['GET'])
def strategies_list():
    return jsonify(list(strategies.keys()))

@app.route('/api/play', methods=['POST'])
def play():
    data = request.json
    s1 = data['strategy1']
    s2 = data['strategy2']
    rounds = data['rounds']
    
    m1, m2 = 0, 0
    history1, history2 = [], []
    results = []
    
    for _ in range(rounds):
        choice1 = strategies[s1](history2)
        choice2 = strategies[s2](history1)
        history1.append(choice1)
        history2.append(choice2)
        round_m1, round_m2 = game(choice1, choice2)
        m1 += round_m1
        m2 += round_m2
        results.append({
            'round': _ + 1,
            'choice1': list(key.keys())[list(key.values()).index(choice1)],
            'choice2': list(key.keys())[list(key.values()).index(choice2)],
            'm1': m1,
            'm2': m2
        })
    
    winner = "Bot1 Win" if m1 > m2 else "Bot2 Win" if m2 > m1 else "Draw"
    
    return jsonify({
        'results': results,
        'final_m1': m1,
        'final_m2': m2,
        'winner': winner
    })

def handler(event, context):
    return app(event, context)
