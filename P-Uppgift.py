import tkinter as tk


class Window():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("P-Uppgift")
        self.root.geometry("1024x1024")
        self.name_var = tk.StringVar()
        
        
    def run(self):
        canvas = tk.Canvas(self.root, width=1024, height=1024)
        canvas.place (relx=0, rely=0, anchor=tk.NW)
        entry_label = tk.Label(self.root, text = "Search for item",font = ('calibre',10,'bold'), bg = 'white', fg = 'black')
        entry = tk.Entry(self.root, textvariable = self.name_var ,font = ('calibre',10,'bold'), bg = 'white', fg = 'black')      
        entry_label.grid(row=3, column=0)
        entry.grid(row=3, column=1)
        sub_btn=tk.Button(self.root,text = 'Search', command = self.search, bg='brown', fg='white')
        sub_btn.grid(row=4, column=1)
        
        self.root.mainloop()

    def search(self):
        name=self.name_var.get().strip.split(",")
        print(name)
        #search for item



if  __name__ == "__main__": 
    _Win = Window()
    _Win.run()

