from models import *

import ctypes
import os

path = os.getcwd()
lib = ctypes.CDLL(os.path.join(path, 'lib.so'))

def get_clients(r: Registration, q: str) -> list:
    if not q or q != 'ALL':
        raise SyntaxError("The query entered is not correct. Try: [ALL].")
    if q == 'ALL':
        result: list = []
        for p in r[0].clist:
            if p:
                result.append([ctypes.addressof(p), 
                               p.contents.id, 
                               p.contents.name.decode('utf-8'), 
                               p.contents.cpf.decode('utf-8'), 
                               p.contents.email.decode('utf-8')])
            else:
                pass
    return result           

# Creates a instance of stack
def create_instance():
    try:
        instance = lib.createInstance
        instance.argtypes = []
        instance.restype = ctypes.POINTER(Registration)

        r = instance()
        return r
    except Exception as e:
        print(f"Error in {create_instance.__name__}:", e)
        exit(2)

# Push (to the top of the stack)
def push(r: Registration, data: list):
    push = lib.push
    push.argtypes = [ctypes.POINTER(Registration), 
                    ctypes.c_int,
                    ctypes.c_char_p,
                    ctypes.c_char_p, 
                    ctypes.c_char_p]

    push.restype = ctypes.c_int
    for sub in data:
        try:
            result = lib.push(r, int(sub[0]), 
                            bytes(sub[1], 'utf-8'), 
                            bytes(sub[2], 'utf-8'), 
                            bytes(sub[3], 'utf-8'))
        except ValueError:
            return 0
    if result == 0:
        return 0
    else:
        return 1

def showAlphabetic(r: Registration) -> int:
    try:
        show_regs = lib.showRegs
        show_regs.argtypes = [ctypes.POINTER(Registration)]
        show_regs.restype = None
        lib.showRegs(r)
        return 1
    except Exception:
        return 0
def freeMemory(r: Registration) -> int:
    try:
        free_mem = lib.freeMemory
        free_mem.argtypes = [ctypes.POINTER(Registration)]
        free_mem.restype = None
        lib.freeMemory(r)
        print("sucess")
        return 1
    except Exception:
        return 0