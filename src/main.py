from textnode import TextNode, TextType
import os
import shutil

source_path = "static/"
target_path = "public/"


def to_public():
    #Clear target file directory
    shutil.rmtree(target_path)
    os.mkdir(target_path)

    #Get source file directory
    full_path_list = get_path(source_path)

    for full_path in full_path_list:
        target = os.path.join(target_path, full_path[7:])
        shutil.copy(full_path, target)



def get_path(path, file = None):
    if file == None:
        file_list = os.listdir(source_path)
        if len(file_list) == 0:
            return []
        else:
            return get_path(path, file_list)
    else:
        file_path = []
        for f in file:
            if os.path.isfile(os.path.join(path,f)):
                file_path.append(os.path.join(path,f))
            else:
                new_path = os.path.join(path,f)
                os.mkdir(os.path.join(target_path, new_path[7:]))
                file_path += get_path(new_path, os.listdir(new_path))
        return file_path




def main():
    to_public()

main()
