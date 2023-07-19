from flask import Flask, render_template, request

app = Flask(__name__)

def estimate_cost_cocomo_ii(loc, team_size, cost_per_staff_month):

    effort = 2.94 * (loc / 1000) ** 1.12
    duration = 3.67 * (effort ** 0.28)
    staff_months = effort
    total_cost = staff_months * team_size * cost_per_staff_month

    return total_cost, duration

def convert_duration_to_years_months_days(duration):
    years = int(duration // 12)
    months = int(duration % 12)
    days = int((duration - int(duration)) * 30)
    return years, months, days

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        loc = int(request.form["lines_of_code"])
        team_size = int(request.form["team_size"])
        cost_per_staff_month = float(request.form["cost_per_staff_month"])
        total_cost, duration = estimate_cost_cocomo_ii(loc, team_size, cost_per_staff_month)
        result = {"cost": total_cost, "duration_years": 0, "duration_months": 0, "duration_days": 0}

        if duration >= 1:
            result["duration_years"], result["duration_months"], result["duration_days"] = convert_duration_to_years_months_days(duration)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
