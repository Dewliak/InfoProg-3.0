from universal_tools import return_data,delete_row,return_column,add_row,search_for, edit_row,check_file
from management import RadioManager,EmptyObject
from playlist import Playlist


import management
import tkinter as tk
from tkinter import ttk
import time
from PIL import ImageTk, Image
from tkinter import filedialog


# MAIN OBJECTS 

show_time = RadioManager(name='show_time',file='data/show_time.csv',rules={'day':7,'start':24,'end':24,'show_id':return_column(file='data/shows.csv', column = 'id')},tags='id,day,start,end,show',linked_file='data/shows.csv',linked_file_tags='id,title,content,manager_id')
show = RadioManager(name='show',file='data/shows.csv',rules={'name': 50, 'content':300, 'manager_id': return_column(file='data/show_managers.csv', column='id')},tags='id,title,content,manager_id',linked_file='data/show_managers.csv',linked_file_tags='id,name,content,picture')
show_manager = RadioManager(name='manager',file='data/show_managers.csv',rules={'name': 50, 'content':300,'picture':''},tags='id,name,content,picture')
playlist = Playlist('data/zenek.csv')
empty_object = EmptyObject()


#GLOBAL OBJECtS/VARIABLES
CHOSEN_OBJECT = empty_object
CHOSEN_TAG = ''
ADDRESS = ''
BUTTON = []

#DISPLAY

window = tk.Tk()

window.title('Radio Manager')
window.iconbitmap('img/icon.ico')
window.resizable(width=False, height=False)
window.geometry('{}x{}'.format(1000,600))


frame= tk.Frame(master=window,width=800,height=500)
background_image = Image.open('img/mixer.jpg')
resized = background_image.resize((800,500),Image.ANTIALIAS)
background_img = ImageTk.PhotoImage(master=frame,image=resized)
background_image_label = tk.Label(master=frame,image=background_img)
background_image_label.place(x=0,y=0)
frame.place(x=200,y=0)
playlistframe= tk.Frame(master=frame,width=800,height=500)



# PLAYLIST

# Kinyissa a fájlböngészőt és a választott mappát az ADDRESS global változóba menti el.
def browseFiles():    
    global ADDRESS

        
    folder = ''
    folder = tk.filedialog.askdirectory()
    if len(folder) == 0:
        ADDRESS = ''
    else:
        ADDRESS = folder

            
#Gomb klassz a playlisthez
class Button():
    
    def __init__(self,text,master,master_text):
        self.var = text
        self.button = tk.Button(master=master,text=text,width=27,height=7,command=self.get)
        self.button.pack()
        self.master = master
        self.master_text = master_text
    
    def validate_playlist(self):
        value = int(PLSB.get())
        songs = list(playlist.found_items(CHOSEN_TAG))
        if value <= len(songs):
            playlist.random_music(songs,value,CHOSEN_TAG,ADDRESS)
        else:
            pass

    #vissza adja a választot értéket    
    def get(self):
        global CHOSEN_TAG
        global PLB,PLSB,PLV,BTEX

        CHOSEN_TAG = self.var
        try:
            BTEX.destroy()
            PLB.destroy()
            PLSB.destroy()
            PLV.destroy()
        except:
            pass
        BTEX= tk.Button(master=self.master_text,text = "Browse Files",width= 30, command = browseFiles)
        PLB = tk.Label(master=self.master_text,width=20,text=f'{CHOSEN_TAG} max:{len(playlist.found_items(CHOSEN_TAG))}')
        PLSB = tk.Spinbox(master=self.master_text,from_=1,to=len(playlist.found_items(CHOSEN_TAG)),width=34)
        PLV = tk.Button(text='Validate',master=self.master_text,width=30,command=self.validate_playlist)
        BTEX.pack(side=tk.LEFT)
        PLB.pack(side=tk.LEFT)
        PLSB.pack(side=tk.LEFT)
        PLV.pack(side=tk.LEFT)


# A playlist résznek a kezelő felülete
def playlist_frame(event):
    global CHOSEN_OBJECT
    global BUTTON

    CHOSEN_OBJECT = empty_object

    # Kitörli az előtte ott lévő ablakot
    try:
        box.pack_forget()
    except NameError:
        pass
    playlistframe.pack()

    #elhelyezi a megfelelő helyre az ablakot
    grid_frame = tk.Frame(master=playlistframe,width=800,height=500)
    text_frame = tk.Frame(master=playlistframe,height=25, width=500,)
    grid_frame.pack()
    #kiiratja a gombokat a megfelelő paraméterek szerint
    counter = 0
    for i in range((len(playlist.tags)//4) + 1):
        for j in range(4):
            try:
                gframe = tk.Frame(master=grid_frame,relief=tk.RAISED,borderwidth=1)
                gframe.grid(row=i, column = j)
                button = Button(playlist.tags[counter],gframe,text_frame)
                if counter == 0:
                    BUTTON.append(button)
                counter += 1
            except IndexError:
                pass
    BUTTON[0].get()
    text_frame.pack()

#FONTOSABB FUNKCIÓK


def render_picture(master,address):
    """A kép renderelésért felel, a master megadja, hogy hova, az address a kép helyét adja meg"""
    global new_pic
    my_pic = Image.open(address)
    resized = my_pic.resize((300,225),Image.ANTIALIAS)
    new_pic = ImageTk.PhotoImage(master=master,image=resized)
    my_label = tk.Label(master=master,image=new_pic)
    my_label.pack()


def deleting(event,obj):
    """Gombra működik, kitörli a válaszot tárgyat a listából"""
    data = obj.data
    if obj == empty_object:
        return
    else:
        pass
    chosen = box.curselection()
    chosen_id = int(chosen[0] + 1)
    pos = int(data[chosen_id][0])
    delete_row(obj.file,pos)
    update_data()
    make_box(event,obj)

def update_data():
    """Frissíti az adatokat"""
    obj = [show_manager,show,show_time]
    for objects in obj:
        
        objects.data = return_data(objects.file)



def add_interface(event,object,mode='add'):# add mode (add or edit
    """Az add vagy edit gombnyomáskor, ki jön egy kezelő felület, ez irányítja azt, mode meg adja hogy add vagy edit,
        az object pedig a válaszot objektum(a programban például a műsorvezetők)"""
    global add_temp
    global objects

    rules = []
    objects = []
    #ellenőrzi hogy van-e egyátalán válaszott fájl.
    if CHOSEN_OBJECT == empty_object:
        return

    #kitörli az előző ablakot, ha volt
    try:
        add_temp.destroy()
    except:
        pass
    add_temp = tk.Tk()
    add_temp.title('Radio Manager')
    add_temp.iconbitmap('img/icon.ico')
    add_temp.resizable(width=False, height=False)


    # Adatok, ami a program számára fontosak
    days = ['Monday','Tuesday',"Wednesday",'Thursday','Friday','Saturday','Sunday']
    show_id =  return_column(file=show_time.linked_file, column='id')
    manager_id = return_column(file=show.linked_file, column='id')
    show_time_id = return_column(file=show_time.file,column='id')

    
    #Kép válaszotó, vissza adja a kép helyét miután a fájl böngészőben kiválasztottuk 
    class Picture():
        def __init__(self):
            self.address = ''
        def pack(self):
            def browseFiles():
                global f_label

                folder = tk.filedialog.askopenfilenames(master = add_temp,title="Choose a picture",
                                                    filetypes=[('image files','.jpg'),
                                                               ('image files','.png'),
                                                               ('image files','.jfif')])
                try:
                    f_label.destroy()
                except:
                    pass
                f_label = tk.Label(master=add_temp,text=folder)
                f_label.pack()
                if len(folder) == 0:
                    self.address = ''
                else:
                    self.address = str(folder[0])

            file_button = tk.Button(master=add_temp,text='Open Image',command=browseFiles)
            file_button.pack()
        def get(self):
            return self.address

    # Az órát és a percet egybefoglaló widget, hogy később egy ként kezelhessük
    class HourMinute:
        def __init__(self,master):
            self.frame = tk.Frame(master=master)
            self.h_s = tk.Spinbox(self.frame,from_=0, to = 23)
            self.m_s = tk.Spinbox(self.frame,from_=0, to = 59)
            self.h_s.pack(side=tk.LEFT)
            self.m_s.pack(side=tk.LEFT)
            
        def pack(self):
            self.frame.pack()
            
        def get(self):
            hour = self.h_s.get()
            minute = self.m_s.get()
            if int(hour) > 23 or int(minute) > 59:
                return
            if len(minute) == 1:
                minute = '0'+str(minute)
            return f'{hour}:{minute}'

        def delete(self,pos,tkEND):
            self.h_s.delete(pos,tkEND)
            self.m_s.delete(pos,tkEND)
        
        def insert(self,pos,data):
            dat = data.split(':')
            self.h_s.delete(0,tk.END)
            self.h_s.insert(pos,dat[0])
            self.m_s.delete(0,tk.END)
            self.m_s.insert(pos,dat[1])
    
    
    def id_check():
        ids = [show_id,manager_id,show_time_id]
        for i in ids:
            if len(i) == 0:
                i.append('None')
            elif len(i) > 1 and i[0] == 'None':
                i.pop(0)
            else:
                pass
    id_check()

    # Létrehozza a változókat a válaszotható widgetekhez
    clicked_manager = tk.StringVar(master=add_temp)
    clicked_show = tk.StringVar(master=add_temp)
    clicked_day = tk.StringVar(master=add_temp)
    

    try:
        clicked_manager.set(manager_id[0])
        clicked_show.set(show_id[0])
        clicked_day.set(days[0])
    except IndexError:
        print('File empty')
    
    
    def change(*args,ids):
    # get
    # search row
    # give the data to the variables
    #update
        global objects
        global m_id 
        if ids == 'manager':
            m_id = manager_id_change.get()
        elif ids == 'show':
            m_id = show_id_change.get()
        elif ids == 'show_time':
            m_id = show_time_id_change.get()
        specific_row = search_for(object.file, search_tag=m_id)
        counter = 1
        for obj in objects:
            if str(obj) == 'name':
                globals()[obj].delete(0,tk.END)
                globals()[obj].insert(0,specific_row[0][counter])
            elif str(obj) == 'picture':
                copy = obj + 'copy'
                globals()[copy] = specific_row[0][counter]
                pass
            elif str(obj) == 'content':
                globals()[obj].delete('1.0',tk.END)
                globals()[obj].insert('1.0',specific_row[0][counter])
            elif str(obj) == 'manager_id':
                clicked_manager.set(specific_row[0][counter])
            elif str(obj) == 'show_id':
                pos = show_id.index(specific_row[0][counter])
                clicked_show.set(specific_row[0][counter])
            elif str(obj) == 'day':
                pos = days.index(specific_row[0][counter])
                clicked_day.set(days[pos])
            elif str(obj) == 'start' or 'end':
                globals()[obj].delete(0,tk.END)
                value = specific_row[0][counter]
                globals()[obj].insert(1,value)
            
            counter += 1
        
    
    # Változók a változó widgetek változásának figyeléséhez
    manager_id_change = tk.StringVar(master=add_temp)
    manager_id_change.trace('w',lambda *args: change(*args,ids='manager'))
    show_id_change = tk.StringVar(master=add_temp)
    show_id_change.trace('w',lambda *args: change(*args,ids='show'))
    show_time_id_change = tk.StringVar(master=add_temp)
    show_time_id_change.trace('w',lambda *args: change(*args,ids='show_time'))

    try:
        manager_id_change.set(manager_id[0])    
        show_id_change.set(show_id[0])
        show_time_id_change.set(show_time_id[0])
    except IndexError:
        print('files empty')
        

    #widget prefixumok, hogy később egyszerűbb legyen velük dolgozni
    editor_widgets = {
        "manager":tk.OptionMenu(add_temp,manager_id_change,*manager_id),
        "show":tk.OptionMenu(add_temp,show_id_change,*show_id),
        "show_time":tk.OptionMenu(add_temp,show_time_id_change,*show_time_id),
                      }
    
    prefixes = {'name': tk.Entry(master=add_temp,justify=tk.LEFT),
                'content':tk.Text(master=add_temp),
                'manager_id':tk.OptionMenu(add_temp,clicked_manager,*manager_id),
                'show_id':tk.OptionMenu(add_temp,clicked_show,*show_id),
                'day':tk.OptionMenu(add_temp,clicked_day,*days),
                'start':HourMinute(master=add_temp),
                'end':HourMinute(master=add_temp),
                'picture':Picture(),
                }

    #A hibák tárolására létrehozott
    errors = []
    Error_frame = tk.Frame(master=add_temp)
    
    def validate(event=event,object=object,mode=mode):
        """ 
            Ez a funkció foglalkozi azzal, hogy az hibákat felüntessük az add illetve edit ablakban.
            Illetve ellenőrzi, hogy a megadott adatok megfelelnek-e a kritériumoknak
        """
        print('validation...')
        def validate_time(start,end):
            """Megnézi, hogy az idő lehetséges-e, például, hogy a start később van mind az end."""
            start_m = start.split(':')
            end_m = end.split(':')
            start_v = int(start_m[0]) * 60 + int(start_m[1])
            end_v = int(end_m[0]) * 60 + int(end_m[1])
            if start_v > end_v:
                return False
            else:
                return True
            
        def time_check(day,days,check_start,check_end,start,end):
            """Ellenörzi, hogy az idők nem zavarnak be-e egymásnak"""
            # kiszámítjuk az időt percekben
            check_start_v = check_start.split(':')
            check_start_v = int(check_start_v[0]) * 60 + int(check_start_v[1])
            check_end_v = check_end.split(':')
            check_end_v = int(check_end_v[0]) * 60 + int(check_end_v[1])
            
            #végig futattjuk a már meglévő időkön, hogy nincsen-e a válaszott időnk átfedésben
            for i in range(len(start)):
                if day == days[i]:
                    start_v = start[i].split(':')
                    start_v = int(start_v[0])*60 + int(start_v[1])
                    end_v = end[i].split(':')
                    end_v = int(end_v[0])*60 + int(end_v[1])
                    if check_start_v < end_v and check_start_v > start_v:
                        return False
                    elif check_end_v > start_v and check_end_v < end_v:
                        return False
                    elif check_start_v < start_v and check_end_v > end_v:
                        return False
                    else:
                        pass
            return True        
        # kitörli az előző errorokat, ha volt.
        check = True
        data = []
        for error in errors:
            error.destroy()
            
        Error_frame.pack()
        
        try:
            Error_label.pack_forget()
        except NameError:
            pass

        #A validáló résznek ez a fő része, itt találhatóak a kritériumok, objektumokra bontva, a kritériumokat megadhatjuk az objektumban
        # így a program általánosabban használható
        for obj in objects:
            if obj == 'name':
                if len(globals()[obj].get()) <= object.rules[obj] and len(globals()[obj].get()) != 0:
                    print(f'   -{obj}....valid')
                    data.append(globals()[obj].get())
                else:
                    Error_label = tk.Label(master=Error_frame, text=f"In the name section there is no text, or the text is too long.")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                    print(f'   -{obj}....invalid')
            elif obj =='content':
                if len(globals()[obj].get('1.0',tk.END)) <= object.rules[obj] and (len(globals()[obj].get('1.0',tk.END)) - 1) != 0:  
                    print(f'   -{obj}....valid') 
                    data.append(globals()[obj].get('1.0',tk.END))
                else:
                    if len(globals()[obj].get('1.0',tk.END)) == 0:
                        Error_label = tk.Label(master=Error_frame, text=f"In the content section there is no text.")
                    else:
                        Error_label = tk.Label(master=Error_frame, text=f"In the content section the text is too long. {len(globals()[obj].get('1.0',tk.END))}")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                    print(f'   -{obj}....invalid')
            elif obj =='manager_id':
                if clicked_manager.get() == 'None':
                    Error_label = tk.Label(master=Error_frame, text=f"None is an invalid input.")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                    print(f'   -{obj}....invalid')
                else:
                    print(f'   -{obj}....valid') 
                    data.append(clicked_manager.get())
            elif obj =='show_id':
                if clicked_show.get() == 'None':
                    Error_label = tk.Label(master=Error_frame, text=f"None is an invalid input.")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                    print(f'   -{obj}....invalid')
                else:
                    print(f'   -{obj}....valid') 
                    data.append(clicked_show.get())
            elif obj == 'day':
                data.append(clicked_day.get())
            elif obj == 'start':
                data.append(globals()[obj].get())
            elif obj == 'end':
                data.append(globals()[obj].get())
                if validate_time(globals()['start'].get(),globals()['end'].get()) == False:
                    Error_label = tk.Label(master=Error_frame, text=f"Start time is higher than the end time.")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                else:
                    pass
                if time_check(clicked_day.get(),return_column(show_time.file,'day'),globals()['start'].get(),globals()['end'].get(),return_column(show_time.file,'start'),return_column(show_time.file,'end')) == False:
                    Error_label = tk.Label(master=Error_frame, text=f"The time of the show is in the period of an other show.")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                else:
                    pass
            elif obj == 'picture':
                if len(globals()[obj].get()) == 0 and mode =='edit':
                    print(f'   -{obj}....valid') 
                    data.append(globals()[obj+'copy'])
                elif len(globals()[obj].get()) == 0 and mode =='add':
                    Error_label = tk.Label(master=Error_frame, text=f"You need to add a picture")
                    Error_label.pack()
                    errors.append(Error_label)
                    check = False
                    print(f'   -{obj}....invalid')
                else:
                    print(f'   -{obj}....valid') 
                    data.append(globals()[obj].get())
            else:
                data.append(globals()[obj].get())
                print(f'   -{obj}....valid')

        # megnézi, hogy az ellenőrzés hogyan sikerült. Ha minden jó, akkor a átírja a fájlt, vagy hozzá ad a fájlhoz, attól függően, hogy milyen módban van
        if mode == 'add' and check == True:
            add_row(object.file,data)
            update_data()
            make_box(event,object)
            print(f'{mode} is valid!')
            add_temp.destroy()
        elif mode == 'edit' and check == True:
            data.insert(0,m_id)
            print(f'{mode} is valid!')
            edit_row(object.file,m_id,'line',data)
            update_data()
            make_box(event,object)
            add_temp.destroy()
        else:
            print(f"{mode} didn't made throught the validation!")
            data.clear()

    # Ez megnézi az objektum kritériumait, hogy majd azokat ellenőrizni tudjuk specifikusan
    for rule in object.rules:
        rules.append((rule,object.rules[rule]))
        globals()[rule] = prefixes[rule]
        objects.append(rule)
    if mode == 'edit':
        id_change = editor_widgets[object.name]
        id_change.pack()
    else:
        pass
    # elkészi az add interface-t vizuálisan
    for obj in objects:
        l = tk.Label(master=add_temp,text=obj)
        l.pack()
        globals()[obj].pack()

    button  = tk.Button(master=add_temp,text='Validate',command=validate)
    button.pack()


update_data()


def print_row(event,obj):
    """Ez a funkció foglalkozik azzal, hogy kiirathassuk egy ablakba a meglévő adatokat"""
    chosen = box.curselection()
    position = chosen[0] + 1
      
    temp = tk.Tk()
    temp.title('Radio Manager')
    temp.iconbitmap('img/icon.ico')
    temp.resizable(width=False, height=False)
    temp.geometry('{}x{}'.format(800,600))
    temp_frame = tk.Frame(master=temp,width=800,height=500)
    
    counter = 0
    header = []
    header.append(obj[0])
    
    # Minden adatot egy új sorban ír ki
    for i in range(len(header[0])):
        
        if header[0][i] == 'content':
            content = tk.Message(master=temp_frame,text=obj[position][i],font=('Courier',20),width=700,justify='left')
            content.pack()
        elif header[0][i] == 'picture':
            try:
                render_picture(master=temp_frame,address=obj[position][i])
            except FileNotFoundError:
                render_picture(master=temp_frame,address='img/infoprog.png')
        else:
            label =  tk.Label(master=temp,font=('Courier',20),text=f'{header[0][i]}:{obj[position][i]}')
            label.pack()
    temp_frame.pack()
    

def handler(self,event,obj):
    """A funkció segít, hogy a hogy a gomb lenyomáskor (a .bind segítségével) ne csak az event menjen át, hanem több paraméter is"""
    try:
        background_image_label.destroy()
    except:
        pass
    print(f'{obj.name}...chosen')
    return self(event,obj)



def make_box(event=0,obj=CHOSEN_OBJECT):
    """Kilistázza a fájlokban található sorokat, a megfelelő módon"""
    global CHOSEN_OBJECT
    global box
    
    CHOSEN_OBJECT = obj
    try:
        playlistframe.place(x=1000,y=0)
    except NameError:
        pass
    try:
        box.pack_forget()
    except NameError:
        pass
    
    scrollbar = tk.Scrollbar(master=frame,orient=tk.VERTICAL)
    box = tk.Listbox(master=frame,width=65,height=22,font=('Courier',15), yscrollcommand=scrollbar)
    
    scrollbar.config(command=box.yview)
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

    counter = 0
    for row in obj.data:
        if counter == 0:
            counter += 1
        else:   
            box.insert(tk.END,f'{row[0]} {row[1]}')
    obj = obj.data
    box.bind('<Double-Button>',lambda event: print_row(event,obj))
    box.pack()



#Oldalsó gombok
btn_manager = tk.Button(window, text="Manager")
btn_manager.bind("<Button-1>",lambda event: handler(self=make_box,event=event,obj=show_manager))
btn_manager.place(height=125,width=200, x=0,y=0)

btn_shows = tk.Button(window, text="Shows")
btn_shows.bind("<Button-1>",lambda event: handler(self=make_box,event=event,obj=show))
btn_shows.place(height=125,width=200, x=0, y=125)

btn_showtime = tk.Button(window, text="Shows Times")
btn_showtime.bind("<Button-1>",lambda event: handler(self=make_box,event=event,obj=show_time))
btn_showtime.place(height=125,width=200, x=0, y=250)

btn_playlist = tk.Button(window, text="Playlist")
btn_playlist.bind("<Button-1>", playlist_frame)
btn_playlist.place(height=125,width=200, x=0, y=375)


#Alsó gombok
btn_add = tk.Button(window, text="Add")
btn_add.bind("<Button-1>", lambda event: add_interface(event,CHOSEN_OBJECT))
btn_add.place(height=100,width=266, x=200, y=500)
btn_edit = tk.Button(window, text="Edit")
btn_edit.bind("<Button-1>", lambda event: add_interface(event,CHOSEN_OBJECT,'edit'))
btn_edit.place(height=100,width=266, x=466, y=500)
btn_delete = tk.Button(window, text="Delete")
btn_delete.bind("<Button-1>", lambda event: deleting(event,CHOSEN_OBJECT))
btn_delete.place(height=100,width=268, x=732, y=500)
         

# Megfelelő betűtípusra állítja a gombokat
buttons = [btn_manager,btn_shows,btn_showtime,btn_playlist,btn_add,btn_edit,btn_delete]
for button in buttons:
    button.config(font=("Courier", 20))


window.mainloop()
