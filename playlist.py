import random
import csv
import datetime
from universal_tools import search_for,playlist_write_full_csv,show_header,write_full_csv

class Playlist():
    """Ez a modul foglalkozik a lejátszási listákkal"""
    def __init__(self,file):
        self.file = file
        self.tags = self.tag_generator()

    def tag_generator(self):
        """A fileban található szenéket szétszortírozza a címkék alapján"""
        with open(self.file, 'r', encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            tags = []
            next(csvfile)
            for row in reader:
                elements = row[5].split(';')
                for element in elements:
                    if element not in tags and element:
                       tags.append(element)
                    else:
                        pass
            for tag in tags:
                if len(self.found_items(tag)) == 0:
                    pos = tags.index(tag)
                    tags.pop(pos)
        return tags

    def found_items(self,searchtag):
        """A searchtag segítségével, kikeresi az össze összes olyan zeneszámot, amiben benne
            van az a címke, listát ad vissza"""
        music = []
        index = show_header(self.file).index('tags')
        with open(self.file, 'r', encoding = 'UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            songs = []
            for row in reader:
                rows = row[index].split(';')
                if searchtag in rows :
                    songs.append(row)
                else:
                    pass
        return songs
    
    def random_music(self,found_items,choice,searchtag,address=''):
        """A funckió kigenerálja a fájlt, a paraméterek szerint,
            found_items - talált zenék, choice-mennyi zeneszámot akarunk
            searchtag-melyik címkét válaszottuk, address- a fálj útja"""
        now = datetime.datetime.now()
        playlist = []    
        random.shuffle(found_items)
        for i in range(int(choice)):
            playlist.append(found_items[i])
        if address  == '':
            adrs = now.strftime(f'{searchtag}-{choice}-%Y-%m-%d-%H-%M.lista')
        else:
            adrs  = now.strftime(f'{address}/{searchtag}-{choice}-%Y-%m-%d-%H-%M.lista')
        #print(adrs)
        playlist_write_full_csv(adrs,playlist)
        return playlist



