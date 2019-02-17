import sqlite3 as sql
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)

        self.db=sql.connect("itemdb.s3db")
        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()


    def createWidgets(self):
        self.master.title('Factorio Item Database')
        
        
        # resizable - this is important, tk is weird about window resizing
        # the app frame is not the root window, use winfo_toplevel() to get
        # the root window
        top=self.winfo_toplevel()
        
        # rowconfigure tells the window that whatever is in row 0 (arg0)
        # should resize at a rate of 1 (arg1,'weight')
        # weight is a ratio compared to other widgets
        # columnconfigure is rowconfigure except for columns
        
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)

        # row index
        ri=0

        # item name row
        self.item_NameSVar = tk.StringVar()
        self.item_NameLabel = tk.Label(self,text="Item Name:")
        self.item_NameLabel.grid(row=ri,column=0,sticky=tk.W+tk.N)
        self.item_NameEntry = tk.Entry(self, textvariable=self.item_NameSVar)
        self.item_NameEntry.grid(row=ri,column=1,sticky=tk.W+tk.E+tk.N)
        ri+=1


        # item production time row
        self.item_TimeSVar = tk.StringVar()
        self.item_TimeLabel = tk.Label(self,text="Prod Time:")
        self.item_TimeLabel.grid(row=1,column=0,sticky=tk.W+tk.N)
        self.item_TimeEntry = tk.Entry(self, textvariable=self.item_TimeSVar)
        self.item_TimeEntry.grid(row=1,column=1,sticky=tk.W+tk.E+tk.N)
        ri+=1


        # delete, add, item buttons row
        self.item_DelItemButton = tk.Button(self, text="Delete Item", command=self.delItem)
        self.item_DelItemButton.grid(row=ri,column=0,sticky=tk.N)
        
        self.item_AddItemButton = tk.Button(self, text='Add Item', command=self.addItem)
        self.item_AddItemButton.grid(row=ri,column=1,sticky=tk.N)
        ri+=1


        # item production requirement row (itemID)
        self.itemReq_ItemIDSVar = tk.StringVar()
        self.itemReq_ItemIDLabel = tk.Label(self,text="Item ID:")
        self.itemReq_ItemIDLabel.grid(row=ri,column=0,sticky=tk.N)
        self.itemReq_ItemIDEntry = tk.Entry(self, textvariable=self.itemReq_ItemIDSVar)
        self.itemReq_ItemIDEntry.grid(row=ri,column=1,sticky=tk.W+tk.E+tk.N)
        ri+=1


        # item production requirement row (reqID)
        self.itemReq_ReqIDSVar = tk.StringVar()
        self.itemReq_ReqIDLabel = tk.Label(self,text="Req ID:")
        self.itemReq_ReqIDLabel.grid(row=ri,column=0,sticky=tk.N)
        self.itemReq_ReqIDEntry = tk.Entry(self, textvariable=self.itemReq_ReqIDSVar)
        self.itemReq_ReqIDEntry.grid(row=ri,column=1,sticky=tk.N+tk.E+tk.W)
        ri+=1


        # item production requirement row (amt)
        self.itemReq_AmtSVar = tk.StringVar()
        self.itemReq_AmtLabel = tk.Label(self,text="Amount:")
        self.itemReq_AmtLabel.grid(row=ri,column=0,sticky=tk.N)
        self.itemReq_AmtEntry = tk.Entry(self, textvariable=self.itemReq_AmtSVar)
        self.itemReq_AmtEntry.grid(row=ri,column=1,sticky=tk.N+tk.E+tk.W)
        ri+=1
        

        # delete and add requirement buttons row
        self.itemReq_DeleteReqButton = tk.Button(self, text="Delete Req", command=self.delReq)
        self.itemReq_DeleteReqButton.grid(row=ri,column=0,sticky=tk.N)
        
        self.itemReq_AddReqButton = tk.Button(self, text="Add Req", command=self.addReq)
        self.itemReq_AddReqButton.grid(row=ri,column=1,sticky=tk.N)
        ri+1


        # separator, top-anchored

        # this tells the grid to resize this row, it will expand with the window
        # which expands with the root window... if the root window doesn't resize
        # nothing else will!
        self.grid_rowconfigure(ri,weight=1)        


        # list of items in s3db
        self.item_ItemListboxSVar = tk.StringVar()
        self.item_ItemListboxYScroll = tk.Scrollbar(self,orient=tk.VERTICAL)
        self.item_ItemListboxYScroll.grid(row=0,rowspan=ri,column=4,sticky=tk.E+tk.W+tk.N+tk.S)
        self.item_ItemListbox = tk.Listbox(self,listvariable=self.item_ItemListboxSVar,yscrollcommand=self.item_ItemListboxYScroll.set)
        self.item_ItemListbox.grid(row=0,rowspan=ri+1,column=3,sticky=tk.N+tk.S)
        self.item_ItemListboxYScroll['command'] = self.item_ItemListbox.yview


        # list of item reqs in s3db
        self.itemReq_ReqListboxSVar = tk.StringVar()
        self.itemReq_ReqListboxYScroll = tk.Scrollbar(self,orient=tk.VERTICAL)
        self.itemReq_ReqListboxYScroll.grid(row=0,rowspan=ri,column=6,sticky=tk.N+tk.S)
        self.itemReq_ReqListbox = tk.Listbox(self,listvariable=self.itemReq_ReqListboxSVar,yscrollcommand=self.itemReq_ReqListboxYScroll.set)
        self.itemReq_ReqListbox.grid(row=0,rowspan=ri+1,column=5,sticky=tk.N+tk.S)
        self.itemReq_ReqListboxYScroll['command'] = self.itemReq_ReqListbox.yview
        ri+=1

        
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=ri,column=0,sticky=tk.N)

        self.updateList()


    def addItem(self):
        try:
            n=self.itemNamevar.get()
            t=self.itemTimevar.get()
            t=float(t)
            c=self.db.cursor()

            
            c.execute('SELECT id FROM item WHERE name LIKE ? ;',(n,))
            if len(c.fetchall()) > 0:
                print("addItem(): Item name already in database.")
                return
            
            c.execute('INSERT INTO item(name,time) VALUES(?,?);',(n,t))
            self.db.commit()
            self.updateList()
                 
        except Exception as e:
            print('Exception occured while adding item:\n' + str(e) )


    def delItem(self):
        try:
            tgt = self.itemListbox.get(self.itemListbox.curselection())
            tid = tgt.split(":")[0]
            c=self.db.cursor()

            
            c.execute("DELETE FROM item WHERE id=?;",(tid,))
            self.db.commit()
            self.updateList()
            
        except Exception as e:
            print('Exception occured while adding item:\n' + str(e))


    def updateItem(self):
        pass


    def addReq(self):
        try:
            rid=int(self.itemReq_ReqIDSVar.get())
            iid=int(self.itemReq_ItemIDSVar.get())
            amt=int(self.itemReq_AmtSVar.get())
            c=self.db.cursor()


            c.execute("SELECT amt FROM itemReq WHERE itemID=? AND reqID=? AND amt=?",(iid,rid,amt))
            if len(c.fetchall())>0:
                print("addReq(): Requirement relationship already in database.")
                return
            
            c.execute("INSERT INTO itemReq(itemID,reqID,amt) VALUES(?)",(iid,rid,amt))
            self.db.commit()
            self.updateList()

            
        except Exception as e:
            print("addReq(): Exception occured while adding requirement:\n" + str(e))
            

    def delReq(self):
        try: 
            iid=int(self.itemReq_ItemIDSVar.get())
            rid=int(self.itemReq_ReqIDSVar.get())
            amt=int(self.itemReq_AmtSVar.get())
            c=self.db.cursor()


            c.execute("DELETE FROM itemReq WHERE itemID=? AND reqID=? AND amt=?",(iid,rid,amt))
            self.db.commit()
            self.updateList()

            
        except Exception as e:
            print("delReq(): Exception occured while deleting requirement:\n" + str(e))


    def updateList(self):
        try:
            c=self.db.cursor()
            
            s=""
            c.execute('SELECT id,name,time FROM item;')
            for i in c.fetchall():
                s+=str(i[0])+":"+str(i[1].replace(" ","\ "))+":"+str(i[2])+" "

            self.item_ItemListboxSVar.set(s)


            s=""
            c.execute("SELECT r.name,r.id,i.name,i.id,ir.amt FROM item AS r \
                      JOIN itemReq AS ir ON r.id = ir.reqID \
                      JOIN item AS i ON i.id = ir.itemID;")
            for i in c.fetchall():
                for j in i:
                    j.replace(" ","\ ")
                    s+=str(j)+":"
                s=s[:-1]+" "

            self.itemReq.ReqListboxSVar.set(s)

            
        except Exception as e:
            print("updateList(): Exception occured while updating lists:\n" + str(e))
            
        
    def quit(self):
        self.db.close()
        super(App,self).quit()

                                      
app = App()
app.mainloop()


