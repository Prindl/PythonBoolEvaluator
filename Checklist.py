import tkinter as tk
import types

class CheckListbox(tk.Listbox):
    mark = "\u2713"#python 2 unicode add u"blabla"
    spacing = "   "
    def __init__(self, parent, adv_browse, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adv_browse = adv_browse #to activate modified browse
        self.bind("<<ListboxSelect>>", self.select_item)
        self.bind("<ButtonPress-1>", self.start_selection)
        self.bind("<Double-Button-1>", self.cancel_event)
        self.bind("<Triple-Button-1>", self.cancel_event)
        self.bind("<ButtonRelease-1>", self.end_selection)
        self.last_selection = set()
        self.last_index = None
        self.mode = kwargs["selectmode"]

    def cancel_event(self, event):
        return "break"

    def end_selection(self, event):
        if self.mode == tk.EXTENDED:
            selection = self.curselection()
            for i in selection:
                text = self.get(i).strip()
                self.delete(i)
                if text[0] == self.mark:
                    self.insert(i, self.spacing + text)
                else:
                    self.insert(i, self.mark + text)
                    self.last_selection.add(i)
                    self.selection_set(i)
            self.activate(selection[-1])
        elif self.mode == tk.SINGLE:
            self.activate(self.last_index)
            return "break"

    def start_selection(self, event):
        if self.mode == tk.SINGLE:
            #mouse is pressed clear prev selection
            if self.last_index != None:
                text = self.get(self.last_index).strip()
                if self.mark == text[0]:
                    self.delete(self.last_index)
                    self.insert(self.last_index, self.spacing + text[1:])
        elif self.mode == tk.EXTENDED:
            #mouse is pressed clear prev selection
            for i in self.last_selection:
                text = self.get(i).strip()
                self.selection_clear(i, i)
                self.delete(i)
                self.insert(i, self.spacing + text[1:])
            self.last_selection = set()
                

    def select_item(self, event):
        selection = self.curselection()
        if self.mode == tk.SINGLE:
            index = selection[0]
            text = self.get(index).strip()
            self.delete(index)
            self.last_index = index
            self.insert(index, self.mark + text)
            self.selection_set(index)
        elif self.mode == tk.MULTIPLE:
            index = (self.last_selection ^ set(selection)).pop()
            text = self.get(index).strip()
            self.delete(index)
            if self.mark == text[0]:
                self.insert(index, self.spacing + text[1:])
                self.last_selection.remove(index)
            else:
                self.insert(index, self.mark + text)
                self.last_selection.add(index)
                self.selection_set(index)
        elif self.mode == tk.BROWSE:
            if self.adv_browse:
                index = selection[0]  
                text = self.get(index).strip()
                self.delete(index)
                if self.mark == text[0]:
                    self.insert(index, self.spacing + text[1:])
                    self.last_selection.remove(index)
                else:
                    self.insert(index, self.mark + text)
                    self.last_selection.add(index)
                for i in self.last_selection:
                    self.selection_set(i)
                self.activate(index)
                self.last_index = index
            else: # ORIGINAL BROWSE - only one selection at a time
                index = selection[0]
                if self.last_index != None:
                    text = self.get(self.last_index).strip()
                    if self.mark == text[0]:
                        self.delete(self.last_index)
                        self.insert(self.last_index, self.spacing + text[1:])
                text = self.get(index).strip()
                self.delete(index)
                self.insert(index, self.mark + text)
                self.selection_set(index)
                self.activate(index)
                self.last_index = index

    def insert_with_space(self, index, text):
        self.insert(index, self.spacing + text)

    def get_selected_items(self, text_mode):
        if self.mode == tk.SINGLE or self.mode == tk.BROWSE and not self.adv_browse:
            if text_mode:
                return self.get(self.last_index)[1:]
            else:
                return self.last_index
        else:
            if text_mode:
                return (self.get(x)[1:] for x in self.last_selection)
            else:
                return (x for x in self.last_selection)

class MainApplication(tk.Frame):
    def __init__(self, parent, list_of_items, selection, text_mode = True, mode = tk.BROWSE):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        tk.Button(parent, text = "Submit", command = self.save_selection).pack(anchor = tk.CENTER)
        #supports tk.SINGLE, tk.MULTIPLE, tk.BROWSE, tk.EXTENDED
        self.container = CheckListbox(parent, True, height = 150, width = 150, selectmode = mode)
        self.container.pack(fill = tk.BOTH, expand = 1)
        self.selection = selection
        self.text_mode = text_mode
        for i,item in enumerate(list_of_items):
            self.container.insert_with_space(i, "{}".format(item))

    def save_selection(self):
        items = self.container.get_selected_items(self.text_mode)
        if isinstance(items, types.GeneratorType):
            self.selection += items
        else:
            self.selection.append(items)
        self.selection.sort()
        self.parent.destroy()

def open_selection_box(list_of_items, text_mode = True, mode = tk.BROWSE, width = 200, height = 400):
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.minsize(100, 400)
    root.maxsize(300, 600)
    root.geometry("{0}x{1}".format(width, height))
    selection = []
    MainApplication(root, ("%s"%item for item in list_of_items), selection, text_mode, mode)
    root.mainloop()
    return selection

if __name__ == "__main__":
    list_of_items = ["Nixon","Hamilton","Richmond","Beasley","Schroeder","Singleton","Haney",
    "Joyce","Fisher","Carrillo","Barry","Day"]
    #list_of_items = [x for x in range(10000)]
    print(open_selection_box(list_of_items, text_mode = True, mode = tk.BROWSE))

