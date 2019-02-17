import sqlite3 as sql
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.db=sql.connect("itemdb.s3db")
        self.createWidgets()

    def createWidgets(self):
        self.master.title('Factorio Item Database')


        
        self.itemName = tk.StringVar()
        self.itemNameLabel = tk.Label(self,text="Item Name:")
        self.itemNameLabel.grid(row=0,column=0,sticky=tk.W+tk.N)
        self.itemNameEntry = tk.Entry(self, textvariable=self.itemName)
        self.itemNameEntry.grid(row=0,column=1,sticky=tk.W+tk.E+tk.N)

        
        self.itemTime = tk.StringVar()
        self.itemNameLabel = tk.Label(self,text="Prod Time:")
        self.itemNameLabel.grid(row=1,column=0,sticky=tk.W+tk.N)
        self.itemTimeEntry = tk.Entry(self, textvariable=self.itemTime)
        self.itemTimeEntry.grid(row=1,column=1,sticky=tk.W+tk.E+tk.N)

        self.itemListvar = tk.StringVar()
        self.itemListbox = tk.Listbox(self,listvariable=self.itemListvar)
        self.itemListbox.grid(row=0,rowspan=3,column=3,sticky=tk.N+tk.E+tk.S+tk.W)

        
        self.addItemButton = tk.Button(self, text='Add Item', command=self.addItem)
        self.addItemButton.grid(row=2,column=1)
        
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=2,column=2)

        self.updateList()

    def addItem(self):
        try:
            n=self.itemName.get()
            t=self.itemTime.get()
            t=float(t)
            c=self.db.cursor()
            print("DEBUG: Inserting %s , %s" % (n, str(t)))

            
            c.execute('SELECT id FROM item WHERE name LIKE ? ;',(n,))
            l=c.fetchall()
            if len(l) > 0:
                print("Item name already found in database. Not adding duplicate.")
                return
            
            c.execute('INSERT INTO item(name,time) VALUES(?,?);',(n,t))
            self.db.commit()
            self.updateList()
                 
        except Exception as e:
            print('Exception occured while adding item:\n' + str(e) )

    def updateList(self):
        c=self.db.cursor()
        s=""
        
        c.execute('SELECT id,name,time FROM item;')
        for i in c.fetchall():
            s+=str(i[0])+":"+str(i[1].replace(" ","\ "))+":"+str(i[2])+" "

        self.itemListvar.set(s)
    def quit(self):
        self.db.close()
        super(App,self).quit()

                                      
app = App()
app.mainloop()


