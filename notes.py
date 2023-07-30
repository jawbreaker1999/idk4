# Import sqlite3
import sqlite3

# Import db module
import db

# Create a sample note if it does not exist
note_title = "Sample note"
note_body = "This is a sample note"

# Get the note id of the sample note from the database
note_id = db.get_note_by_id(note_title)

# If the note id is None, insert the sample note and the sample tag
if note_id is None:
  # Insert the sample note into the notes table and get its id
  note_id = db.insert_note(note_title, note_body)

  # Insert the sample tag into the tags table and get its id
  tag_name = "sample"
  tag_id = db.insert_tag(tag_name)

  # Attach the sample tag to the sample note in the note_tags table
  db.attach_tag(note_id, tag_id)

  # Print a confirmation message
  print(f"Created a sample note with title '{note_title}' and body '{note_body}' and attached a tag with name '{tag_name}'")
else:
  # Print a message that the sample note already exists
  print(f"A note with title '{note_title}' already exists")
