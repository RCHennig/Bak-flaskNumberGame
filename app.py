from flask import Flask, render_template, request, session, redirect, url_for
from pygame import mixer
import random
import time
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"
#TIME_LIMIT = 10

# Set up the MySQL connection
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="PlayerData"
)
db_cursor = db_connection.cursor()

def start_new_round():
    session["target_number"] = random.randint(1, 100)

def start_new_game():
    session["score"]= 0
    session["guessScore"]=0
    start_new_round()

def save_score(player, score):
    sql = "INSERT INTO scores (player, score) VALUES (%s, %s)"
    values = (player, score)
    db_cursor.execute(sql, values)
    db_connection.commit()

@app.route("/play", methods=["GET", "POST"])

def game():

    volume = session["audioVolume"] / 100
    mixer.music.set_volume(volume)

    if "guessScore" not in session:
        session["guessScore"]=0
    if "score" not in session:
        session["score"] = 0
    if "target_number" not in session:
        session["message"]= "Runde Vorbei"
        #start_new_round()

    if request.method == "POST":
        guess = int(request.form["guess"])

        if guess == session["target_number"]:
            session["message"] = "Congratulations! You guessed the correct number."
            player_name = "Player"  # You can customize this to take player's name as input
            session["score"] += 10
            session["guessScore"] += 1
            if session["guessScore"]>0: #Anzahl der zu erratenden Zahlen pro Runde
                return redirect("/endscreen", code=302)

            else:
                start_new_round()
        elif guess < session["target_number"]:
            session["message"] = "Try higher!"
            session["score"] -= 1
        else:
            session["message"] = "Try lower!"
            session["score"] -= 1

    return render_template("game.html", score=session["score"], message=session.get("message"))

@app.route("/scores")
def scores():
    volume = session["audioVolume"] / 100
    mixer.music.set_volume(volume)

    sql = "SELECT player, score FROM scores ORDER BY score DESC"
    db_cursor.execute(sql)
    scores = db_cursor.fetchall()
    return render_template("scores.html", scores=scores)

@app.route("/")
def menu():
    if "audioVolume" not in session:
        session["audioVolume"] = 0.5

    mixer.init()
    volume = session["audioVolume"] / 100
    mixer.music.set_volume(volume)
    mixer.music.load('./music/backgroundMusic.mp3')
    mixer.music.play(999)
    return render_template("menu.html")

@app.route("/endscreen", methods=["GET","POST"])
def endscreen():
    volume = session["audioVolume"] / 100
    mixer.music.set_volume(volume)

    if request.method=="POST":
        playerName =(request.form["playername"])
        save_score(playerName,session["score"])

    return render_template("endscreen.html")

@app.route("/options", methods=["GET","POST"])
def options():
    if request.method=="POST":
        #print('test')
        session["audioVolume"] = int(request.form.get("audioVolume"))
        volume = session["audioVolume"] / 100
        mixer.music.set_volume(volume)
        #print(session["audioVolume"])
        #print(volume)
    
    return render_template("options.html", audioVolume=session["audioVolume"])

if __name__ == "__main__":
    app.run(debug=True)