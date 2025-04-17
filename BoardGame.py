#Flask App for Runaway Train Game


from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

NUM_TILES = 12
NUM_PLAYERS = 4

def roll_die():
    return random.randint(1, 6)

@app.route('/')
def index():
    if 'players' not in session:
        session['players'] = [0] * NUM_PLAYERS  # Starting positions
        session['turn'] = 0
        session['winner'] = None
        session['last_positions'] = [0] * NUM_PLAYERS
    return render_template('index.html', players=session['players'], turn=session['turn'],
                           winner=session['winner'], tiles=NUM_TILES)

@app.route('/roll', methods=['POST'])
def roll():
    turn = session['turn']
    players = session['players']
    last_positions = session['last_positions']
    
    move_roll = roll_die()
    new_position = min(players[turn] + move_roll, NUM_TILES - 1)

    session['last_positions'][turn] = players[turn]
    players[turn] = new_position

    match_roll = roll_die()
    
    if new_position == match_roll - 1:  # tile 1 is index 0
        die1 = roll_die()
        die2 = roll_die()
        if die1 == die2:
            session['winner'] = f'Player {turn + 1}'
        else:
            players[turn] = session['last_positions'][turn]
    
    session['players'] = players
    session['turn'] = (turn + 1) % NUM_PLAYERS if not session['winner'] else turn
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
