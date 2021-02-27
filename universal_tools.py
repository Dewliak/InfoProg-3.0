import csv

def check_file(file,tags):
    """Ellenörzi a fájl létezését, hga nem létezik készít egyet a megfelelő címkékkel"""
    try:
        with open(file,newline='',encoding='ISO-8859-2') as csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(csvfile)
            counter = 0
            for rows in reader:
                if counter == 0 and rows == []:
                    writer.writerow(tags + '\n')
                    counter += 1
                else:
                    pass            
    except IOError:
        with open(file,'w+',newline='',encoding='ISO-8859-2') as f:
            f.write(tags + '\n')


def check_if_length_right(string,max_length):
    """Ellenörzi két string hosszának viszonyát."""
    return len(string) <= int(max_length)


def show_header(file):
    """Vissza adja a fájl fejlécét"""
    dict_reader = csv.DictReader(open(file,'r',encoding='ISO-8859-2'))
    return dict_reader.fieldnames


def return_column(file,column):
    """Egy listában vissza ad egy specifikus oszlopot a fájlban"""
    column_data = []
    dict_reader = csv.DictReader(open(file, 'r', newline='' ,encoding='ISO-8859-2'), delimiter = ',')
    # Kikeresi az oszlopot a  fájlban
    if column in dict_reader.fieldnames:
        for row in dict_reader:
            column_data.append(row[column])
    else:
        print("The column doesn't exits")

    return column_data


def search_for(file,search_tag,specify=''):
    """Egy specifikus címke alapján keresshetünk a megadott fájlban, a search_tag meghatározza hogy mit keresünk,
        a specify alapból üres string, ekkor az egész fájlt átnézi, ha megadunk valamilyen címkét, akkor azt az
        oszlopot fogja ellenőrizni(pl név, id,...)."""

    # keresési funkció, megnézi hogy a keresett címke, benne van-e a választott elementben, True-t vagy False-t ad vissza
    def search_by_tag(x, search=str(search_tag)):
        return search in x

    with open(file, newline='', encoding = 'ISO-8859-2') as csvfile:
        found_items = []
        reader = csv.reader(csvfile,delimiter=',')
        header = next(csvfile)
        csvfile.seek(0)
        if specify != '' and specify in header:
            pos = header.index(specify)
            for row in reader:
                if str(search_tag) in str(row[pos]):
                    found_items.append(row)
                else:
                    pass
        else:
            found_items =  list(filter(search_by_tag, reader))

    return found_items


def write_full_csv(name,content):
        """Egy teljes fájlt megír a content tartalmával (ami egy lista), a name
            megadja a kívánt fájl nevét."""
        with open(name,'w',encoding='ISO-8859-2', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for elements in content:
                writer.writerow(elements)


def playlist_write_full_csv(name,content):
    """Egy teljes fájlt megír a content tartalmával (ami egy lista), a name
            megadja a kívánt fájl nevét UTF-8 kódolasban"""
    with open(name,'w',encoding='UTF-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for elements in content:
            writer.writerow(elements)


def add_row(file,content):
    """Hozzá ad egy sort a kívánt fájloz, a content egy lista"""
    with open(file, 'r+', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for rows in reader:
            pass
        id = 0
        ids = return_column(file, 'id')
        if len(ids) == 0:
            pass
        else:
            id = int(ids[-1])
        id += 1

        appender = csv.writer(csvfile)
        content.insert(0, id)
        appender.writerow(content)


def edit_row(file,id,tag,content):
    """A megadott fájlban, editálja a specifikus sort"""    
    if id == 0 or id == '0':
        print("You can't change the header.")
        return

    data = []
    specific_row = search_for(file=file, search_tag=id, specify='id')
    reader = csv.reader(open(file,'r',encoding='ISO-8859-2'))
    i = 0
    
    for row in reader: # ez a resz csunya van meg mit javitani rajta &&&
        if i == 0:
            first_row = row
            i += 1
        data.append(row)
    if tag == 'line':
        pass
    else:
        position = first_row.index(tag)
        
    writer = csv.writer(open(file, 'w', newline='', encoding='ISO-8859-2'))
    for item in data:
        if tag == 'line' and item in specific_row:
            writer.writerow(content)
        elif item in specific_row:
            item[position] = content
            writer.writerow(item)
        else:
            writer.writerow(item)


def delete_row(file,id):
    """Kitöröl egy specifikus sort a megadott fájlban"""
    if id == 0 or id == '0':
        print("You can't change the header.")
        return
    data = []
    specific_row = search_for(file=file,search_tag=str(id),specify='id')
    reader = csv.reader(open(file,'r',encoding='ISO-8859-2'))

    for row in reader:
        data.append(row)
    writer = csv.writer(open(file,'w',newline='' ,encoding='ISO-8859-2'))
    for item in data:
        if item in specific_row:
            pass
        else:
            writer.writerow(item)


# DEBUG

def return_data(file):
    data = []
    
    with open(file,'r',encoding='ISO-8859-2') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data
