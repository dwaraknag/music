from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["music_therapy"]
collection = db["tracks"]

# Mood detection
def detect_mood(text):
    mood_keywords = {
        "happy": ["happy", "joy", "excited", "great"],
        "sad": ["sad", "cry", "down", "bad"],
        "angry": ["angry", "furious", "mad"],
        "relaxed": ["calm", "relaxed", "peaceful", "chill"]
    }
    for mood, keywords in mood_keywords.items():
        if any(word in text.lower() for word in keywords):
            return mood
    return "relaxed"

# Mood background images
mood_images = {
    "happy": "https://img.freepik.com/premium-vector/happy-music-logo-template-design_20029-410.jpg",
    "sad": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSy1x7IKWkW5n9nwCADz1fktMeOsrXP9KeZTA&s",
    "angry": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtsn0rwEAxd1zi5fUgGK8L0KOH-1HUZLFBGX0KEMORyyck7d-p92-6lJrX2LtZNfWgo3Y&usqp=CAU",
    "relaxed": "https://static.vecteezy.com/system/resources/thumbnails/027/870/964/small_2x/black-music-notes-with-white-background-3d-rendering-photo.jpg"
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hardcoded for now — can be changed to use MongoDB
        if username == "admin" and password == "pass123":
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_input = request.form["user_input"]
    mood = detect_mood(user_input)
    mood_data = collection.find_one({"mood": mood})
    songs = mood_data["songs"] if mood_data else []
    background_url = mood_images.get(mood, "")
    return render_template("result.html", mood=mood, songs=songs, bg_image=background_url)

if __name__ == '__main__':
    app.run(debug=True)
