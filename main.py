import datetime
import sqlite3
# import tkcaleder
# import subprocess as s
import time
from tkinter import *
from tkinter import messagebox


class Application(Text):
    def __init__(self,
                 master):  # defined within a class causes Python to use the first parameter as a placeholder for the object
        Text.__init__(self, master)

        # heading for the main window
        self.heading = Label(master, text=" Welcome to MedKeeper ", font='arial 25 bold', fg='red')
        self.heading.place(x=200, y=0)

        # labels for medicine name, company name and date added along with expiry date
        self.medicine_name = Label(master, text="Name of the Medicine: ")

        self.company_name = Label(master, text="Company of the medicine: ")

        self.expiry_date = Label(master, text="Expiry Date: ")

        self.medic_type = Label(master, text="Medicine type: ")

        self.medic_boxes = Label(master, text="No. of boxes: ")

        self.medic_peices = Label(master, text="No. of peices: ")

        self.medicine_name.place(x=0, y=60)
        self.company_name.place(x=0, y=100)
        self.expiry_date.place(x=0, y=140)
        self.medic_type.place(x=0, y=180)
        self.medic_boxes.place(x=0, y=320)
        self.medic_peices.place(x=0, y=360)

        # entries for labels
        self.medicine = StringVar()
        self.medicine_ent = Entry(master, width=30, textvariable=self.medicine).place(x=150, y=60)

        self.companyname = StringVar()
        self.company_ent = Entry(master, width=30, textvariable=self.companyname).place(x=150, y=100)

        self.expirydate = StringVar()
        self.expiry_ent = Entry(master, width=30, textvariable=self.expirydate).place(x=150, y=140)

        self.medic_type = IntVar()
        # self.type_ent = Entry(master, width=30, textvariable=self.medic_type).place(x=150, y=180)
        self.tablet_ent = Radiobutton(master, width=5, text=" Tablet", value=1, variable=self.medic_type).place(x=50,
                                                                                                                y=205)
        self.capsule_ent = Radiobutton(master, width=5, text="Capsule", value=2, variable=self.medic_type).place(x=50,
                                                                                                                 y=225)
        self.syrup_ent = Radiobutton(master, width=5, text="  Syrup", value=3, variable=self.medic_type).place(x=50,
                                                                                                               y=245)
        self.cream_ent = Radiobutton(master, width=5, text="  Cream", value=4, variable=self.medic_type).place(x=50,
                                                                                                               y=265)
        self.powder_ent = Radiobutton(master, width=5, text=" Powder", value=5, variable=self.medic_type).place(x=50,
                                                                                                                y=285)

        self.boxes = IntVar()
        self.boxes_ent = Entry(master, width=30, textvariable=self.boxes).place(x=150, y=321)

        self.peices = IntVar()
        self.peices_ent = Entry(master, width=30, textvariable=self.peices).place(x=150, y=361)

        # button to perform  #dynamic data entry takes exa  Qctly one argument
        self.submit = Button(master, text="Add To Database", command=self.dynamic_data_entry, width=20, height=2).place(
            x=400, y=450)

        self.search = Button(master, text="Search Medicine", width=14, height=2, command=self.search_root).place(x=600,
                                                                                                                 y=450)

        self.purchase = Button(master, text="Purchase", width=14, height=2, command=self.search_root).place(x=600,
                                                                                                            y=550)

        self.quit = Button(master, text="Exit", width=14, height=2, command=master.destroy).place(x=840, y=450)

        # textbox to display updates
        self.box = Text(master, height=20, width=80)
        # self.box.focus_set()
        self.box.place(x=330, y=60)

    # Now adding the user input to database.
    global conn  # globally can access conn rather than locally
    global cursor_object
    conn = sqlite3.connect('medicines.db')
    cursor_object = conn.cursor()

    def dynamic_data_entry(self):
        # creating the database if it doesn't exist
        cursor_object.execute(
            "CREATE TABLE IF NOT EXISTS medicine_db(date_issued TEXT, medicine_name TEXT, company_name TEXT, expiry_date TEXT, medicine_type TEXT, no_of_boxes TEXT,no_of_peices TEXT, total TEXT )")

        # adding fields and values to the database
        unix = time.time()
        date_issued = str(datetime.datetime.fromtimestamp(unix).strftime(
            '%Y-%m-%d'))  # it will create a date stamp for the data inserted at that time
        medicine_name = self.medicine.get()
        company_name = self.companyname.get()
        expiry_date = self.expirydate.get()
        medicine_type = self.medic_type.get()
        # medicine_type = str(self.medic_type.get())

        if medicine_type == 1:
            medicine_type = "Tablets"

        elif medicine_type == 2:
            medicine_type = "Capsule"

        elif medicine_type == 3:
            medicine_type = "Syrup"

        elif medicine_type == 4:
            medicine_type = "Cream"

        elif medicine_type == 5:
            medicine_type = "Powder"

        medicine_type = str(medicine_type)

        no_of_boxes = self.boxes.get()
        no_of_pieces = self.peices.get()

        # if self.boxes == str() or self.peices == str():
        #     messagebox.showwarning("Please input number not string.")
        # else:
        #     pass
        if len(medicine_name) == 0 or len(company_name) == 0 or len(expiry_date) == 0 or len(
                medicine_type) == 0 or no_of_boxes == 0 or no_of_pieces == 0:
            # print("Failed. Please Fill up all the information")
            messagebox.showwarning("Failed", "Please don't leave anything blank.")
        else:
            # no_of_boxes = int(no_of_boxes)
            # no_of_packets = int(no_of_packets)

            total = no_of_pieces * no_of_boxes
            total = str(total)
            no_of_pieces = str(no_of_pieces)
            no_of_boxes = str(no_of_boxes)

            cursor_object.execute(
                "INSERT INTO medicine_db (date_issued, medicine_name, company_name, expiry_date, medicine_type , no_of_boxes ,no_of_peices, total ) VALUES (?,?, ?, ?, ? ,?, ?, ?)",
                (
                date_issued, medicine_name, company_name, expiry_date, medicine_type, no_of_boxes, no_of_pieces, total))
            conn.commit()
            self.box.insert(END, (
                    'Logs: Added \nName: ' + medicine_name.upper() + "\nCompany: " + company_name.upper() + "\nExpires at: " + expiry_date + "\nMedicine type: " + medicine_type.upper() + "\nNo. of boxes: " + no_of_boxes + "\nNo. of pieces: " + no_of_pieces + "\nTotal: " + total + "\n========================================================\n"))
            messagebox.showinfo("Success", "Successfully added to the medical database")

    # search functionality feature.
    def search_root(self):
        class Search(Text):
            def __init__(self, xpsp):
                Text.__init__(self, xpsp)

                # labels for window
                self.heading = Label(xpsp, text="Search Medicines Here.", font='arial 25 bold')
                self.heading.place(x=0, y=0)

                self.name = Label(xpsp, text="Name of the Medicine: ")
                self.name.place(x=0, y=60)
                self.name.focus_set()

                # self.entrybox

                self.search_medic_name = Entry(xpsp, width=30)
                self.search_medic_name.place(x=150, y=60)

                self.sbox = Text(xpsp, height=20, width=105)
                self.sbox.place(x=10, y=130)
                # self.sbox.focus_set()  # focus_set()
                # moves the keyboard focus to this widget.
                # This means that all keyboard events sent to the application will be routed to this widget.

                # button to perform search
                self.bt = Button(xpsp, text="Search", command=self.get_it, width=20, height=2)
                self.bt.place(x=390, y=50)

                # button to purchase medicine
                self.bt1 = Button(xpsp, text="Purchase", command=self.add_it, width=20, height=2).place(x=850, y=170)

                # button to quit
                self.qt = Button(xpsp, text="Exit", command=xpsp.destroy, width=20, height=2).place(x=850, y=270)

                #button to view all
                self.qt = Button(xpsp, text="View Medicines", command=self.view_all, width=20, height=2).place(x=850, y=370)

            # destroy button
            def master_exit(self):
                self.master.destroy()

            # button to medics

            def add_it(self):
                class Stan(Text):
                    def __init__(self, xps):
                        Text.__init__(self, xps)
                        # self.total =
                        self.ad = Label(xps, text="Purchase this medicine", font='arial 25 bold')
                        self.ad.place(x=0, y=0)

                        # info of the medic buyer
                        self.id = Label(xps, text="Name of customer", font='arial 15')
                        self.id.place(x=0, y=60)

                        self.medic_name = Label(xps, text="Name of the medicine", font='arial 15')
                        self.medic_name.place(x=0, y=100)

                        self.med_quantity = Label(xps, text="Quantity", font='arial 15')
                        self.med_quantity.place(x=0, y=160)

                        # unix = time.time()
                        # date_purchased = str(datetime.datetime.fromtimestamp(unix).strftime(
                        #     '%Y-%m-%d'))

                        self.datee = time.strftime("%x")
                        self.datee = str(datetime.datetime.strptime(self.datee, "%m/%d/%y"))

                        # entries for the info
                        self.name_of_buyer = Entry(xps, width=30)
                        self.name_of_buyer.place(x=280, y=60)

                        self.name_of_medicine = Entry(xps, width=30)
                        self.name_of_medicine.place(x=280, y=100)

                        self.med_quantity = Entry(xps, width=30)
                        self.med_quantity.place(x=280, y=160)

                        # button to make issue right
                        self.doneee = Button(xps, text="Done", width=20, height=2, command=self.done).place(x=0, y=340)
                        self.exit = Button(xps, text="Exit", width=20, height=2, command=xps.destroy).place(x=200,
                                                                                                            y=340)

                        self.logs = Text(xps, height=16, width=45)
                        self.logs.place(x=550, y=60)

                    def done(self):
                        self.buyer = self.name_of_buyer.get()
                        self.med_name = self.name_of_medicine.get()
                        self.quantity = self.med_quantity.get()
                        # self.date_bought = self.datee.get()

                        # self.available_medicine = self.total.get()

                        # conn = sqlite3.connect("medicines.db")
                        # cursor_object = conn.cursor()
                        # cursor_object.execute(
                        #     "SELECT total,medicine_name FROM medicine_db",
                        #     (self.quantity,self.med_name))
                        # conn.commit()
                        #
                        # cursor_object.execute(
                        #     "UPDATE medicine_db SET total = ? WHERE medicine_name = ?", (self.quantity, self.med_name))
                        # conn.commit()

                        if self.buyer == '' or self.med_name == '' or self.quantity == '':
                            messagebox.showwarning("Error", "Please Fill The Missing Boxes")
                            another_window = Tk()
                            another_window.geometry('1000x500')
                            another_window.resizable(False, False)
                            another_window.config(background='gray')
                            d = Stan(another_window)
                            # d = Search(Search)
                            another_window.mainloop()
                        else:

                            # conn_db = sqlite3.connect("medicines.db")
                            # cursor_object = conn.cursor()
                            # free = self.name_of_medicine.get()
                            # cursor_object.execute(
                            #     "SELECT * FROM medicine_db WHERE medicine_name LIKE ?",
                            #     (free,))
                            # conn_db.commit()
                            #
                            # if len(free) == 0:
                            #     # print("Failed. Please Fill up all the information")
                            #     messagebox.showwarning("Failed",
                            #                            "Please enter the name of the medicine you want to search.")
                            # else:
                            #     for self.row in cursor_object.fetchall():  # it put the values to listbox, fetchall() to grab all the values to the rows
                            #         if self.row == None:
                            #             messagebox.showinfo("Sorry, No such medicine found.")
                            #             self.sbox.insert(END, "No Such medicine found in the database.")
                            #         else:
                            #             # self.sbox.insert(END,"Found")
                            #             self.sbox.insert(END,
                            #                              ("Entered on: " + self.row[0].upper() + "\nName: " + self.row[
                            #                                  1].upper() + "\nCompany: " + self.row[
                            #                                   2].upper() + "\nExpires on " + self.row[
                            #                                   3] + "\nType: " + self.row[
                            #                                   4] + "\nTotal boxes: " + self.row[5] + "\nQuantity: " +
                            #                               self.row[
                            #                                   7] + "\n--------------------------------------------"))
                            #     # dynamic_data_entry()
                            #     conn_db.commit()
                            #     conn_db.close()

                            content = (
                                    self.buyer.upper() + " bought " + self.quantity + " " + self.med_name.upper() + " " + " on: " + self.datee + "\n=====================" + "\n")
                            self.logs.insert(END, content)

                            messagebox.showinfo("Successfully bought a medicine")
                            file = open(self.buyer, "w")
                            file.write(content)
                            file.close()

                another_window = Tk()
                another_window.geometry('1000x500')
                another_window.resizable(False, False)
                another_window.config(background='gray')
                d = Stan(another_window)
                # d = Search(Search)
                another_window.mainloop()



            def get_it(self):
                connect = sqlite3.connect('medicines.db')
                cursor_object = connect.cursor()
                # cursor_object.execute(
                #     "CREATE TABLE IF NOT EXISTS medicine_db(datestamp TEXT, medicine_name TEXT, company_name TEXT, expiry_date TEXT)")
                free = self.search_medic_name.get()
                # full_proof = '%' + free + '%'
                cursor_object.execute("SELECT * FROM medicine_db WHERE medicine_name LIKE ?", (free,))
                # cursor_object.execute("SELECT * FROM medicine_db WHERE medicine_name = ?", (free),)
                # data = c.fetchall()
                # print(data)
                # self.row = ''

                self.sbox.delete(0.0,'end')
                if len(free) == 0:

                    # print("Failed. Please Fill up all the information")
                    messagebox.showwarning("Failed", "Please enter the name of the medicine you want to search.")
                else:
                    # self.sbox.delete(0,END)
                    for self.row in cursor_object.fetchall():  # it put the values to listbox, fetchall() to grab all the values to the rows

                        if self.row == None:
                            # self.sbox.delete(0,'end')
                            messagebox.showinfo("Sorry, No such medicine found.")
                            self.sbox.insert(END, "No Such medicine found in the database.")
                        else:
                            # self.sbox.delete(0,'end')
                            # self.sbox.insert(END,"Found")
                            self.sbox.insert(END, ("Entered on: " + self.row[0].upper() + "\nName: " + self.row[
                                1].upper() + "\nCompany: " + self.row[2].upper() + "\nExpires on " + self.row[
                                                       3] + "\nType: " + self.row[
                                                       4] + "\nTotal boxes: " + self.row[5] + "\nQuantity: " + self.row[
                                                       7] + "\n--------------------------------------------\n"))
                    # dynamic_data_entry()
                    connect.commit()
                    connect.close()

            def view_all(self):
                print("View all")
                connect = sqlite3.connect('medicines.db')
                cursor_object = connect.cursor()
                cursor_object.execute("SELECT * FROM medicine_db")
                self.sbox.delete(0.0,'end')

                self.sbox.insert(END,
                                 "Added on     |    Name     |     Company     |     Expires on     |     Type     |    Quantity\n")
                for self.data in cursor_object.fetchall():
                    self.sbox.insert(END, self.data[0] + "\t\t" + self.data[1].upper()
                                + "\t\t" + self.data[2].upper() + "\t\t" + self.data[3] + "\t\t\t" + self.data[4].upper() + "\t\t" + self.data[7] + "\n")

                connect.commit()
                connect.close()

        search_window = Tk()
        search_window.geometry('1000x500')
        search_window.resizable(False, False)
        search_window.config(background='gray')
        cursor_object = Search(search_window)
        search_window.mainloop()


root = Tk()
root.geometry('1000x1000')
root.resizable(True, True)
root.config(background='gray')

b = Application(root)
root.mainloop()
root.mainloop()
