import random
import tkinter as tk
from tkinter import ttk
import json
import urllib.request
import io
from PIL import ImageTk, Image

class AddButton(): 
    """Generic button class"""
    def __init__(self, root, text, clicked):
        self.root = root
        self.button = ttk.Button(self.root, text=text, command=clicked)

class Display(AddButton):
    """Class to add buttons with images to the GUI"""
    def __init__(self, root, window, item):
        AddButton.__init__(self, root, None, None)
        self.item = item
        print(item)
        try:
            with urllib.request.urlopen(item.image) as u:
                self.raw_data = u.read()
            self.image = Image.open(io.BytesIO(self.raw_data))
            self.image = self.image.resize((50, 50))
            self.photo = ImageTk.PhotoImage(self.image, (50, 50))
            self.button = ttk.Button(self.root, text = item.name, image = self.photo, compound = tk.LEFT, command=lambda:window.item_edit_mode(self.item))
        except Exception as e:
            print(f"Error loading image: {e}")
            try:
                self.image = Image.open(r'./error.png')
                self.image = self.image.resize((50, 50))
                self.photo = ImageTk.PhotoImage(self.image, (50,50))
                self.button = ttk.Button(self.root, text=item.name, image=self.photo, compound=tk.LEFT, command=lambda:window.item_edit_mode(self.item))
            except Exception as e:
                self.button = ttk.Button(self.root, text=item.name, compound=tk.LEFT, command=lambda:window.item_edit_mode(self.item))

class MuseumItem():
    """Class representing a museum item"""
    def __init__(self, item):
        self.name = item['name']
        self.description = item['description']
        self.context = item['context']
        self.id = item['id']
        self.image = item['image']
        self.borrowed = item['borrowed']
        self.times_searched = item['times_searched']

    def get_as_dict(self):
        """Returns the item as a dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'context': self.context,
            'id': self.id,
            'image': self.image,
            'borrowed': self.borrowed,
            'times_searched': self.times_searched
        }


class Window():
    """Class responsible for running the entire program and displaying the GUI"""
    def __init__(self, json_data):
        """The constructor for the Window class, receives the json data and sets up the GUI"""
        #creates the canvas and sets it up
        self.root = tk.Tk()
        self.root.title("P-Uppgift")
        self.root.geometry("600x600")
        #creates string variables for the GUI
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.context_var = tk.StringVar()
        self.borrowed = tk.BooleanVar()
        self.borrowed.set(False)
        self.borrowed_text = tk.StringVar()
        self.mode_text = tk.StringVar()
        self.item_url = tk.StringVar()
        self.item_url.set("https://www.example.com/image.jpg")
        self.borrowed_text.set("Borrow")
        self.item_list = [MuseumItem(item) for item in json_data] #Creates a list of MuseumItem objects from the json data
        self.item_being_edited = None
        self.show_borrowed = False



    def make_button(self):
        """Creates the buttons for the GUI, just looks cluttered af"""
        canvas = tk.Canvas(self.root, width=300, height=300)
        canvas.place (relx=0, rely=0, anchor=tk.NW)
        search_label = ttk.Label(
            self.root, text="Search for item",font=('calibre', 10, 'bold'), background="white")
        search_label.grid(row=0, column=0)
        search_button = ttk.Button(self.root, text='Search', command=self.search_mode)
        search_button.grid(row=0, column=1)

        create_label = ttk.Label(
            self.root, text="Create new item", font=('calibre', 10, 'bold'), background="white")
        create_label.grid(row=1, column=0)
        create_button = ttk.Button(self.root, text='Create', command=self.item_create_mode)
        create_button.grid(row=1, column=1)
        finnish_button = ttk.Button(self.root, text='Finnish', command=self.finnish)
        finnish_button.grid(row=2, column=1)
        self.main_menu = [
            search_label, search_button, create_label, create_button, finnish_button
        ]
        self.current_mode = self.main_menu

        #search mode
        entry_label = ttk.Label(self.root, text = "Search for item",font = ('calibre',10,'bold'))
        entry = ttk.Entry(self.root, textvariable = self.name_var ,font = ('calibre',10,'bold'))      
        entry_label.grid(row=3, column=0)
        entry.grid(row=3, column=1)
        self.show_borrowed_btn = ttk.Button(self.root, text='Show borrowed', command=lambda:self.toggle_show_borrowed())
        self.show_borrowed_btn.grid(row=3, column=2)
        sub_btn=ttk.Button(self.root,text = 'Search', command = self.search)
        back_btn=ttk.Button(self.root,text = 'Back', command = self.main_menu_mode)
        self.search_buttons = self.displayed = [
            entry_label, entry,
            sub_btn, back_btn,
            self.show_borrowed_btn
        ]
        self.hide(self.search_buttons)

        #create Mode
        create_label = ttk.Label(self.root, text="Create new item", font=('calibre', 10, 'bold'))
        create_label.grid(row=3, column=0)
        name_label = ttk.Label(self.root, text="Name", font=('calibre', 10, 'bold'))
        name_label.grid(row=4, column=0)
        create_name_entry = ttk.Entry(self.root, textvariable=self.name_var, font=('calibre', 10, 'bold'))
        create_name_entry.grid(row=4, column=1)
        description_label = ttk.Label(self.root, text="Description", font=('calibre', 10, 'bold'))
        description_label.grid(row=5, column=0)
        create_description_entry = ttk.Entry(
            self.root, textvariable=self.description_var, font=('calibre', 10, 'bold'))
        create_description_entry.grid(row=5, column=1)
        context_label = ttk.Label(self.root, text="Context", font=('calibre', 10, 'bold'),)
        context_label.grid(row=6, column=0)
        create_context_entry = ttk.Entry(self.root, textvariable=self.context_var, font=('calibre', 10, 'bold'))
        create_context_entry.grid(row=6, column=1)
        create_item_url_label = ttk.Label(self.root, text="Image URL", font=('calibre', 10, 'bold'))
        create_item_url_label.grid(row=7, column=0)
        create_item_url_entry = ttk.Entry(self.root, textvariable=self.item_url, font=('calibre', 10, 'bold'))
        create_item_url_entry.grid(row=7, column=1)
        create_borrowed_button = ttk.Button(self.root, textvariable=self.borrowed_text, command=lambda: self.borrow_check())
        create_borrowed_button.grid(row=8, column=2)
        create_sub_btn = ttk.Button(self.root, textvariable=self.mode_text, command=self.create)
        create_sub_btn.grid(row=8, column=1)
        remove_button = ttk.Button(self.root, text='Remove', command=self.remove)
        remove_button.grid(row=8, column=0)
        self.create_mode = [
            create_label, name_label,
            create_name_entry, description_label,
            create_description_entry, context_label,
            create_context_entry, 
            create_sub_btn, remove_button,
            create_borrowed_button, create_item_url_entry,
            create_item_url_label
        ]
        self.hide(self.create_mode)


    def borrow_check(self):
        """Checks if the item is borrowed or not"""
        self.borrowed.set(not self.borrowed.get())
        self.borrowed_text.set("Return" if self.borrowed.get() else "Borrow") #If borrowed, set to return, else borrow



    def run(self):
        """Runs the GUI and starts the main loop"""
        
        self.make_button()
        self.root.mainloop()

    def toggle_show_borrowed(self):
        """Toggles the show borrowed button"""
        print("toggle")
        if self.show_borrowed:
            self.show_borrowed_btn.config(text='Show borrowed')
        else:
            self.show_borrowed_btn.config(text='Hide borrowed')
        self.show_borrowed = not self.show_borrowed
        print(self.show_borrowed)

    def hide(self, widgets):
        """Hides the widgets in the GUI"""
        for widget in widgets:
            widget.grid_remove()

    def show(self, widgets):
        """Shows the widgets in the GUI"""
        for widget in widgets:
            widget.grid()

    def main_menu_mode(self):
        """Shows the main menu"""
        self.hide(self.current_mode)
        self.show(self.main_menu)
        self.current_mode = self.main_menu

    def search_mode(self):
        """Shows the search mode"""
        self.hide(self.current_mode)
        self.current_mode = self.search_buttons
        self.show(self.search_buttons)

    def item_create_mode(self):
        """Shows the create mode"""
        self.mode_text.set(
            "Edit" if self.item_being_edited else "Create"
        )
        self.hide(self.current_mode)
        self.show(self.create_mode)
        self.current_mode = self.create_mode


    def create(self):
        """Creates a new item or edits an existing one"""
        if self.item_being_edited:
            self.borrowed.set(self.item_being_edited.borrowed)
            self.borrowed_text.set("return" if self.item_being_edited.borrowed else "borrow")
            self.item_being_edited.name = self.name_var.get()
            self.item_being_edited.description = self.description_var.get().split(",")
            self.item_being_edited.context = self.context_var.get()
            self.item_being_edited.borrowed = self.borrowed.get()
        else:
            new_item = MuseumItem(
                self.name_var.get(),
                self.description_var.get().split(","),
                self.context_var.get(),
                random.randint(0, 1000000),#random id is generated
                self.item_url.get(),
                self.borrowed.get(),
                0
            )
            self.item_list.append(new_item)
        self.item_being_edited = None
        self.name_var.set("")
        self.description_var.set("")
        self.context_var.set("")
        self.item_url.set("")
        #clicked_item  = [x for x in filter(lambda x: x['id'] == id, self.a)][0]
        #self.json_data.up
        self.main_menu_mode()

    def remove(self):
        """Removes the item from the list"""
        if self.item_being_edited:
            self.item_list.remove(self.item_being_edited)
            self.item_being_edited = None
        self.name_var.set("")
        self.description_var.set("")
        self.context_var.set("")
        self.item_url.set("")
        self.main_menu_mode()

    def item_edit_mode(self, item):
        """Sets the edit mode for the item"""
        self.name_var.set(item.name)
        self.description_var.set(("".join(x + "," for x in item.description)).strip(","))
        self.context_var.set(item.context)
        self.item_url.set(item.image)
        self.item_being_edited = item
        self.hide(self.displayed)
        self.item_create_mode()

    def search(self):
        """Searches for items in the item list and displays them"""
        self.hide(self.current_mode)
        self.show(self.search_buttons)
        self.current_mode = self.search_buttons
        search_results = []

        key_words=self.name_var.get().split(",") #Splits what you searched for into multiple words and looks if any of them are in the name, description or context of the item
        if self.show_borrowed:
            for key_word in key_words:
                search_results.extend([item for item in self.item_list #Just searching through everythingg
                    if key_word in item.name
                    or key_word in "".join(desc for desc in item.description)
                    or key_word in item.context
                    or str(item.id) == key_word
                ])
        else:
            for key_word in key_words:
                search_results.extend([item for item in self.item_list #Just searching through everythingg
                    if (key_word in item.name
                    or key_word in "".join(desc for desc in item.description)
                    or key_word in item.context
                    or str(item.id) == key_word)
                    and not item.borrowed
                ])
        #search for item
        self.formated_non_duplicate_results = list({v.id:v for v in search_results}.values()) # removes duplicates

        for x in self.formated_non_duplicate_results: 
           x.times_searched += 1#increments the amount of times the item has been searched for
        self.displayed_search_results(self.formated_non_duplicate_results)

    def displayed_search_results(self , search_results):
        """Displays the search results in the GUI"""
        print(search_results)
        self.displayed_results = [Display(self.root, self, museum_item) for museum_item in search_results]
        self.displayed = self.displayed[:5] #Keeps only the first elements here, that being the search buttons and shit, this is done to cut away any previous searchresults in the case that you would press search twice in a row
        print(len(self.displayed_results))
        self.photos = []
        for i in range(len(search_results)):
            self.displayed.append(self.displayed_results[i].button) #Creates an array with only the button objects in the display objects so that they can be displayed
        self.hide(self.current_mode)
        self.current_mode = self.displayed
        self.show(self.displayed)

    def finnish(self):
        """Calls the save function"""
        save_and_exit(self.item_list)







class TerminalMuseum:
    """Class responsible for running the terminal-based program"""
    def __init__(self, json_data):
        self.item_list = [MuseumItem(item) for item in json_data]
        self.item_being_edited = None

    def main_menu(self):
        """Displays the main menu"""
        while True:
            print("\nMain Menu:")
            print("1. Search for an item")
            print("2. Create a new item")
            print("3. Edit an item")
            print("4. Remove an item")
            print("5. Show all items")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.search_items()
            elif choice == "2":
                self.create_item()
            elif choice == "3":
                self.edit_item()
            elif choice == "4":
                self.remove_item()
            elif choice == "5":
                self.show_all_items()
            elif choice == "6":
                self.finnish()
            else:
                print("Invalid choice. Please try again.")

    def search_items(self):
        """Searches for items in the item list"""
        query = input("Enter search keywords (comma-separated): ").split(",")
        results = []
        if input("Show borrowed items? (yes/no): ").strip().lower() == "yes":
            for key_word in query:
                results.extend([item for item in self.item_list #Just searching through everythingg
                    if (key_word in item.name
                    or key_word in "".join(desc for desc in item.description)
                    or key_word in item.context
                    or str(item.id) == key_word)
                    and not item.borrowed
                ])
        else:
            for key_word in query:
                results.extend([item for item in self.item_list #Just searching through everythingg
                    if key_word in item.name
                    or key_word in "".join(desc for desc in item.description)
                    or key_word in item.context
                    or str(item.id) == key_word
                ])
        results = list({item.id: item for item in results}.values())  # Remove duplicates
        for item in results:
            item.times_searched += 1
        if results:
            print("\nSearch Results:")
            for item in results:
                print(f"- {item.name} (ID: {item.id})")
        else:
            print("No items found.")

    def create_item(self):
        """Creates a new item"""
        new_item_dict = {
            "name" : input("Enter item name: "),
            "description": input("Enter item description (comma-seperated for multiple keywords): ").split(","),
            "context": input("Enter item context: "),
            "image": input("Enter item image URL: "),
            "borrowed": input("Is the item borrowed? (yes/no): ").strip().lower() == "yes",
            "id": random.randint(0, 1000000),
            "times_searched": 0
        }
        new_item = MuseumItem(new_item_dict)
        self.item_list.append(new_item)
        print("Item created successfully.")

    def edit_item(self):
        """Edits an existing item"""
        item_id = input("Enter the ID of the item to edit: ")
        item = next((item for item in self.item_list if str(item.id) == item_id), None)
        if item:
            print(f"Editing item: {item.name}")
            print("Press Enter to keep the current value.")
            item.name = input(f"Enter new name (current: {item.name}): ") or item.name
            item.description = input(
                f"Enter new description (current: {item.description}): ") or item.description
            item.context = input(f"Enter new context (current: {item.context}): ") or item.context
            item.image = input(f"Enter new image URL (current: {item.image}): ") or item.image
            item.borrowed = input(
                f"Is the item borrowed? (yes/no, current: {'yes' if item.borrowed else 'no'}): "
                ).strip().lower() == "yes"
            print("Item updated successfully.")
        else:
            print("Item not found.")

    def remove_item(self):
        """Removes an item from the list"""
        item_id = input("Enter the ID of the item to remove: ")
        item = next((item for item in self.item_list if str(item.id) == item_id), None)
        if item:
            self.item_list.remove(item)
            print("Item removed successfully.")
        else:
            print("Item not found.")

    def show_all_items(self):
        """Displays all items"""
        if not self.item_list:
            print("No items available.")
        else:
            print("\nAll Items:")
            for item in self.item_list:
                print(f"- {item.name}: (ID: {item.id}, Borrowed: {'Yes' if item.borrowed else 'No'})")

    def finnish(self):
        """Saves the data to a JSON file and exits the program"""
        save_and_exit(self.item_list)





def save_and_exit(item_list):
    """Saves the data to a JSON file and exits the program"""
    with open('data.json', 'w') as json_file:
        json.dump([item.get_as_dict() for item in item_list], json_file)
    print("Data saved. Exiting program.")
    exit()

def load_data_from_file():
    try:
        open('data.json', 'x').close()
    except:
        pass    
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        return data

if  __name__ == "__main__":   
    
    while True:
        mode = input("1 to run GUI, 2 to run terminal app: ")
        if mode == "1":
            _Win = Window(load_data_from_file())
            _Win.run()
        elif mode == "2":
            app = TerminalMuseum(load_data_from_file())
            app.main_menu()
        else:
            print("Invalid choice. Please try again.")
