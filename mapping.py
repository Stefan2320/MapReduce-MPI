import os
import shutil
import re
import string
from collections import Counter


def createFileFromWord(directory, file_name, origin_name):


    f = open(directory + "\\" + file_name, "a")
    f.write(str(origin_name) + "|")
    f.close()


def writeProcessInFile(filename, origin_name):
    f = open(filename, "a")
    f.write(str(origin_name) + "|")
    f.close()


def mapping(nr_process, file_name):
    read_path = "test-files\\" + str(file_name)
    destination_dir = "intermediary\\" + str(nr_process)
    encoding = 'unicode_escape'
    f = open(read_path, "r",encoding=encoding)

    content_one_space = re.sub(' +', ' ', f.read().lower())
    content_one_space = re.sub('\W+\s*', ' ', content_one_space)
    content_split = content_one_space.split(" ")
    for word in content_split:
        if(word.isalpha()):
            new_file = destination_dir + "\\" + word + ".txt"
            writeProcessInFile(new_file,file_name)




def createDirectoryForProcess(nr_process):
    try:
        os.mkdir("intermediary\\" + str(nr_process))
    except Exception:
        print("Directory already exists.")


def deleteResults():
    path = r"D:\Facultate\AN_4\Sem_1\APD\Tema de casa\intermediary"
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir("intermediary")
    path = r"D:\Facultate\AN_4\Sem_1\APD\Tema de casa\output"
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir("output")
    open('result_final.txt', 'w').close()

def reduce(letter):
    directory = "intermediary\\"
    for root1, dirs1, files1 in os.walk(directory):
        for dir in dirs1:
            for root, dirs, files in os.walk(directory+"\\"+dir):
                for file in files:
                    if file.startswith(letter):
                        f2 = open(directory+"\\"+dir+"\\"+file,"r")
                        content = f2.read().replace(".txt","")
                        content = content.split("|")
                        content = list(map(int, content[:-1]))
                        freq_arr = Counter(content)
                        for item in freq_arr:
                            formatted = "("+str(item)+".txt,"+str(freq_arr[item])+"),"
                            f = open("output\\"+file,"a")
                            f.write(formatted)
                            f.close()

def make_result():
    f = open("result_final.txt","w")
    for root, dirs, files in os.walk("output"):
        for file in files:
            f.write(file[:-4]+":")
            f2 = open("output\\"+file,"r")
            content = f2.read()[:-1]+"\n\n"
            f.write(content[:-1])
            f2.close()

