import tkinter as tk
from tkinter import ttk
import pickle
from tkinter.scrolledtext import ScrolledText


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Calculator')
        self.geometry('400x200')

        self.entry_text = tk.StringVar()
        self.ent = ttk.Entry(self, textvariable=self.entry_text)
        self.ent.grid(row=0, column=1, columnspan=2)

        self.counter_ = 0
        self.history = self.load_hist_file()
        self.buttons_init()

    def set_value(self, ans: str):
        self.entry_text.set(ans)

    def clear_value(self):
        self.entry_text.set("")

    def add_value(self, inp):
        check_lst = ["+", "-", "/", "*", "."]
        try:
            current = self.entry_text.get()
            if current[0] == "-":
                current = current[1:]
            if "+" in current or "-" in current or "*" in current or "/" in current:
                if current[-1] in check_lst[:-1] and inp in check_lst[:-1]:
                    current = self.entry_text.get()
                    new = current[:-1]+inp
                    self.set_value(new)

                elif inp in check_lst[:-1]:
                    self.process()
                    self.add_value(inp)
                else:
                    current = self.entry_text.get()
                    new = current+inp
                    self.set_value(new)
            else:
                current = self.entry_text.get()
                new = current+inp
                self.set_value(new)
        except Exception as e:
            if inp not in check_lst:
                current = self.entry_text.get()
                new = current+inp
                self.set_value(new)

    def buttons_init(self):
        btn_dict = {'3': ["3", 3, 2],
                    '2': ["2", 3, 1],
                    '1': ["1", 3, 0],
                    '6': ["6", 2, 2],
                    '5': ["5", 2, 1],
                    '4': ["4", 2, 0],
                    '9': ["9", 1, 2],
                    '8': ["8", 1, 1],
                    '7': ["7", 1, 0],
                    '0': ["0", 4, 0],
                    '.': ["dot", 4, 1],
                    'C': ["clear", 0, 3],
                    '+': ["add", 1, 3],
                    '-': ["sub", 2, 3],
                    '/': ["div", 3, 3],
                    '*': ["mul", 4, 3],
                    '=': ["eql", 4, 2],
                    'history': ["history", 0, 0]}
        for btn, dets in btn_dict.items():
            exec(f"self.button_{dets[0]} = ttk.Button(self, text='{btn}')")
            if btn == "history":
                exec(
                    f"self.button_{dets[0]}['command'] =self.button_history_clicked")
            elif btn == "C":
                exec(
                    f"self.button_{dets[0]}['command'] =self.clear_value ")
            elif btn == "=":
                exec(
                    f"self.button_{dets[0]}['command'] =self.process ")
            else:
                exec(
                    f"self.button_{dets[0]}['command'] =lambda: app.add_value('{btn}') ")
            exec(
                f"self.button_{dets[0]}.grid(row ={dets[1]}, column = {dets[2]})")

    def save_history(self, data, ans):
        self.history[data] = ans
        self.save_hist_file()

    def save_hist_file(self):
        with open('history.pickle', 'wb') as handle:
            pickle.dump(self.history, handle)

    def load_hist_file(self):
        try:
            with open('history.pickle', 'rb') as handle:
                a = pickle.load(handle)
            return a
        except FileNotFoundError:
            return dict()

    def process(self):
        data = self.entry_text.get()
        ans = 0
        if "+" in data:
            lst = data.split("+")
            ans = float(lst[0])+float(lst[1])
            self.set_value(ans)
            self.save_history(data, ans)
        elif data[0] != "-" and "-" in data:
            lst = data.split("-")
            ans = float(lst[0])-float(lst[1])
            self.set_value(ans)
            self.save_history(data, ans)
        elif data[0] == "-" and "-" in data[1:]:
            lst = data[1:].split("-")
            ans = (-float(lst[0]))-float(lst[1])
            self.set_value(ans)
            self.save_history(data, ans)
        elif "*" in data:
            lst = data.split("*")
            ans = float(lst[0])*float(lst[1])
            self.set_value(ans)
            self.save_history(data, ans)
        elif "/" in data:
            lst = data.split("/")
            ans = float(lst[0])/float(lst[1])
            self.set_value(ans)
            self.save_history(data, ans)
        else:
            self.set_value(data)

    def button_history_clicked(self):
        hist = Show_history()
        hist.mainloop()


class Show_history(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Calculator History')
        self.geometry('200x200')

        self.show_data = ScrolledText(self, height=5)
        self.show_data.place(relx=0, relwidth=1, relheight=1, rely=0)
        self.history = self.load_hist_file()
        for i, j in self.history.items():
            self.add_info(i, j)

    def load_hist_file(self):
        try:
            with open('history.pickle', 'rb') as handle:
                a = pickle.load(handle)
            return a
        except FileNotFoundError:
            return dict()

    def add_info(self, data, ans):
        text = str(data)+"="+str(ans)+"\n"
        self.show_data.insert(tk.END, text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
