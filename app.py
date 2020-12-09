# Copyright (C) 2017 Chris Tarazi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, render_template, redirect, \
    url_for, request, flash, escape

import os
import time
import simulator  # Import simulator.py code

app = Flask(__name__)

app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Anzahl der Simulationen
            n = int(escape(request.form["simulations"]))

            if n > 10000000:
                flash("Fehler: 10.000.000 ist die maximale Anzahl der Simulationen")
            elif n < 1:
                flash("Fehler: Anzahl muss größer als Null sein.")
            else:
                start = time.perf_counter()
                draws, gw, gr = simulator.execute_simulation(n)
                end = time.perf_counter()
                return render_template(
                    "results.html",
                    draws=draws,
                    n=n,
                    time=end - start,
                    winners=gw,
                    runners_up=gr)
        except Exception as e:
            print(e)
            flash("Fehler: bitte nur Nummern eingeben.")
    # else:

    return render_template("form.html")


@app.route("/count", methods=["GET"])
def count():
    try:
        start = time.perf_counter()
        count = simulator.count_possible_draws()
        end = time.perf_counter()
        return render_template("count.html", count=count, time=end - start)
    except Exception as e:
        print(e)
        flash("Fehler: etwas ging schief beim berechnen der Möglichkeiten, versuche es noch einmal.")

    return redirect("/")


@app.context_processor
def utility_processor():
    def format_odds(odds):
        # Format floating point to 5 decimal places.
        return "{0:.5}".format(odds)

    return dict(format_odds=format_odds)


if __name__ == "__main__":
    app.run()
