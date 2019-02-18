import sqlite3 as sql
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.db=sql.connect("itemdb.s3db")
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()


    def createItemNameRow(self,ri):
        self.item_NameSVar = tk.StringVar()
        self.item_NameLabel = tk.Label(self,text="Item Name:")
        self.item_NameLabel.grid(row=ri,column=0,columnspan=2,sticky=tk.W+tk.N)
        self.item_NameEntry = tk.Entry(self, textvariable=self.item_NameSVar)
        self.item_NameEntry.grid(row=ri,column=2,columnspan=2,sticky=tk.W+tk.E+tk.N)
        

    def createItemTimeRow(self,ri):
        self.item_TimeSVar = tk.StringVar()
        self.item_TimeLabel = tk.Label(self,text="Prod Time:")
        self.item_TimeLabel.grid(row=ri,column=0,columnspan=2,sticky=tk.W+tk.N)
        self.item_TimeEntry = tk.Entry(self, textvariable=self.item_TimeSVar)
        self.item_TimeEntry.grid(row=ri,column=2,columnspan=2,sticky=tk.W+tk.E+tk.N)


    def createItemButtonsRow(self,ri):
        self.item_DelItemButton = tk.Button(self, text="Delete Item", command=self.delItem)
        self.item_DelItemButton.grid(row=ri,column=0,columnspan=2,sticky=tk.N)
        
        self.item_AddItemButton = tk.Button(self, text='Add Item', command=self.addItem)
        self.item_AddItemButton.grid(row=ri,column=2,columnspan=2,sticky=tk.N)


    def createItemReqItemIDRow(self,ri):
        self.itemReq_ItemIDSVar = tk.StringVar()
        self.itemReq_ItemIDLabel = tk.Label(self,text="Item ID:")
        self.itemReq_ItemIDLabel.grid(row=ri,column=0,columnspan=2,sticky=tk.W+tk.N)
        self.itemReq_ItemIDEntry = tk.Entry(self, textvariable=self.itemReq_ItemIDSVar)
        self.itemReq_ItemIDEntry.grid(row=ri,column=2,columnspan=2,sticky=tk.W+tk.E+tk.N)


    def createItemReqReqIDRow(self,ri):
        self.itemReq_ReqIDSVar = tk.StringVar()
        self.itemReq_ReqIDLabel = tk.Label(self,text="Req ID:")
        self.itemReq_ReqIDLabel.grid(row=ri,column=0,columnspan=2,sticky=tk.W+tk.N)
        self.itemReq_ReqIDEntry = tk.Entry(self, textvariable=self.itemReq_ReqIDSVar)
        self.itemReq_ReqIDEntry.grid(row=ri,column=2,columnspan=2,sticky=tk.W+tk.E+tk.N)


    def createItemReqAmtRow(self,ri):
        self.itemReq_AmtSVar = tk.StringVar()
        self.itemReq_AmtLabel = tk.Label(self,text="Amount:")
        self.itemReq_AmtLabel.grid(row=ri,column=0,columnspan=2,sticky=tk.W+tk.N)
        self.itemReq_AmtEntry = tk.Entry(self, textvariable=self.itemReq_AmtSVar)
        self.itemReq_AmtEntry.grid(row=ri,column=2,columnspan=2,sticky=tk.W+tk.E+tk.N)


    def createItemReqButtonsRow(self,ri):
        self.itemReq_DeleteReqButton = tk.Button(self, text="Delete Req", command=self.delReq)
        self.itemReq_DeleteReqButton.grid(row=ri,column=0,columnspan=2,sticky=tk.N)
        
        self.itemReq_AddReqButton = tk.Button(self, text="Add Req", command=self.addReq)
        self.itemReq_AddReqButton.grid(row=ri,column=2,columnspan=2,sticky=tk.N)

        
    def createSciCheckboxTopRow(self,ri):
        self.calc_RedSciIVar        =  tk.IntVar()
        self.calc_RedSciCheckbox    = tk.Checkbutton(self, text="Red",variable=self.calc_RedSciIVar)
        self.calc_RedSciCheckbox.grid(row=ri,column=0,sticky=tk.W)

        self.calc_GreenSciIVar      = tk.IntVar()
        self.calc_GreenSciCheckbox  = tk.Checkbutton(self, text="Green",variable=self.calc_GreenSciIVar)
        self.calc_GreenSciCheckbox.grid(row=ri,column=1,sticky=tk.W)

        self.calc_BlueSciIVar       = tk.IntVar()
        self.calc_BlueSciCheckbox   = tk.Checkbutton(self, text="Blue",variable=self.calc_BlueSciIVar)
        self.calc_BlueSciCheckbox.grid(row=ri,column=2,sticky=tk.W)

        self.calc_GreySciIVar       = tk.IntVar()
        self.calc_GreySciCheckbox   = tk.Checkbutton(self, text="Grey",variable=self.calc_GreySciIVar)
        self.calc_GreySciCheckbox.grid(row=ri,column=3,sticky=tk.W)


    def createSciCheckboxBottomRow(self,ri):
        self.calc_PurpleSciIVar     = tk.IntVar()
        self.calc_PurpleSciCheckbox = tk.Checkbutton(self, text="Purple",variable=self.calc_PurpleSciIVar)
        self.calc_PurpleSciCheckbox.grid(row=ri,column=0,sticky=tk.W)

        self.calc_YellowSciIVar     = tk.IntVar()
        self.calc_YellowSciCheckbox = tk.Checkbutton(self, text="Yellow",variable=self.calc_YellowSciIVar)
        self.calc_YellowSciCheckbox.grid(row=ri,column=1,sticky=tk.W)

        self.calc_WhiteSciIVar      = tk.IntVar()
        self.calc_WhiteSciCheckbox  = tk.Checkbutton(self, text="White",variable=self.calc_WhiteSciIVar)
        self.calc_WhiteSciCheckbox.grid(row=ri,column=2,sticky=tk.W)


    def createItemListboxColumn(self,top,ri):
        self.item_ItemListboxSVar = tk.StringVar()
        self.item_ItemListboxYScroll = tk.Scrollbar(self,orient=tk.VERTICAL)
        self.item_ItemListboxYScroll.grid(row=top,rowspan=ri,column=5,sticky=tk.E+tk.W+tk.N+tk.S)
        self.item_ItemListbox = tk.Listbox(self,listvariable=self.item_ItemListboxSVar,yscrollcommand=self.item_ItemListboxYScroll.set)
        self.item_ItemListbox.grid(row=top,rowspan=ri,column=4,sticky=tk.N+tk.S+tk.E+tk.W)
        self.item_ItemListboxYScroll['command'] = self.item_ItemListbox.yview
        self.grid_columnconfigure(4,weight=1)


    def createItemReqListboxColumn(self,top,ri):
        self.itemReq_ReqListboxSVar = tk.StringVar()
        self.itemReq_ReqListboxYScroll = tk.Scrollbar(self,orient=tk.VERTICAL)
        self.itemReq_ReqListboxYScroll.grid(row=top,rowspan=ri,column=7,sticky=tk.E+tk.W+tk.N+tk.S)
        self.itemReq_ReqListbox = tk.Listbox(self,listvariable=self.itemReq_ReqListboxSVar,yscrollcommand=self.itemReq_ReqListboxYScroll.set)
        self.itemReq_ReqListbox.grid(row=top,rowspan=ri,column=6,sticky=tk.N+tk.S+tk.E+tk.W)
        self.itemReq_ReqListboxYScroll['command'] = self.itemReq_ReqListbox.yview
        self.grid_columnconfigure(6,weight=3)
        

    def createCalcLabRow(self,ri):
        self.calc_LabAmtSVar = tk.StringVar()
        self.calc_LabAmtLabel = tk.Label(self,text="Number of labs: ")
        self.calc_LabAmtLabel.grid(row=ri,column=0,columnspan=3,sticky=tk.W+tk.N)
        self.calc_LabAmtEntry = tk.Entry(self,textvariable=self.calc_LabAmtSVar)
        self.calc_LabAmtEntry.grid(row=ri,column=3,columnspan=1,sticky=tk.W+tk.E+tk.N)


    def createCalcTimeRow(self,ri):
        self.calc_ResearchTimeSVar = tk.StringVar()
        self.calc_ResearchTimeLabel = tk.Label(self,text="Research time per sci unit:")
        self.calc_ResearchTimeLabel.grid(row=ri,column=0,columnspan=3,sticky=tk.W+tk.N)
        self.calc_ResearchTimeEntry = tk.Entry(self,textvariable=self.calc_ResearchTimeSVar)
        self.calc_ResearchTimeEntry.grid(row=ri,column=3,columnspan=1,sticky=tk.W+tk.E+tk.N)


    def createSearchRow(self,ri):
        self.itemSearchSVar = tk.StringVar()
        self.itemSearchLabel = tk.Label(self,text="Searchbar:")
        self.itemSearchLabel.grid(row=ri,column=3,sticky=tk.E)
        self.itemSearchEntry = tk.Entry(self,textvariable=self.itemSearchSVar)
        self.itemSearchEntry.grid(row=ri,column=4,sticky=tk.E+tk.W+tk.N+tk.S)
        self.itemSearchEntry.bind('<Any-KeyRelease>',self.updateItemList)

        self.itemReqSearchSVar = tk.StringVar()
        self.itemReqSearchEntry = tk.Entry(self,textvariable=self.itemReqSearchSVar)
        self.itemReqSearchEntry.grid(row=ri,column=6,sticky=tk.E+tk.W+tk.N+tk.S)
        self.itemReqSearchEntry.bind('<Any-KeyRelease>',self.updateItemReqList)
        


    def createWidgets(self):
        self.master.title('Factorio Item Database')
        
        # resizable - this is important, tk is weird about window resizing
        # the app frame is not the root window, use winfo_toplevel() to get
        # the root window
        top=self.winfo_toplevel()
        
        top['width']=800
        top['height']=600
        top.grid_propagate(0)
        
        # rowconfigure tells the window that whatever is in row 0 (arg0)
        # should resize at a rate of 1 (arg1,'weight')
        # weight is a ratio compared to other widgets
        # widget will resize by (self.weight/total.weight) percent of total width
        # columnconfigure is rowconfigure except for columns
        
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)

        # row index
        ri=0

        # each row is tk.N stickied, with tk.W labels and tk.W+tk.E stretched widgets       
        self.createItemNameRow(ri)
        ri+=1
        self.createItemTimeRow(ri)
        ri+=1
        self.createItemButtonsRow(ri)
        ri+=1
        self.createItemReqItemIDRow(ri)
        ri+=1
        self.createItemReqReqIDRow(ri)
        ri+=1
        self.createItemReqAmtRow(ri)
        ri+=1
        self.createItemReqButtonsRow(ri)
        ri+=1
        self.createSciCheckboxTopRow(ri)
        ri+=1
        self.createSciCheckboxBottomRow(ri)
        ri+=1
        self.createCalcLabRow(ri)
        ri+=1
        self.createCalcTimeRow(ri)
        
        # expand the last row before the bottom to pad the area between the
        # row grid and the searchbar/quit button. This allows the listboxes
        # to resize without creating distance between each of the above rows.
        self.grid_rowconfigure(ri,weight=1)
        
        self.createItemListboxColumn(0,ri)
        self.createItemReqListboxColumn(0,ri)
        ri+=1

        self.createSearchRow(ri)        
        
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=ri,column=6,sticky=tk.N+tk.E)

        self.updateItemList()
        self.updateItemReqList()


    def addItem(self):
        try:
            n=self.item_NameSVar.get()
            t=self.item_TimeSVar.get()
            t=float(t)
            c=self.db.cursor()
            
            c.execute('INSERT INTO item(name,time) VALUES(?,?);',(n,t))
            c.close()
            self.db.commit()
            self.item_NameSVar.set("")
            self.item_TimeSVar.set("")
            self.updateItemList()
                 
        except Exception as e:
            print( 'delItem(): Exception occured while adding item:\n' + str(e) )


    def delItem(self):
        try:
            deltuple=self.item_ItemListbox.curselection()
            for d in deltuple:
                tgt = self.item_ItemListbox.get()
                tid = tgt.split(":")[0]
                c=self.db.cursor()
                c.execute("DELETE FROM item WHERE id=?;",(tid,))
                
            c.close()
            self.db.commit()
            self.updateItemList()
            
        except Exception as e:
            print('delItem(): Exception occured while deleting item:\n' + str(e))


    def updateItem(self):
        pass


    def addReq(self):
        try:
            rid=int(self.itemReq_ReqIDSVar.get())
            iid=int(self.itemReq_ItemIDSVar.get())
            amt=int(self.itemReq_AmtSVar.get())
            c=self.db.cursor()


            c.execute( "INSERT INTO itemReqs(itemID,reqID,amt) VALUES(?,?,?);", (iid,rid,amt)  )
            c.close()
            self.db.commit()
            self.updateItemReqList()

            
        except Exception as e:
            print("addReq(): Exception occured while adding requirement:\n" + str(e.args))
            

    def delReq(self):
        try: 
            iid=int(self.itemReq_ItemIDSVar.get())
            rid=int(self.itemReq_ReqIDSVar.get())
            amt=int(self.itemReq_AmtSVar.get())
            c=self.db.cursor()


            c.execute("DELETE FROM itemReqs WHERE itemID=? AND reqID=? AND amt=?;", (iid,rid,amt) )
            c.close()
            self.db.commit()
            self.updateItemReqList()

            
        except Exception as e:
            print("delReq(): Exception occured while deleting requirement:\n" + str(e))


    def updateItemList(self,event=None):
        try:
            c=self.db.cursor()
            searchTerm=self.itemSearchSVar.get()
            s=""
            c.execute( 'SELECT id,name,time FROM item WHERE name LIKE ? ;', ("%"+searchTerm+"%",) )
            for i in c.fetchall():
                s+=str(i[0])+":"+str(i[1].replace(" ","\ "))+":"+str(i[2])+" "

            self.item_ItemListboxSVar.set(s)
            c.close()
            
        except Exception as e:
            print("updateItemList(): Exception occured while updating lists:\n" + str(e))

            
    def updateItemReqList(self,event=None):
        try:
            c=self.db.cursor()
            searchTerm=self.itemReqSearchSVar.get()
            s=""
            c.execute('SELECT i.name,i.id,r.name,r.id,ir.amt FROM item AS r \
                      JOIN itemReqs AS ir ON r.id = ir.reqID \
                      JOIN item AS i ON i.id = ir.itemID \
                      WHERE r.name LIKE ? or i.name LIKE ? ;',
                      ( ("%"+str(searchTerm)+"%","%"+str(searchTerm)+"%") )
                      )
            for i in c.fetchall():
                for j in i:
                    s+=str(j).replace(" ","\ ")+":"
                s=s[:-1]+" "

            self.itemReq_ReqListboxSVar.set(s)
            c.close()

        except Exception as e:
            print("updateItemReqList(): Exception occured while updating lists:\n" + str(e))
            
        
    def quit(self):
        self.db.close()
        super(App,self).quit()

                                      
app = App()
app.mainloop()


