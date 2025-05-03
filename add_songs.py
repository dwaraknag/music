from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["music_therapy"]
collection = db["tracks"]

# Define mood-based songs
data = [
    {
        "mood": "happy",
        "songs": [
            {"title": "Happy - Pharrell Williams", "url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"},
            {"title": "Uptown Funk - Bruno Mars", "url": "https://www.youtube.com/watch?v=OPf0YbXqDm0"},
        ]
    },
    {
        "mood": "sad",
        "songs": [
            {"title": "Someone Like You - Adele", "url": "https://www.youtube.com/watch?v=hLQl3WQQoQ0"},
            {"title": "Let Her Go - Passenger", "url": "https://www.youtube.com/watch?v=RBumgq5yVrA"},
        ]
    },
    {
        "mood": "angry",
        "songs": [
            {"title": "In The End - Linkin Park", "url": "https://www.youtube.com/watch?v=eVTXPUF4Oz4"},
            {"title": "Smells Like Teen Spirit - Nirvana", "url": "https://www.youtube.com/watch?v=hTWKbfoikeg"},
        ]
    },
    {
        "mood": "relaxed",
        "songs": [
            {"title": "Weightless - Marconi Union", "url": "https://www.youtube.com/watch?v=UfcAVejslrU"},
            {"title": "Clair de Lune - Debussy", "url": "https://www.youtube.com/watch?v=CvFH_6DNRCY"},
        ]
    }
]

# Insert or update
for mood_data in data:
    collection.update_one(
        {"mood": mood_data["mood"]},
        {"$set": {"songs": mood_data["songs"]}},
        upsert=True
    )

print("Songs added to MongoDB!")
