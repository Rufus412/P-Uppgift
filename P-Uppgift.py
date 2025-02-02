import tkinter as tk
import json


class Window():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("P-Uppgift")
        self.root.geometry("1024x1024")
        self.name_var = tk.StringVar()
        
        
    def run(self, json_data):
        canvas = tk.Canvas(self.root, width=1024, height=1024)
        canvas.place (relx=0, rely=0, anchor=tk.NW)
        entry_label = tk.Label(self.root, text = "Search for item",font = ('calibre',10,'bold'), bg = 'white', fg = 'black')
        entry = tk.Entry(self.root, textvariable = self.name_var ,font = ('calibre',10,'bold'), bg = 'white', fg = 'black')      
        entry_label.grid(row=3, column=0)
        entry.grid(row=3, column=1)
        sub_btn=tk.Button(self.root,text = 'Search', command = self.search(json_data), bg='brown', fg='white')
        sub_btn.grid(row=4, column=1)
        
        self.root.mainloop()

    def search(self, json_data):
        keyWord=self.name_var.get().strip().split(",")
        print(len(json_data['items']))
        print([x for x in filter(lambda x: x['name'] == keyWord or keyWord in x['description'] or x['context'] == keyWord or x['id'] == keyWord , data['items'])])
        #search for item



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





    _Win = Window()
    _Win.run(data)

