from flask import Flask, render_template, request, redirect, url_for, session
import pickle

app = Flask(__name__)
app.secret_key = "secure_key_123"

# ---------------- LOGIN CREDENTIALS ----------------
USERNAME = "Batch2"
PASSWORD = "project"

# ---------------- LOAD MODEL ----------------
mb = pickle.load(open('nlp model.pkl', 'rb'))
cv = pickle.load(open('transform.pkl', 'rb'))

# ---------------- LOGIN DECORATOR ----------------
def login_required(route):
    def wrapper(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for('login'))
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper

# ---------------- ROUTES ----------------

# 1️⃣ Welcome Page
@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

# 2️⃣ Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for('home'))
        else:
            error = "❌ Invalid Username or Password"
    return render_template("login.html", error=error)

# 3️⃣ Home / Project Page
@app.route('/home')
@login_required
def home():
    return render_template("home.html")

# 4️⃣ About Page
@app.route('/about')
@login_required
def about():
    return render_template("about.html")

# 5️⃣ Detect Page
@app.route('/detect')
@login_required
def detect():
    return render_template("detect.html")

# 6️⃣ Prediction Route
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    message = request.form['message']
    vect = cv.transform([message]).toarray()

    # Prediction
    prediction_label = "Spam" if mb.predict(vect)[0] == 1 else "Ham"

    # Probabilities
    probs = mb.predict_proba(vect)[0]  # [Ham_prob, Spam_prob]
    ham_prob = round(probs[0]*100, 2)
    spam_prob = round(probs[1]*100, 2)

    # Overall confidence
    confidence = max(ham_prob, spam_prob)

    # Explanation
    explanation = (
        "This email contains suspicious keywords and patterns commonly found in spam emails."
        if prediction_label == "Spam"
        else "This email appears legitimate based on its content."
    )

    return render_template(
        "result.html",
        prediction=prediction_label,
        confidence=confidence,
        spam_prob=spam_prob,
        ham_prob=ham_prob,
        explanation=explanation
    )

# 7️⃣ Logout Route
@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect(url_for('login'))

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
