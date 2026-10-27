
from flask import Flask, render_template, request

app = Flask(__name__)


class PasswordChecker:
    def __init__(self, password):
        self.password = password

    def length_ok(self):
        return len(self.password) >= 8

    def has_uppercase(self):
        return any(char.isupper() for char in self.password)

    def has_lowercase(self):
        return any(char.islower() for char in self.password)

    def has_digit(self):
        return any(char.isdigit() for char in self.password)

    def has_special(self):
        special_chars = "@#$%^&*!~_+-="
        return any(char in special_chars for char in self.password)

    def validate(self):
        checks = [
            self.length_ok(),
            self.has_uppercase(),
            self.has_lowercase(),
            self.has_digit(),
            self.has_special()
        ]

        score = sum(checks)

        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Moderate"
        else:
            strength = "Strong"

        suggestions = []

        if not checks[0]:
            suggestions.append("Use at least 8 characters.")

        if not checks[1]:
            suggestions.append("Add an uppercase letter (A-Z).")

        if not checks[2]:
            suggestions.append("Add a lowercase letter (a-z).")

        if not checks[3]:
            suggestions.append("Add a number (0-9).")

        if not checks[4]:
            suggestions.append(
                "Add a special character, such as ! or @."
            )

        return strength, score, suggestions


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        password = request.form.get("password", "")

        if password:
            checker = PasswordChecker(password)
            strength, score, suggestions = checker.validate()

            # Send a dictionary to the HTML template
            result = {
                "strength": strength,
                "score": score,
                "suggestions": suggestions
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
