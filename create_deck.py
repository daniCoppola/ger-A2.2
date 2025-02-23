import genanki
import os
import re

from anki.collection import Collection as aopen
from anki.importing.apkg import AnkiPackageImporter

my_model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'German'},
        {'name': 'English'},
    ],
    templates=[
        {
            'name': 'DE-ENG',
            'qfmt': '{{German}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{English}}',
        },
        {
            'name': 'ENG-DE',
            'qfmt': '{{English}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{German}}',
        },
    ])


def read_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    title_pattern = r"^#+\s([a-zA-Z0-9]+)"
    word_pattern = r"([a-zA-Z ]+)=([a-zA-Z ]+)"
    document = {}
    for i, line in enumerate(lines):
        if re.match(title_pattern, line):
            title = re.findall(title_pattern, line)[0].lower()
            document[title] = []
        if "=" in line:
            if re.match(word_pattern, line):
                ger_to_eng = re.findall(word_pattern, line)[0]
                document[title].append(ger_to_eng)
    return document


def create_notes(model, ger_to_eng):
    notes = []
    for note in ger_to_eng:
        notes.append(genanki.Note(model=model,
                     fields=[note[0], note[1]]))
        print(f"Created note. GER:{note[0]}\t ENG:{note[1]}")
    return notes


def main():
    folder_path = "./"
    model = my_model
    notes_collection = {}
    exclude_files = ["README.md", "template.md"]
    # Go over all md files
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".md") \
                and filename not in exclude_files:
            print(f"Importing {file_path}")
            ger_to_eng = read_file(file_path)
            title = filename[:-3]
            notes_collection[title] = create_notes(
                model, ger_to_eng["vocabulary"])

    all_deck_name = "GER-A2.2::all"
    all_deck_id = 999999999
    all_deck = genanki.Deck(all_deck_id, all_deck_name)

    decks = []
    for title, notes in notes_collection.items():
        if len(notes) == 0:
            continue
        deck_id = abs(hash(title)) % (10**9)
        deck_name = f"GER-A2.2::{title}"
        deck = genanki.Deck(deck_id, deck_name)
        for note in notes:
            deck.add_note(note)
            all_deck.add_note(note)
        decks.append(deck)
    decks.append(all_deck)
    output_file = 'decks/GER-A2.2.apkg'
    genanki.Package(decks).write_to_file(output_file)

    col = aopen("/home/dan/.local/share/Anki2/User 1/collection.anki2")
    imp = AnkiPackageImporter(col, output_file)
    imp.run()


if __name__ == "__main__":
    main()
