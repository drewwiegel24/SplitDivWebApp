from flask import Flask, redirect, render_template, request, session, url_for
from fractions import Fraction
import secrets

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

@app.route("/equivalentSplit")
def equivalentSplit():
    float_div = float(session.get('div_val', None))
    float_split = (float_div + 100) / 100
    stock_split = Fraction(float_split)
    return "Equivalent stock split: %s" % str(stock_split).replace("/", ":")

@app.route("/equivalentDividend")
def equivalentDividend():
    split_vals = session.get('split_val', None).split(":")
    dividend = (float(split_vals[0]) - float(split_vals[1])) / float(split_vals[1])
    dividend *= 100
    return "Equivalent stock dividend: %s percent" % str(dividend)


@app.route("/dataSubmission", methods=["GET", "POST"])
def dataSubmission():
    if request.method == "POST":
        print(request.form)
        print(len(request.form['div']))
        print(len(request.form['split']))
        dividend = request.form["div"]
        split = request.form["split"]
        if (len(dividend) == 0 and len(split) == 0):
            return render_template("dataSubmission.html")
        if (len(dividend) > 0):
            session['div_val'] = dividend
            return redirect(url_for("equivalentSplit"))
        else:
            session['split_val'] = split
            return redirect(url_for("equivalentDividend"))
    elif request.method == "GET":
        dividend = request.args.get("div")
        return render_template("dataSubmission.html")
    else:
        return render_template("dataSubmission.html")

@app.errorhandler(403)
def forbidden_page(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(port=5000, debug=True)