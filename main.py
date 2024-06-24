from typing import Tuple
from lib import *
import customtkinter
from CTkListbox import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class AddToStackWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Push to stack")
        self.geometry("400x400")
        self.maxsize(400, 600)
        self.buffer_result = []
        
        self.label = customtkinter.CTkLabel(self, text="Push")
        self.label.pack(padx=10, pady=10)
        
        self.id_entry = customtkinter.CTkEntry(self, placeholder_text='Custom ID:')
        self.id_entry.pack(padx=10, pady=10)
        
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text='Name:')
        self.name_entry.pack(padx=10, pady=10)
        
        self.cpf_entry = customtkinter.CTkEntry(self, placeholder_text='CPF:')
        self.cpf_entry.pack(padx=10, pady=10)
        
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text='E-mail:')
        self.email_entry.pack(padx=10, pady=10)
        
        self.btn2 = customtkinter.CTkButton(self, text="Push", command=self.push_to_stack)
        self.btn2.pack(pady=5, padx=5)
        
        self.btn3 = customtkinter.CTkButton(self, text="Clear", command=self.clear_entries)
        self.btn3.pack(pady=10, padx=10)
        
    def clear_entries(self):
        self.id_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.cpf_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        
    def push_to_stack(self):
        data = [[self.id_entry.get(), self.name_entry.get(), self.cpf_entry.get(), self.email_entry.get()]]
        if push(self.master.r, data=data) == 1:
            result = get_clients(self.master.r, 'ALL')
            if not result:
                print("Erro in the data. The list is empty.")
                self.destroy()
            for item in result:
                if item != None:
                    self.master.listbox.insert('END', item)
                    self.master.button2.configure(state='normal')
        else:
            print("failed to push")
            self.destroy()

    
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("Registers")
        self.maxsize(800, 600)
        
        self.r: Registration = create_instance()
        
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.legendLabel = customtkinter.CTkLabel(master=self.frame, compound='left', text="ID | Memory Address | Client ID | Name | CPF | E-mail", text_color='white', font=("Arial", 20))
        self.legendLabel.pack(pady=2, padx=2)

        self.listbox = CTkListbox(master=self.frame)
        self.listbox.pack(fill='both', pady=12, padx=10, expand=True)
        
        self.button = customtkinter.CTkButton(master=self.frame, text="Add", command=self.add)
        self.button.pack(pady=5, padx=10)
        
        self.button2 = customtkinter.CTkButton(master=self.frame, text="Free", command=self.free)
        self.button2.pack(pady=10, padx=10)
        
        if self.listbox.size() == 0:
            self.button2.configure(state='disabled')
        else:
            self.button2.configure(state='normal')

        self.addtostack_window = None
        
    def add(self):
        if self.addtostack_window is None or not self.addtostack_window.winfo_exists():
            self.addtostack_window = AddToStackWindow(self)
            self.addtostack_window.focus()
        else:
            self.addtostack_window.focus()
            
    def free(self):
        if self.listbox.size() != 0: # check if the listbox is empty
            print("yes")
            self.button2.configure(state='normal')
            f = freeMemory(self.r)
            if (f == 1):
                print("test")
                self.listbox.delete(0,'END')
                print("r instance: ", self.r)
                self.button2.configure(state='disabled')
            
app = App()
app.mainloop()
