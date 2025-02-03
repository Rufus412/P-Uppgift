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
        self.json_data = json_data


        
        
    def run(self):
        canvas = tk.Canvas(self.root, width=1024, height=1024)
        canvas.place (relx=0, rely=0, anchor=tk.NW)
        
        self.search_label = tk.Label(self.root, text="Search for item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        self.search_label.grid(row=0, column=0)
        self.search_button = tk.Button(self.root, text='Search', command=self.searchMode, bg='brown', fg='white')
        self.search_button.grid(row=0, column=1)

        self.create_label = tk.Label(self.root, text="Create new item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        self.create_label.grid(row=1, column=0)
        self.create_button = tk.Button(self.root, text='Create', command=self.createMode, bg='brown', fg='white')
        self.create_button.grid(row=1, column=1)

        self.add_label = tk.Label(self.root, text="Add item to inventory", font=('calibre', 10, 'bold'), bg='white', fg='black')
        self.add_label.grid(row=2, column=0)
        self.add_button = tk.Button(self.root, text='Add', command=self.addMode, bg='brown', fg='white')
        self.add_button.grid(row=2, column=1)

        self.edit_label = tk.Label(self.root, text="Edit item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        self.edit_label.grid(row=3, column=0)
        self.edit_button = tk.Button(self.root, text='Edit', command=self.editMode, bg='brown', fg='white')
        self.edit_button.grid(row=3, column=1)

        self.remove_label = tk.Label(self.root, text="Remove item", font=('calibre', 10, 'bold'), bg='white', fg='black')
        self.remove_label.grid(row=4, column=0)
        self.remove_button = tk.Button(self.root, text='Remove', command=lambda: self.hide(self.remove_label), bg='brown', fg='white')
        self.remove_button.grid(row=4, column=1)

        self.mainMenu = [
            [self.search_label, self.search_button],
            [self.create_label, self.create_button],
            [self.add_label, self.add_button],
            [self.edit_label, self.edit_button],
            [self.remove_label, self.remove_button]
        ]
        self.currentMode = self.mainMenu
        self.entry_label = tk.Label(self.root, text = "Search for item",font = ('calibre',10,'bold'), bg = 'white', fg = 'black')
        self.entry = tk.Entry(self.root, textvariable = self.name_var ,font = ('calibre',10,'bold'), bg = 'white', fg = 'black')      
        #entry_label.grid(row=3, column=0)
        #entry.grid(row=3, column=1)
        self.sub_btn=tk.Button(self.root,text = 'Search', command = self.search, bg='brown', fg='white')
        self.back_btn=tk.Button(self.root,text = 'Back', command = self.mainMenuMode, bg='brown', fg='white')
        self.search_buttons = [[self.entry_label, self.entry], [self.sub_btn], [self.back_btn]]
        self.root.mainloop()
        
        #sub_btn.grid(row=4, column=1)
        #self.root.mainloop()
    
    def hide(self, widget):
        widget.grid_remove()

    def show(self, widget):
        widget.grid()

    def mainMenuMode(self):
        for widget in self.currentMode:
            for w in widget:
                self.hide(w)
        for widget in self.mainMenu:
            for w in widget:
                self.show(w)
        

    def searchMode(self):
        for widget in self.mainMenu:
            for w in widget:
                self.hide(w)
        for widget in self.search_buttons:
            for w in widget:
                self.show(w)
        self.currentMode = self.search_buttons
        pass

    def createMode(self):
        for widget in self.mainMenu:
            for w in widget:
                self.hide(w)

        pass

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

