import subprocess
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk
def find_all_txt(path): #looking for every file .txt in system
    files = []
    for x in os.listdir(path): 
        fullpath = os.path.join(path,x) 
        if os.path.isdir(fullpath):
            files.extend(find_all_txt(fullpath))
        elif os.path.isfile(fullpath) and x.endswith(".txt"):
            files.append(x)
    return files
class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-zoomed", True)
        self.root.minsize(800,500)
        self.root.title("System Informations")
        self.choice_selected = []
        self.currdir  = os.getcwd()
        self.combo = ttk.Combobox(self.root, values=["1-Check current working direction",
                                                    "2-Check list of files in current direction",
                                                    "3-Check every .txt file name in system",
                                                    "4-Check the most using CPU and mem usage process"],
                                                    state="readonly")
        self.combo.pack(pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.selections_results)
        
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(fill="both", expand=True)

        self.lista = tk.Listbox(frame_lista,width=80, height=20)
        self.scrollbar=tk.Scrollbar(frame_lista,orient="vertical")
        
        self.lista.config(yscrollcommand=self.scrollbar.set) 
        self.scrollbar.config(command=self.lista.yview)
        
        self.lista.pack(side="left",fill="both",expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.check_files_button = tk.Button(self.root, text="check_files", command=self.open_files_window)
        self.check_files_button.pack(pady=10)
        self.check_files_button.pack_forget()
    def open_files_window(self):
        #opens a new window and displays all found .txt files. 
        new_wind = tk.Toplevel(self.root)
        new_wind.title("System Files")
        new_wind.geometry("800x500")
        lista = tk.Listbox(new_wind, width=80,height=20)
        scrollbar = tk.Scrollbar(new_wind,orient="vertical")
        lista.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=lista.yview)
        lista.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
        
        os.chdir(Path.home())
        path = os.path.abspath(os.getcwd())
        txt_files = find_all_txt(path)
        if not txt_files:
            lista.insert(tk.END,"No files found")
        else:
            i = 1
            for x in txt_files:
                lista.insert(tk.END, f"{i}: {x}")
                i+=1
    def selections_results(self,event = None):
        choice = self.combo.get()
        if choice not in self.choice_selected:
                if choice == "1-Check current working direction":
                    t = ("\n=====Working-Direction=====\n")
                    date = subprocess.check_output(["pwd"]).decode()
                    self.lista.insert(tk.END,t)
                    self.lista.insert(tk.END,date)
                elif choice =="2-Check list of files in current direction":
                    t= ("\n=====Current-dir-files=====\n")
                    os.chdir(self.currdir)
                    date = subprocess.check_output(["ls"]).decode()
                    self.lista.insert(tk.END,t)
                    self.lista.insert(tk.END,date)
                elif choice == "3-Check every .txt file name in system":
                    t= ("=====Every-system-txt-file=====\n")
                    self.lista.insert(tk.END,t)
                    self.check_files_button.pack()
                elif choice == "4-Check the most using CPU and mem usage process":
                    t= ("\n=====CPU/Mem-usage=====\n")
                    self.lista.insert(tk.END,t)
                    output = subprocess.check_output(["ps", "-eo", "pid,user,comm,%mem,%cpu", "--sort=-%cpu"]).decode()
                    for line in output.splitlines()[:11]: #returns the first 10
                        d = (f"{line}\n")
                        self.lista.insert(tk.END,d)                            
        self.choice_selected.append(choice)
    def run(self):
        self.root.mainloop()
app = Main()
app.run()