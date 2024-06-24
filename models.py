import ctypes
import os

ALPHA = 26

class Client(ctypes.Structure):
    pass

Client._fields_ = [("id", ctypes.c_int),
                ("name", ctypes.c_char_p),
                ("cpf", ctypes.c_char_p),
                ("email", ctypes.c_char_p),
                ("next", ctypes.POINTER(Client))]

  
class Registration(ctypes.Structure):
    _fields_ = [("clist", ctypes.POINTER(Client) * ALPHA)]
    