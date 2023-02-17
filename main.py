import string

from mpi4py import MPI
import os

from mapping import mapping, createDirectoryForProcess, deleteResults, writeProcessInFile, reduce, make_result

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()



print(rank)
if rank == 0:
    deleteResults()
    for dir in range(1,size):
        createDirectoryForProcess(dir)

    folder = "test-files"
    file_list = os.listdir(folder)
    file_length = len(file_list)
    file_length -= 1



    # Initializare comunicatie
    for proc in range(1, size):
        comm.send(file_list[file_length], dest=proc)
        file_length -= 1

    # trimitere mesaje (Round-robin)
    while file_length >= 0:
        source = comm.recv(source=MPI.ANY_SOURCE,status=status)
        comm.send(file_list[file_length], dest=status.Get_source())
        file_length -= 1

    alphabet = list(string.ascii_lowercase)
    len_alfa = int(len(alphabet) / (size - 1))
    parts = [alphabet[x:x + len_alfa] for x in range(0, (size - 1) * len_alfa, len_alfa)]
    for i in range((size - 1) * len_alfa, len(alphabet)):
        parts[len(parts) - 1].append(alphabet[i])

    for proc in range(1, size):
        comm.send("STOP", dest=proc)
        comm.send(parts[proc-1], dest=proc)

    ready = 0
    while ready < (size-1):
        msg = comm.recv(source=MPI.ANY_SOURCE)
        if(msg == "DONE"):
            ready+=1

    make_result()
    print("Finalizat")
else:

    message = comm.recv(source=0, status=status)
    mapping(rank,message)
    print("Am primit mesajul.Rank: ",rank)
    while message != "STOP":
        comm.send("ready", dest=0)
        message = comm.recv(source=0,status=status)
        if(message != "STOP"):
            mapping(rank,message)

    letter = comm.recv(source=0, status=status)
    print(letter)
    print("Reduce")
    for l in letter:
        reduce(l)
    print("Reduce done for ",rank)
    comm.send("DONE", dest=0)


