import tkinter as tk
from tkinter import ttk
import json
import urllib.request

class AddButton(): 
    def __init__(self, root, text, clicked):
        self.root = root
        self.button = ttk.Button(self.root, text=text, command=clicked)

class Display(AddButton):
    def __init__(self, root, window, item):
        AddButton.__init__(self, root, None, None)
        self.photo = tk.PhotoImage(file=r'./mona-lisa.png')
        self.photoimage = self.photo.subsample(5, 5) 
        self.button = ttk.Button(self.root, text = item.name, image = self.photoimage, compound = tk.LEFT, command=lambda: window.editMode(item))
        self.item = item
        
        #window.test()


class MuseumItem():
    def __init__(self, name, description, context, id, image, borrowed, times_searched):
        self.name = name
        self.description = description
        self.context = context
        self.id = id
        self.borrowed = borrowed
        self.times_searched = times_searched
        self.image = image

    def getAsDict(self):
        return {
            'name': self.name,
            'description': self.description,
            'context': self.context,
            'id': self.id,
            'image': self.image,
            'borrowed': self.borrowed,
            'times_searched': self.times_searched
        }

    def __str__(self):
        return f"name: {self.name}, description: {self.description}, context: {self.context}, id: {self.id}, image: {self.image}, borrowed: {self.borrowed}, times_searched: {self.times_searched}"    


class RemoveButton(AddButton):
    def __init__(self, root, text, clicked):
        AddButton.__init__(self, root, text, clicked)
        self.button = ttk.Button(self.root, text='Remove', command=clicked)


class Window():
    def __init__(self, json_data):
        self.root = tk.Tk()
        self.root.title("P-Uppgift")
        self.root.geometry("300x300")
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.context_var = tk.StringVar()
        self.json_data = json_data
        self.item_list = [MuseumItem(
            item['name'],
            item['description'],
            item['context'],
            item['id'],
            item['image'],
            item['borrowed'],
            item['times_searched']
        ) for item in json_data]
        self.item_being_edited = None
        self.modeText = tk.StringVar()
        self.showBorrowed = False


        
        
    def run(self):
        canvas = tk.Canvas(self.root, width=1024, height=1024)
        canvas.place (relx=0, rely=0, anchor=tk.NW)
        
        search_label = ttk.Label(self.root, text="Search for item", font=('calibre', 10, 'bold'))
        search_label.grid(row=0, column=0)
        search_button = ttk.Button(self.root, text='Search', command=self.searchMode)
        search_button.grid(row=0, column=1)

        create_label = ttk.Label(self.root, text="Create new item", font=('calibre', 10, 'bold'))
        create_label.grid(row=1, column=0)
        create_button = ttk.Button(self.root, text='Create', command=self.createMode)
        create_button.grid(row=1, column=1)
        finnish_button = ttk.Button(self.root, text='Finnish', command=self.finnish)
        finnish_button.grid(row=2, column=1)
        self.mainMenu = [
            search_label, search_button, create_label, create_button, finnish_button
        ]
        self.currentMode = self.mainMenu



        entry_label = ttk.Label(self.root, text = "Search for item",font = ('calibre',10,'bold'))
        entry = ttk.Entry(self.root, textvariable = self.name_var ,font = ('calibre',10,'bold'))      
        entry_label.grid(row=3, column=0)
        entry.grid(row=3, column=1)
        self.show_borrowed_btn = ttk.Button(self.root, text='Show borrowed', command=lambda:self.toggleShowBorrowed())
        self.show_borrowed_btn.grid(row=3, column=2)
        sub_btn=ttk.Button(self.root,text = 'Search', command = self.search)
        back_btn=ttk.Button(self.root,text = 'Back', command = self.mainMenuMode)
        self.search_buttons = self.displayed = [entry_label, entry, sub_btn, back_btn, self.show_borrowed_btn]
        #self.searched_buttons = [entry_label, entry, sub_btn, back_btn, self.show_borrowed_btn]
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
        create_description_entry = ttk.Entry(self.root, textvariable=self.description_var, font=('calibre', 10, 'bold'))
        create_description_entry.grid(row=5, column=1)

        context_label = ttk.Label(self.root, text="Context", font=('calibre', 10, 'bold'),)
        context_label.grid(row=6, column=0)
        create_context_entry = ttk.Entry(self.root, textvariable=self.context_var, font=('calibre', 10, 'bold'))
        create_context_entry.grid(row=6, column=1)

        create_sub_btn = ttk.Button(self.root, textvariable=self.modeText, command=self.create)
        create_sub_btn.grid(row=7, column=1)
        remove_button = ttk.Button(self.root, text='Remove', command=self.remove)
        remove_button.grid(row=7, column=0)
        self.create_mode = [create_label, name_label, create_name_entry, description_label, create_description_entry, context_label, create_context_entry, create_sub_btn, remove_button]
        self.hide(self.create_mode)
        self.root.mainloop()
    
    def toggleShowBorrowed(self):
        print("toggle")
        if self.showBorrowed:
            self.show_borrowed_btn.config(text='Show borrowed')
        else:
            self.show_borrowed_btn.config(text='Hide borrowed')
        self.showBorrowed = not self.showBorrowed
        print(self.showBorrowed)
    def hide(self, widgets):
        for widget in widgets:
            widget.grid_remove()

    def show(self, widgets):
        for widget in widgets:
            widget.grid()

    def mainMenuMode(self):
        self.hide(self.currentMode)
        self.show(self.mainMenu)
        self.currentMode = self.mainMenu
        

    def searchMode(self):
        self.hide(self.currentMode)
        self.currentMode = self.search_buttons
        self.show(self.search_buttons)
        pass

    def createMode(self):
        self.modeText.set(
            "Edit" if self.item_being_edited else "Create"
        )
        self.hide(self.currentMode)
        self.show(self.create_mode)
        self.currentMode = self.create_mode
        print (self.json_data)
        pass
    

    def create(self):

        if self.item_being_edited:
            self.item_being_edited.name = self.name_var.get()
            self.item_being_edited.description = self.description_var.get().split(",")
            self.item_being_edited.context = self.context_var.get()
        else:
            new_item = MuseumItem(
                self.name_var.get(),
                self.description_var.get().split(","),
                self.context_var.get(),
                len(self.json_data) + 1,
                None,  # Assuming no image is provided during creation
                False,
                0
            )
            self.item_list.append(new_item) 
        self.item_being_edited = None
        self.name_var.set("")
        self.description_var.set("")
        self.context_var.set("")
        #clicked_item  = [x for x in filter(lambda x: x['id'] == id, self.a)][0]
        #self.json_data.up
        self.mainMenuMode()
    def addMode(self):
        pass

    def remove(self):
        if self.item_being_edited:
            self.item_list.remove(self.item_being_edited)
            self.item_being_edited = None
        self.name_var.set("")
        self.description_var.set("")
        self.context_var.set("")
        self.mainMenuMode()
    def editMode(self, item):
        self.name_var.set(item.name)
        self.description_var.set(("".join(x + "," for x in item.description)).strip(","))
        self.context_var.set(item.context)
        self.item_being_edited = item
        self.hide(self.displayed)
        self.createMode()

    def search(self):
        self.hide(self.currentMode)
        self.show(self.search_buttons)
        self.currentMode = self.search_buttons
        searchResults = []

        keyWords=self.name_var.get().split(",")
        if self.showBorrowed:
            for keyWord in keyWords:
                searchResults.append([item for item in self.item_list if keyWord in item.name or keyWord in "".join(desc for desc in item.description) or keyWord in item.context or str(item.id) == keyWord])
        else:
            for keyWord in keyWords:
                searchResults.append([item for item in self.item_list if (keyWord in item.name or keyWord in "".join(desc for desc in item.description) or keyWord in item.context or str(item.id) == keyWord) and item.borrowed])
        #search for item
        formattedResults = []
        print(searchResults)
        for listOfResults in searchResults:
            for result in listOfResults:
                formattedResults.append(result)
        print(formattedResults)
        self.formated_non_duplicate_results = list({v.id:v for v in formattedResults}.values())
        for x in self.formated_non_duplicate_results:
           x.times_searched += 1
           print(x)
        self.displaySearchResults(self.formated_non_duplicate_results)

    def displaySearchResults(self , searchResults):
        self.displayedResults = [Display(self.root, self, x) for x in searchResults]
        self.displayed = self.displayed[:5]
        print(len(self.displayedResults))
        #self.displayed = []
        self.photos = []
        for i in range(len(searchResults)):
            photo = tk.PhotoImage(file=r'./mona-lisa.png')
            photoimage = photo.subsample(5, 5)
            self.photos.append(photoimage)
            self.displayed.append(self.displayedResults[i].button)
        self.hide(self.currentMode)
        self.currentMode = self.displayed
        self.show(self.displayed)

    def finnish(self):
        self.item_list = [x.getAsDict() for x in self.item_list]
        with open('data.json', 'w') as json_file:
            json.dump(self.item_list, json_file)
        self.root.destroy()


if  __name__ == "__main__":
    try:
        open('data.json', 'x').close()
    except:
        pass    
    finally:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            #x = json.loads(data)
            #print(x)
    print('davinci' in ' davinci')

    for x in data:
        print(x)

    item_list = []

    for x in data:
        item_list.append(MuseumItem(
            x['name'],
            x['description'],
            x['context'],
            x['id'],
            x['image'],
            x['borrowed'],
            x['times_searched']
        ))

    _Win = Window(data)
    _Win.run()

