from flask import Flask, render_template, request, redirect, url_for
import itertools

app = Flask(__name__)

gruppen = []
tabellen = []

def gruppen_erstellen(spieler, gruppen_anzahl):
    gruppen = [[] for _ in range(gruppen_anzahl)]
    for i, spieler_name in enumerate(spieler):
        gruppen[i % gruppen_anzahl].append(spieler_name)
    return gruppen

def tabelle_initialisieren(gruppe):
    return {spieler: {"Punkte": 0, "Spiele": 0} for spieler in gruppe}

@app.route("/", methods=["GET", "POST"])
def index():
    global gruppen, tabellen

    if request.method == "POST":
        spieler = request.form["spieler"].split(",")
        spieler = [s.strip() for s in spieler]
        gruppen_anzahl = int(request.form["gruppen"])

        gruppen = gruppen_erstellen(spieler, gruppen_anzahl)
        tabellen = [tabelle_initialisieren(g) for g in gruppen]

        return redirect(url_for("turnier"))

    return render_template("index.html")

@app.route("/turnier", methods=["GET", "POST"])
def turnier():
    global gruppen, tabellen

    if request.method == "POST":
        gruppe_index = int(request.form["gruppe"])
        spieler1 = request.form["spieler1"]
        spieler2 = request.form["spieler2"]
        score1 = int(request.form["score1"])
        score2 = int(request.form["score2"])

        tabelle = tabellen[gruppe_index]

        tabelle[spieler1]["Spiele"] += 1
        tabelle[spieler2]["Spiele"] += 1

        if score1 > score2:
            tabelle[spieler1]["Punkte"] += 2
        elif score2 > score1:
            tabelle[spieler2]["Punkte"] += 2
        else:
            tabelle[spieler1]["Punkte"] += 1
            tabelle[spieler2]["Punkte"] += 1

        return redirect(url_for("turnier"))

    spielplaene = [list(itertools.combinations(g, 2)) for g in gruppen]

    return render_template("index.html", gruppen=gruppen, tabellen=tabellen, spielplaene=spielplaene)

if __name__ == "__main__":
    app.run(debug=True)
