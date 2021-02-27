from playlist import Playlist
from universal_tools import *

class RadioManager:
    def __init__(self,name,file,rules,tags,linked_file='',linked_file_tags = ''):
        check_file(file, tags)
        if linked_file != '' and linked_file_tags != '':
            check_file(linked_file,linked_file_tags)
            self.linked_file = linked_file
        else:
            pass
        self.name = name
        self.file = file
        self.rules = rules


class EmptyObject:
    pass

