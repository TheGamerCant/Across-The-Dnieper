import tkinter as tk
from tkinter import messagebox

class ListEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("List Editor")

        self.list_data = ["Item 1", "Item 2", "Item 3"]

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.listbox.pack(padx=20, pady=20)

        self.entry = tk.Entry(self.root)
        self.entry.pack(padx=20, pady=5)

        self.add_button = tk.Button(self.root, text="Add", command=self.add_item)
        self.add_button.pack(padx=20, pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_item)
        self.edit_button.pack(padx=20, pady=5)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_list)
        self.save_button.pack(padx=20, pady=5)

        self.populate_listbox()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.list_data:
            self.listbox.insert(tk.END, item)

    def add_item(self):
        new_item = self.entry.get()
        if new_item:
            self.list_data.append(new_item)
            self.populate_listbox()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter an item.")

    def edit_item(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            new_value = self.entry.get()
            if new_value:
                self.list_data[selected_index[0]] = new_value
                self.populate_listbox()
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "Please enter a new value.")
        else:
            messagebox.showwarning("Selection Error", "Please select an item to edit.")

    def save_list(self):
        # In a real application, this would save to a file or database
        print("List saved:", self.list_data)
        messagebox.showinfo("Save", "List has been saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ListEditorApp(root)
    root.mainloop()