# creation.chararacter.logic defines the character creation process.
# the logic will ask for: username, password(hash), name, age, and gender
# temporarily log name, age, and sex (sexChoice enum) into the 'character' table.
# generate 'player' table id and input the username and password(hashed) into the table.
# place playerid into 'character' table.
# load questionare logic
# # Questionare Logic:
# # Player will be asked [8] Questions with [4] options for each question. These questions
# # will be based on morality of their previous life; virtues, sins, desires.
# # based off the answers, the player will be given [3] species options:
# # High Elf, Dark Elf, Vahadar Elf, Wood Elf, Human, Hill Dwarf, Drow, Tararact, Demon, Devil
# gather the species the Player picked and log it into 'character' table using the speciesId.
# species Ids example: species.human, species.darkElf, species.tararact
# Ask them if they wish to be on the [Demon Lord] or [Hero] story path
# If [Demon Lord] set their age to between [18, 32]
# If [Hero] set their age to between [18, 24]
# Set their age in 'character' table.
# 
#
#
#
# Depending on species load their particular logic:
# ex: species.human.logic.py
# await a success response from the species logic
# request for an image submission or image link: allow common file types like png, jpg
import random
import uuid

# backend/codebase/creation/character/creation.character.logic.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database (replace with Prisma or any other database integration)
characters_db = []


# Enum for sexChoice
class SexChoice:
    MALE = 'Male'
    FEMALE = 'Female'


# Endpoint for character creation
@app.route('/creation/character', methods=['POST'])
def create_character():
    data = request.json  # Assuming JSON payload for simplicity

    # Extracting data from the request
    username = data.get('username')
    password_hash = data.get('password_hash')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    # Temporary log into 'character' table
    character_entry = {
        'name': name,
        'age': age,
        'sex': gender,
        # Add more fields as needed
    }
    characters_db.append(character_entry)

    # Generate 'player' table id and input into the table
    player_id = generate_player_id()
    player_entry = {
        'id': player_id,
        'username': username,
        'password': password_hash,
    }

    # Place player id into 'character' table
    character_entry['player_id'] = player_id

    # Load questionnaire logic (you need to implement this)
    species = load_questionnaire_logic()

    # Log species into 'character' table using speciesId
    character_entry['species'] = species

    # Ask about story path
    story_path = ask_story_path()

    # Set age based on story path
    character_entry['age'] = set_age_based_on_story_path(story_path, age)

    # Add character entry to the database
    characters_db.append(character_entry)

    return jsonify({"message": "Character created successfully"})


# Helper functions (replace with actual implementations)
def generate_player_id():
    return str(uuid.uuid4())


def load_questionnaire_logic():
    # Simulated questionnaire with questions and species mapping
    questionnaire = [
        {"question": "What is your favorite color?",
         "options": ["Red", "Blue", "Green", "Yellow"],
         "species_mapping": {"Red": "species.demon",
                             "Blue": "species.highElf",
                             "Green": "species.human",
                             "Yellow": "species.woodElf"}},
        {"question": "Choose a weapon:",
         "options": ["Sword", "Bow", "Staff", "Dagger"],
         "species_mapping": {"Sword": "species.human",
                             "Bow": "species.woodElf",
                             "Staff": "species.highElf",
                             "Dagger": "species.drow"}},
        # Add more questions and species mappings as needed
    ]

    player_answers = []

    # Simulate player answering the questionnaire
    for question in questionnaire:
        answer = random.choice(question["options"])
        player_answers.append({"question": question["question"], "answer": answer})

    # Determine species based on player answers
    species_mapping = {}
    for answer in player_answers:
        for question in questionnaire:
            if answer["answer"] in question["options"]:
                species_mapping.update(question["species_mapping"])

    # If no species is determined, choose a default species
    default_species = "species.human"
    return species_mapping.get(player_answers[-1]["answer"], default_species)


def ask_story_path():
    # Prompt the user to choose a story path
    print("Choose your story path:")
    print("1. Demon Lord")
    print("2. Hero")

    user_choice = input("Enter the number of your chosen path: ")

    if user_choice == '1':
        return 'Demon Lord'
    elif user_choice == '2':
        return 'Hero'
    else:
        # Default to 'Hero' in case of invalid input
        return 'Hero'


def set_age_based_on_story_path(story_path, original_age):
    # Adjust age based on the selected story path
    if story_path == 'Demon Lord':
        return max(18, min(original_age, 32))
    elif story_path == 'Hero':
        return max(18, min(original_age, 24))
    else:
        # Default case
        return original_age


if __name__ == "__main__":
    app.run(debug=True)
