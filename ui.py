# Import curses and the wrapper function
import curses

# Import the notes module
import notes

# Import the db module
import db

# Define a function to display a menu of notes
def display_menu(stdscr):
  # Turn off the cursor
  curses.curs_set(0)

  # Get the size of the screen
  height, width = stdscr.getmaxyx()

  # Create a subwindow for the menu
  menu_win = stdscr.subwin(height - 2, width - 2, 1, 1)
  menu_win.box()

  # Create a subwindow for the status bar
  status_win = stdscr.subwin(1, width, height - 1, 0)
  status_win.bkgd(curses.color_pair(1))
  status_win.addstr(0, 0, "Press Q to quit, ENTER to select")

  # Initialize the menu items
  menu_items = []

  # Query the database and get the notes
  with db.conn: # Use db.conn instead of notes.conn
    cur = db.conn.cursor() # Use db.conn instead of notes.conn
    cur.execute("""
    SELECT n.note_id, n.note_title, n.note_body, GROUP_CONCAT(t.tag_name) AS tags
    FROM notes n
    LEFT JOIN note_tags nt ON n.note_id = nt.note_id
    LEFT JOIN tags t ON nt.tag_id = t.tag_id
    GROUP BY n.note_id, n.note_title, n.note_body
    """)
    
    # Fetch all the rows from the cursor
    rows = cur.fetchall()
    
    # Add each row as a menu item
    for row in rows:
      menu_items.append(row)

  # Initialize the current selection index
  current_index = 0

  # Start the main loop
  while True:
    # Clear the menu window
    menu_win.clear()
    menu_win.box()

    # Display the menu items
    for i, item in enumerate(menu_items):
      # Get the note id, title, body and tags from the item
      note_id, note_title, note_body, tags = item

      # Highlight the current selection with a different color pair
      if i == current_index:
        menu_win.attron(curses.color_pair(2))
        menu_win.addstr(i + 1, 2, f"{note_id}. {note_title}")
        menu_win.attroff(curses.color_pair(2))
      else:
        menu_win.addstr(i + 1, 2, f"{note_id}. {note_title}")

    # Refresh the windows
    stdscr.refresh()
    menu_win.refresh()
    status_win.refresh()

    # Get the user input
    key = stdscr.getch()

    # Handle the user input
    if key == curses.KEY_UP and current_index > 0:
      # Move up the selection index
      current_index -= 1
    elif key == curses.KEY_DOWN and current_index < len(menu_items) - 1:
      # Move down the selection index
      current_index += 1
    elif key == curses.KEY_ENTER or key in [10,13]:
      # Enter key was pressed, display the note details
      display_note(stdscr, menu_items[current_index])
      # Return to the menu after displaying the note details
      stdscr.clear()
      stdscr.box()
      status_win.clear()
      status_win.bkgd(curses.color_pair(1))
      status_win.addstr(0, 0, "Press Q to quit, ENTER to select")
    elif key == ord('q') or key == ord('Q'):
      # Q key was pressed, exit the program
      break

# Define a function to display a note details
def display_note(stdscr, note_item):
  # Get the note id, title, body and tags from the item
  note_id, note_title, note_body, tags = note_item

  # Get the size of the screen
  height, width = stdscr.getmaxyx()

  # Create a subwindow for the note details
  note_win = stdscr.subwin(height - 2, width - 2, 1, 1)
  note_win.box()

  # Create a subwindow for the status bar
  status_win = stdscr.subwin(1, width, height - 1, 0)
  status_win.bkgd(curses.color_pair(1))
  status_win.addstr(0, 0, "Press any key to return")

  # Display the note details
  note_win.addstr(1, 2, f"Note ID: {note_id}")
  note_win.addstr(2, 2, f"Note Title: {note_title}")
  note_win.addstr(3, 2, f"Note Body: {note_body}")
  note_win.addstr(4, 2, f"Tags: {tags}")

  # Refresh the windows
  stdscr.refresh()
  note_win.refresh()
  status_win.refresh()

  # Wait for any key press to return
  stdscr.getch()
