import requests
from time import sleep
import json

host = ""
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

word_list = [
    {"word": "Feather", "cost": 1},
    {"word": "Coal", "cost": 1},
    {"word": "Pebble", "cost": 1},
    {"word": "Leaf", "cost": 2},
    {"word": "Paper", "cost": 2},
    {"word": "Rock", "cost": 2},
    {"word": "Water", "cost": 3},
    {"word": "Twig", "cost": 3},
    {"word": "Sword", "cost": 4},
    {"word": "Shield", "cost": 4},
    {"word": "Gun", "cost": 5},
    {"word": "Flame", "cost": 5},
    {"word": "Rope", "cost": 5},
    {"word": "Disease", "cost": 6},
    {"word": "Cure", "cost": 6},
    {"word": "Bacteria", "cost": 6},
    {"word": "Shadow", "cost": 7},
    {"word": "Light", "cost": 7},
    {"word": "Virus", "cost": 7},
    {"word": "Sound", "cost": 8},
    {"word": "Time", "cost": 8},
    {"word": "Fate", "cost": 8},
    {"word": "Earthquake", "cost": 9},
    {"word": "Storm", "cost": 9},
    {"word": "Vaccine", "cost": 9},
    {"word": "Logic", "cost": 10},
    {"word": "Gravity", "cost": 10},
    {"word": "Robots", "cost": 10},
    {"word": "Stone", "cost": 11},
    {"word": "Echo", "cost": 11},
    {"word": "Thunder", "cost": 12},
    {"word": "Karma", "cost": 12},
    {"word": "Wind", "cost": 13},
    {"word": "Ice", "cost": 13},
    {"word": "Sandstorm", "cost": 13},
    {"word": "Laser", "cost": 14},
    {"word": "Magma", "cost": 14},
    {"word": "Peace", "cost": 14},
    {"word": "Explosion", "cost": 15},
    {"word": "War", "cost": 15},
    {"word": "Enlightenment", "cost": 15},
    {"word": "Nuclear Bomb", "cost": 16},
    {"word": "Volcano", "cost": 16},
    {"word": "Whale", "cost": 17},
    {"word": "Earth", "cost": 17},
    {"word": "Moon", "cost": 17},
    {"word": "Star", "cost": 18},
    {"word": "Tsunami", "cost": 18},
    {"word": "Supernova", "cost": 19},
    {"word": "Antimatter", "cost": 19},
    {"word": "Plague", "cost": 20},
    {"word": "Rebirth", "cost": 20},
    {"word": "Tectonic Shift", "cost": 21},
    {"word": "Gamma-Ray Burst", "cost": 22},
    {"word": "Human Spirit", "cost": 23},
    {"word": "Apocalyptic Meteor", "cost": 24},
    {"word": "Earth’s Core", "cost": 25},
    {"word": "Neutron Star", "cost": 26},
    {"word": "Supermassive Black Hole", "cost": 35},
    {"word": "Entropy", "cost": 45}
]

def query_ollama(system_word):
    prompt = f"""
        ### Context:
            You are a helpful assistant playing a word-based strategy game ( like rock-paper-scrissors ). 
            Your task is to select the most cost-efficient word from a predefined list that can realistically defeat the system word.
        
        ### Constraints:
            1. The system can be defeated by a word from the list given as "Word List".
            2. The key is to choose a word that accomplishes this task and is cost efficient ( Cost is retrieved from the Word List JSON ).
            3. Choose lowest cost word that can logically overpower or neutralize the system word.
            5. The word must be the lowest cost possible.
            6. Response must be only the word chosen.
            7. You must choose at least one word which is more powerful than the system word.

        ### Word List which you MUST USE:
        {json.dumps(word_list, indent=2)}
        
        ### System Word:
            "{system_word}"
        
        ### Examples:
            If the system word is "Galaxy", the best word to defeat it is "Supermassive Black Hole", because it could logically supercede it and it's cost is lower than "Entropy".
            If the system word is "Sun", the best word to defeat it is "Neutron Star", because it could logically supercede it and it's cost is lower than "Supermassive Black Hole".

        ### Output:
            The best word, according to the rules from the list to defeat it.
            Respond only with the best word according to the rules and it MUST be in the Word list.
            Your Response MUST only contain one word taken from the word list.
            No additional information is needed.
        """

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "max_tokens": 10,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    }

    #print(prompt)

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(result.get("response", ""))
        chosen_word = result.get("response", "").strip('"').lower()
        print(f"Attack word: {chosen_word}")

        for index, word_info in enumerate(word_list, start=1):
            if word_info["word"].lower() == chosen_word.lower():
                return index

        return 49 # Return a good answer xd
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return 49 # Return a good answer xd

def what_beats(word):
    return query_ollama(word)

def play_game():
    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        sys_word = ""
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']

            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = what_beats(sys_word)
        data = {"player_id": "KAGHiVOdmh", "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())

def play_game_tests():
    choosen_word = what_beats("hotel")
    data = {"player_id": 256, "word_id": choosen_word, "round_id": 0}
    print(data)

#play_game_tests()

if __name__ == "__main__":
    while True:
        play_game()