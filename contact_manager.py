import json
import tkinter
import re
import datetime
from tkinter import messagebox, filedialog
from typing import List


def end_program(window: tkinter.Tk):
    # End the main loop and exit the window
    global run_loop
    if messagebox.askyesno("Exit", "Do you want to quit the application?"):
        window.destroy()
        run_loop = False


def cntct_import(search_var: tkinter.StringVar, filename: str, new_filename: str):
    # Get contacts from different file imported into current file
    if new_filename == filename:
        return messagebox.showerror('Default load', 'Default/Previous file was laoded')
    if not file_check(new_filename):
        return messagebox.showerror('Invalid File', 'File you selected is invalid or has invalid values')
    if new_filename[-5:] == '.json':
        with open(filename, 'r') as data:
            data = json.load(data)
        with open(new_filename, 'r') as new_data:
            new_data = json.load(new_data)
            for i in new_data:
                data.append(i)
        with open(filename, 'w') as old_data:
            json.dump(data, old_data)
    elif filename[-4:] == '.vcf' or filename[-6:] == '.vcard':
        with open(filename, 'r') as data:
            data = json.load(data)
        with open(new_filename, 'r') as new_data:
            new_data = json.load(new_data)
        # TODO
    for i in data:
        brth_today_chck(i)
    cntct_load(search_var, filename)


def cntct_load(search_var: tkinter.StringVar, filename: str):
    # Load contacts onto screen with search parameter
    global cntct_list
    search = search_var.get()
    cntct_list.delete(0, cntct_list.index('end'))
    with open(filename, 'r') as data:
        data = json.load(data)
        for i in data:
            if search in i['name'] or search == '':
                cntct_list.insert(cntct_list.index('end'), i['name'])
    return True


def cntct_save(search_var: tkinter.StringVar, filename: str, possition: str):
    # Update or Add contact to file
    search = search_var.get()
    data_possition = -1
    if brth_chck(line_brth.get()) or email_chck(line_email.get()) or phone_chck(line_tel.get()):
        return
    new_contact = {'name': line_name.get(),
                   'brth': line_brth.get(),
                   'email': line_email.get(),
                   'tel': line_tel.get(),
                   'note': line_note.get()}
    if possition == ():
        possition = None
    else:
        possition = int(possition[0])
    with open(filename, 'r') as data:
        if filename[-5:] == '.json':
            try:
                data = json.load(data)
                if possition is None:
                    data.append(new_contact)
                for i in range(len(data)):
                    if search in data[i]['name'] or search == '':
                        data_possition += 1
                        if data_possition == possition:
                            data[i] = new_contact
                            break
            except:
                data = [new_contact]
    with open(filename, 'w') as saving:
        if filename[-5:] == '.json':
            json.dump(data, saving)
    cntct_load(search_var, filename)
    if possition is not None:
        cntct_list.select_set(possition)


def cntct_del(search_var: tkinter.StringVar, filename: str, possition: tuple):
    # Delete contact
    possition = int(possition[0])
    data_possition = -1
    search = search_var.get()
    with open(filename, 'r') as data:
        if filename[-5:] == '.json':
            data = json.load(data)
            for i in range(len(data)):
                if search in data[i]['name'] or search == '':
                    data_possition += 1
                    if data_possition == possition:
                        data.pop(i)
                        break
    with open(filename, 'w') as saving:
        if filename[-5:] == '.json':
            json.dump(data, saving)
    del_values()
    cntct_load(search_var, filename)


def cntct_add():
    # Deselect contact to add a new
    global search_var
    cntct_list.select_clear(0, cntct_list.index('end'))
    del_values()
    search_var.set('')
    cntct_load(search_var, filename)


def cntct_edit_line(possition: List, name: str):
    # Create info lines
    lbl = tkinter.Label(window, text=name)
    lbl.grid(row=possition[0], column=possition[1], sticky='e')
    entr = tkinter.Entry(window)
    entr.grid(row=possition[0], column=possition[1]+1)
    return lbl, entr


def del_values():
    # Clear info Values
    line_name.delete(0, len(line_name.get()))
    line_brth.delete(0, len(line_brth.get()))
    line_email.delete(0, len(line_email.get()))
    line_tel.delete(0, len(line_tel.get()))
    line_note.delete(0, len(line_note.get()))


def order_ascending(filename: str):
    # Order file ascending
    with open(filename, 'r') as data:
        data = json.load(data)
    data = sorted(data, key=lambda d: d['name'])
    with open(filename, 'w') as old_data:
        json.dump(data, old_data)
    cntct_load(search_var, filename)
    del_values()


def order_descending(filename: str):
    # Order file descending
    with open(filename, 'r') as data:
        data = json.load(data)
    data = sorted(data, key=lambda d: d['name'], reverse=True)
    with open(filename, 'w') as old_data:
        json.dump(data, old_data)
    cntct_load(search_var, filename)
    del_values()


def update_values(event):
    # Write out selected conctact
    search = search_var.get()
    del_values()
    reduced_data = []
    if cntct_list.curselection() == ():
        return
    with open(filename) as data:
        data = json.load(data)
        for i in data:
            if search in i['name'] or search == '':
                reduced_data.append(i)
    line_name.insert(0, reduced_data[cntct_list.curselection()[0]]['name'])
    line_brth.insert(0, reduced_data[cntct_list.curselection()[0]]['brth'])
    line_email.insert(0, reduced_data[cntct_list.curselection()[0]]['email'])
    line_tel.insert(0, reduced_data[cntct_list.curselection()[0]]['tel'])
    line_note.insert(0, reduced_data[cntct_list.curselection()[0]]['note'])


def savelocation(in_filename: str):
    # Set new save location
    global filename
    if messagebox.askquestion('Set new save file', 'Set your new .json file?') == 'yes':
        new_filename = filedialog.askopenfilename()
        if file_check(new_filename):
            try:
                with open(new_filename, 'r') as data:
                    data = json.load(data)
                    for i in data:
                        brth_today_chck(i)
            except:
                with open(new_filename, 'w') as data:
                    json.dump([], data)
            filename = new_filename
            cntct_load(search_var, filename)
            return
        else:
            messagebox.showerror('Invalid File', 'File you selected is invalid or has invalid values\nSetting default file')
    else:
        messagebox.showerror('Default load', 'Default/Previous file was laoded')
    try:
        with open(in_filename, 'r') as data:
            data = json.load(data)
            for i in data:
                brth_today_chck(i)
    except:
        with open(in_filename, 'w') as data:
            json.dump([], data)
    filename = in_filename
    cntct_load(search_var, filename)
    return


def file_check(filename: str):
    # Check if selected file has propper values
    valid = True
    if filename[-5:] == '.json':
        with open(filename, 'r') as data:
            data = json.load(data)
            if type(data) == list:
                for i in data:
                    if type(i) == dict:
                        if set(i.keys()) == keylist:
                            if i['name'] == '' or brth_chck(i['brth']) or email_chck(i['email']) or phone_chck(i['tel']):
                                valid = False
                        else:
                            valid = False
                    else:
                        valid = False
            else:
                valid = False
    elif filename[-5:] == 'vcard':
        with open(filename, 'r') as data:
            pass
        # TODO
    else:
        valid = False
    return valid


def brth_today_chck(person: dict):
    # Check if contact has birthday today
    if datetime.date.today().strftime('%d-%m') == person['brth'][:5]:
        messagebox.showinfo('Happy Birthday', 'Today has {} birthday'.format(person['name']))


def email_chck(email: str):
    # Check email value
    regex = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
    if re.fullmatch(regex, email) or email == '':
        return False
    messagebox.showerror('Invalid Value', 'Invalid Email\nformat name@domain.something')
    return True


def phone_chck(phone: str):
    # Check tel value
    phone = phone.replace(' ', '')
    if phone == '':
        return False
    elif phone.isdigit() or (phone[0] == '+' and phone[1:].isdigit()):
        return False
    messagebox.showerror('Invalid Value', 'Invalid Telephone Number\nformat with +00000.. or 00000..')
    return True


def brth_chck(date: str):
    # Check date value
    regex = '[0-3][0-9][-][0-1][0-9][-][0-9][0-9][0-9][0-9]'
    if re.fullmatch(regex, date) or date == '':
        return False
    messagebox.showerror('Invalid Value', 'Invalid Birth Date\nformat dd-mm-yyyy')
    return True


def visible_values():
    # Window to toggle visible values
    pop_window = tkinter.Toplevel()
    pop_window.title('Visible Information')
    tkinter.Checkbutton(pop_window, text='Brith Date', command=lambda: check_change(lbl_brth, line_brth, pos_brth, active_brth), variable=active_brth).grid(row=0, column=0, sticky='w')
    tkinter.Checkbutton(pop_window, text='Email', command=lambda: check_change(lbl_email, line_email, pos_email, active_email), variable=active_email).grid(row=1, column=0, sticky='w')
    tkinter.Checkbutton(pop_window, text='Telephone', command=lambda: check_change(lbl_tel, line_tel, pos_tel, active_tel), variable=active_tel).grid(row=2, column=0, sticky='w')
    tkinter.Checkbutton(pop_window, text='Note', command=lambda: check_change(lbl_note, line_note, pos_note, active_note), variable=active_note).grid(row=3, column=0, sticky='w')
    tkinter.Button(pop_window, text='Exit', command=lambda: pop_window.destroy()).grid(row=4, column=0)


def check_change(lbl: tkinter.Label, entry: tkinter.Entry, pos: List, var: tkinter.IntVar):
    # Add or Remove info bar
    if var.get() == 0:
        lbl.grid_remove()
        entry.grid_remove()
    else:
        lbl.grid(row=pos[0], column=pos[1], sticky='e')
        entry.grid(row=pos[0], column=pos[1]+1)


# Spawn main window
window = tkinter.Tk()
window.geometry('400x400')
window.title('Správce kontaktu')
window.protocol('WM_DELETE_WINDOW', lambda: end_program(window))

# Variables
run_loop = True
keylist = {'name', 'brth', 'email', 'tel', 'note'}

active_brth = tkinter.IntVar()
active_brth.set(1)
active_email = tkinter.IntVar()
active_email.set(1)
active_tel = tkinter.IntVar()
active_tel.set(1)
active_note = tkinter.IntVar()
active_note.set(1)

pos_brth, pos_email, pos_tel, pos_note = [3, 1], [4, 1], [5, 1], [6, 1]

# Search line
search_var = tkinter.StringVar()
line_search = tkinter.Entry(window, textvariable=search_var)
line_search.grid(row=0, column=0)
search_var.trace('w', lambda a, b, c: cntct_load(search_var, filename))
lbl_search = tkinter.Label(window, text='Search')
lbl_search.grid(row=0, column=1, sticky='w')

# Contacts
cntct_list = tkinter.Listbox(window)
cntct_list.grid(row=1, column=0)
cntct_list.bind('<<ListboxSelect>>', update_values)

# Left Buttons
btn_add = tkinter.Button(window, text='New Contact', command=lambda: cntct_add())
btn_add.grid(row=2, column=0)

btn_imprt = tkinter.Button(window, text='Import Contacts', command=lambda: cntct_import(search_var, filename, filedialog.askopenfilename()))
btn_imprt.grid(row=3, column=0)

btn_savelctn = tkinter.Button(window, text='Set New Save Location', command=lambda: savelocation(filename))
btn_savelctn.grid(row=4, column=0)

btn_order_up = tkinter.Button(window, text='Order Ascending', command=lambda: order_ascending(filename))
btn_order_up.grid(row=5, column=0)
btn_order_down = tkinter.Button(window, text='Oder Descending', command=lambda: order_descending(filename))
btn_order_down.grid(row=6, column=0)

btn_visible = tkinter.Button(window, text='Visible Values', command=lambda: visible_values())
btn_visible.grid(row=7, column=0)

# Info lines
lbl_name, line_name = cntct_edit_line([2, 1], 'Name:')
lbl_brth, line_brth = cntct_edit_line(pos_brth, 'Birth Date:')
lbl_email, line_email = cntct_edit_line(pos_email, 'Email:')
lbl_tel, line_tel = cntct_edit_line(pos_tel, 'Telephone Number:')
lbl_note, line_note = cntct_edit_line(pos_note, 'Note:')

# Right Buttons
btn_save = tkinter.Button(window, text='Save Contact', command=lambda: cntct_save(search_var, filename, cntct_list.curselection()), state=tkinter.DISABLED)
btn_save.grid(row=1, column=1, sticky='se')

btn_del = tkinter.Button(window, text='Delete Contact', command=lambda: cntct_del(search_var, filename, cntct_list.curselection()), state=tkinter.DISABLED)
btn_del.grid(row=1, column=2, sticky='sw')

btn_end = tkinter.Button(window, text='Exit', command=lambda: end_program(window))
btn_end.grid(row=0, column=2, sticky='e')

filename = 'kontakty.json'
savelocation(filename)
cntct_load(search_var, filename)

# Main program loop
while run_loop:
    if line_name.get() != '':
        btn_save['state'] = tkinter.NORMAL
    else:
        btn_save['state'] = tkinter.DISABLED
    if cntct_list.curselection() != ():
        btn_del['state'] = tkinter.NORMAL
    else:
        btn_del['state'] = tkinter.DISABLED
    window.update()
