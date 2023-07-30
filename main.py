# Import the ui module
import ui

# Import the notes module
import notes

# Import the wrapper function from curses
from curses import wrapper

# Define the main function
def main(stdscr):
  # Display the menu and handle the user input
  ui.display_menu(stdscr)

# Check if the module is being run as the main program
if __name__ == "__main__":
  # Call the wrapper function to run the main function
  wrapper(main)
