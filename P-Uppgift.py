import tkinter as tk
import json


class Display():
    def __init__(self, root):
        self.root = root
        self.photo = tk.PhotoImage(file=r'./mona-lisa.png')
        self.photoimage = self.photo.subsample(5, 5) 
        self.button = tk.Button(self.root, text = 'Click Me !', image = self.photoimage, compound = tk.LEFT)

class Button():
    def __init__(self, root, text):
        self.root = root
        self.button = tk.Button(self.root, text = 'Click Me !', image = self.photoimage, compound = tk.LEFT)

class Window():
    def __init__(self, json_data):
        self.root = tk.Tk()
        self.root.title("P-Uppgift")
        self.root.geometry("300x300")
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.context_var = tk.StringVar()
        self.json_data = json_data


        
        
    def run(self):
        canvas = tk.Canvas(self.root, width=1024, height=1024)
        canvas.place (relx=0, rely=0, anchor=tk.NW)
        
        search_label = tk.Label(self.root, text="Search for item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        search_label.grid(row=0, column=0)
        search_button = tk.Button(self.root, text='Search', command=self.searchMode, bg='brown', fg='white')
        search_button.grid(row=0, column=1)

        create_label = tk.Label(self.root, text="Create new item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        create_label.grid(row=1, column=0)
        create_button = tk.Button(self.root, text='Create', command=self.createMode, bg='brown', fg='white')
        create_button.grid(row=1, column=1)

        add_label = tk.Label(self.root, text="Add item to inventory", font=('calibre', 10, 'bold'), bg='white', fg='black')
        add_label.grid(row=2, column=0)
        add_button = tk.Button(self.root, text='Add', command=self.addMode, bg='brown', fg='white')
        add_button.grid(row=2, column=1)

        edit_label = tk.Label(self.root, text="Edit item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        edit_label.grid(row=3, column=0)
        edit_button = tk.Button(self.root, text='Edit', command=self.editMode, bg='brown', fg='white')
        edit_button.grid(row=3, column=1)

        remove_label = tk.Label(self.root, text="Remove item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        remove_label.grid(row=4, column=0)
        remove_button = tk.Button(self.root, text='Remove', command=self.removeMode, bg='brown', fg='white')
        remove_button.grid(row=4, column=1)

        self.mainMenu = [
            search_label, search_button,
            create_label, create_button,
            add_label, add_button,
            edit_label, edit_button,
            remove_label, remove_button
        ]
        self.currentMode = self.mainMenu



        entry_label = tk.Label(self.root, text = "Search for item",font = ('calibre',10,'bold'), bg = 'white', fg = 'black')
        entry = tk.Entry(self.root, textvariable = self.name_var ,font = ('calibre',10,'bold'), bg = 'white', fg = 'black')      
        entry_label.grid(row=3, column=0)
        entry.grid(row=3, column=1)
        sub_btn=tk.Button(self.root,text = 'Search', command = self.search, bg='brown', fg='white')
        back_btn=tk.Button(self.root,text = 'Back', command = self.mainMenuMode, bg='brown', fg='white')
        self.search_buttons = [entry_label, entry, sub_btn, back_btn]
        self.hide(self.search_buttons)


        #create Mode
        create_label = tk.Label(self.root, text="Create new item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        create_label.grid(row=3, column=0)

        name_label = tk.Label(self.root, text="Name", font=('calibre', 10, 'bold'), bg='white', fg='black')
        name_label.grid(row=4, column=0)
        create_name_entry = tk.Entry(self.root, textvariable=self.name_var, font=('calibre', 10, 'bold'), bg='white', fg='black')
        create_name_entry.grid(row=4, column=1)

        description_label = tk.Label(self.root, text="Description", font=('calibre', 10, 'bold'), bg='white', fg='black')
        description_label.grid(row=5, column=0)
        create_description_entry = tk.Entry(self.root, textvariable=self.description_var, font=('calibre', 10, 'bold'), bg='white', fg='black')
        create_description_entry.grid(row=5, column=1)

        context_label = tk.Label(self.root, text="Context", font=('calibre', 10, 'bold'), bg='white', fg='black')
        context_label.grid(row=6, column=0)
        create_context_entry = tk.Entry(self.root, textvariable=self.context_var, font=('calibre', 10, 'bold'), bg='white', fg='black')
        create_context_entry.grid(row=6, column=1)

        create_sub_btn = tk.Button(self.root, text='Create', command=self.create, bg='brown', fg='white')
        create_sub_btn.grid(row=7, column=1)
        self.create_mode = [create_label, name_label, create_name_entry, description_label, create_description_entry, context_label, create_context_entry, create_sub_btn]
        self.hide(self.create_mode)
        self.root.mainloop()


        #edit Mode

        
        #sub_btn.grid(row=4, column=1)
        #self.root.mainloop()
    
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
        self.hide(self.mainMenu)
        self.show(self.search_buttons)
        self.currentMode = self.search_buttons
        pass

    def createMode(self):
        self.hide(self.mainMenu)
        self.show(self.create_mode)
        self.currentMode = self.create_mode
        print (self.json_data)
        pass

    def create(self):

        new_item = {
            "name": self.name_var.get(),
            "description": self.description_var.get().split(","),
            "context": self.context_var.get(),
            "id": len(self.json_data['items']) + 1
        }
        self.name_var.set("")
        self.description_var.set("")
        self.context_var.set("")
        self.json_data['items'].append(new_item)
        self.mainMenuMode()
    def addMode(self):
        pass

    def editMode(self):
        pass
    def removeMode(self):
        pass


    def search(self):
        searchResults = []
        keyWords=self.name_var.get().split(",")
        print(f"Hi  {keyWords}")
        for keyWord in keyWords:
            searchResults.append([x for x in filter(lambda x:keyWord in x['name'] or keyWord in x['description'] or keyWord in x['context'] or x['id'] == keyWord , self.json_data['items'])])
        #search for item
        formattedResults = []
        print(searchResults)
        for listOfResults in searchResults:
            for result in listOfResults:
                formattedResults.append(result)
        print(formattedResults)
        a = list({v['id']:v for v in formattedResults}.values())
        for x in a:
           print(x)
        self.displaySearchResults(a)

    def displaySearchResults(self , searchResults):
        self.displayedResults = [Display(self.root) for x in searchResults]
        for i in range(len(searchResults)):
            self.displayedResults[i].button.grid(row=i+7, column=0)
            #self.displayedResults[i].button.bind("<Button-1>", lambda event, result=result: self.displayItem(result))


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
    
    #print([x for x in filter(lambda x: x['name'] or x['description'] or x['context'] or x['id'] == keyWord , data['items'])])

    #filtered_items = [x for x in data['items'] if "j" in x['name';'description']]

    print([x for x in data['items'] if "J" in x[key]] for key in data.keys())

    for x in data['items']:
        print(x)

    #test = ["test1", "test2", "test13"]

    #filtered_test = [x for x in test if "1" in x]
    #print(filtered_test)
    #print(filter(lambda x: "1" in x, test))





    _Win = Window(data)
    _Win.run()

