# Import sqlite3
import sqlite3

# Create a connection object to the database file
conn = sqlite3.connect("notes.db")

# Create a cursor object
cur = conn.cursor()

# Create the notes table if it does not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
  note_id INTEGER PRIMARY KEY,
  note_title TEXT NOT NULL,
  note_body TEXT NOT NULL
);
""")

# Create the tags table if it does not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS tags (
  tag_id INTEGER PRIMARY KEY,
  tag_name TEXT NOT NULL
);
""")

# Create the note_tags table if it does not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS note_tags (
  note_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY (note_id, tag_id),
  FOREIGN KEY (note_id) REFERENCES notes (note_id),
  FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
);
""")

# Define a function to get all notes from the database
def get_all_notes():
  # Execute a SQL query to select all notes and their tags
  cur.execute("""
  SELECT n.note_id, n.note_title, n.note_body, GROUP_CONCAT(t.tag_name) AS tags
  FROM notes n
  LEFT JOIN note_tags nt ON n.note_id = nt.note_id
  LEFT JOIN tags t ON nt.tag_id = t.tag_id
  GROUP BY n.note_id, n.note_title, n.note_body
  """)
  
  # Fetch all the rows from the cursor
  rows = cur.fetchall()
  
  # Return the rows as a list of tuples
  return rows

# Define a function to get a note by its id from the database
def get_note_by_id(note_id):
  # Execute a SQL query to select a note and its tags by its id
  cur.execute("""
  SELECT n.note_id, n.note_title, n.note_body, GROUP_CONCAT(t.tag_name) AS tags
  FROM notes n
  LEFT JOIN note_tags nt ON n.note_id = nt.note_id
  LEFT JOIN tags t ON nt.tag_id = t.tag_id
  WHERE n.note_id = ?
  GROUP BY n.note_id, n.note_title, n.note_body
  """, (note_id,))
  
  # Fetch one row from the cursor
  row = cur.fetchone()
  
  # Return the row as a tuple or None if not found
  return row

# Define a function to insert a note into the database
def insert_note(note_title, note_body):
  # Execute a SQL query to insert a note into the notes table
  cur.execute("INSERT INTO notes (note_title, note_body) VALUES (?, ?)", (note_title, note_body))
  
  # Get the note_id of the last inserted note
  note_id = cur.lastrowid
  
  # Commit the changes to the database
  conn.commit()
  
  # Return the note_id of the inserted note
  return note_id

# Define a function to update a note in the database
def update_note(note_id, note_title, note_body):
  # Execute a SQL query to update a note in the notes table by its id
  cur.execute("UPDATE notes SET note_title = ?, note_body = ? WHERE note_id = ?", (note_title, note_body, note_id))
  
  # Commit the changes to the database
  conn.commit()

# Define a function to delete a note from the database
def delete_note(note_id):
  # Execute a SQL query to delete a note from the notes table by its id
  cur.execute("DELETE FROM notes WHERE note_id = ?", (note_id,))
  
  # Commit the changes to the database
  conn.commit()

# Define a function to get all tags from the database
def get_all_tags():
  # Execute a SQL query to select all tags from the tags table
  cur.execute("SELECT * FROM tags")
  
  # Fetch all the rows from the cursor
  rows = cur.fetchall()
  
  # Return the rows as a list of tuples
  return rows

# Define a function to get a tag by its id from the database
def get_tag_by_id(tag_id):
   # Execute a SQL query to select a tag from the tags table by its id 
   cur.execute("SELECT * FROM tags WHERE tag_id = ?", (tag_id,))
   
   # Fetch one row from the cursor
   row = cur.fetchone()
   
   # Return the row as a tuple or None if not found
   return row

# Define a function to insert a tag into the database
def insert_tag(tag_name):
  # Execute a SQL query to insert a tag into the tags table
  cur.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag_name,))
  
  # Get the tag_id of the last inserted tag
  tag_id = cur.lastrowid
  
  # Commit the changes to the database
  conn.commit()
  
  # Return the tag_id of the inserted tag
  return tag_id

# Define a function to update a tag in the database
def update_tag(tag_id, tag_name):
  # Execute a SQL query to update a tag in the tags table by its id
  cur.execute("UPDATE tags SET tag_name = ? WHERE tag_id = ?", (tag_name, tag_id))
  
  # Commit the changes to the database
  conn.commit()

# Define a function to delete a tag from the database
def delete_tag(tag_id):
  # Execute a SQL query to delete a tag from the tags table by its id
  cur.execute("DELETE FROM tags WHERE tag_id = ?", (tag_id,))
  
  # Commit the changes to the database
  conn.commit()

# Define a function to attach a tag to a note in the database
def attach_tag(note_id, tag_id):
  # Execute a SQL query to insert a record into the note_tags table
  cur.execute("INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))
  
  # Commit the changes to the database
  conn.commit()

# Define a function to detach a tag from a note in the database
def detach_tag(note_id, tag_id):
  # Execute a SQL query to delete a record from the note_tags table
  cur.execute("DELETE FROM note_tags WHERE note_id = ? AND tag_id = ?", (note_id, tag_id))
  
  # Commit the changes to the database
  conn.commit()
