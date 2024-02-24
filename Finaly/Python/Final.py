from tkinter import *
from tkinter import simpledialog, messagebox

class ContactsApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Список контактів")
        self.contacts = {}
        self.load_contacts()
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        label = Label(self.root, text="Список контактів:", justify='center')  
        label.pack(pady=10)

        self.contact_listbox = Listbox(self.root, width=40, justify='center')  
        self.contact_listbox.pack()

        self.add_button = Button(self.root, text="Додати контакт", command=self.add_contact)
        self.add_button.pack(pady=5)

        self.edit_button = Button(self.root, text="Редагувати контакт", command=self.edit_contact)
        self.edit_button.pack(pady=5)

        self.delete_button = Button(self.root, text="Видалити контакт", command=self.delete_contact)
        self.delete_button.pack(pady=5)

        self.refresh_listbox()

    def refresh_listbox(self):
        self.contact_listbox.delete(0, END)
        for name, number in self.contacts.items():
            self.contact_listbox.insert(END, f"{name}: {number}")

    def add_contact(self):
        name = simpledialog.askstring("Додати контакт", "Введіть ім'я контакту:")
        if name:
            number = simpledialog.askstring("Додати контакт", f"Введіть номер для {name}:")
            if number:
                try:
                    if not number.startswith('+') and not number.isdigit():
                        raise ValueError("Номер телефону може містити лише цифри")
                    if not number.isdigit() and any(not char.isdigit() for char in number if char != '+'):
                        raise ValueError("Номер телефону може містити лише цифри")
                    if len(number) > 13:
                        raise ValueError("Номер телефону не може перевищувати 13 символів")
                    self.contacts[name] = number
                    self.refresh_listbox()
                    self.save_contacts()
                except ValueError as e:
                    messagebox.showerror("Помилка", str(e))

    def edit_contact(self):
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            index = selected_contact[0]
            contacts_names = list(self.contacts.keys())
            if index < len(contacts_names):
                name = contacts_names[index]
                new_number = simpledialog.askstring("Редагувати контакт", f"Введіть новий номер для {name}:")
                if new_number:
                    try:
                        if not (new_number.startswith('+') or new_number.isdigit()):
                            raise ValueError("Номер телефону може містити лише цифр")
                        if len(new_number) > 13:
                            raise ValueError("Номер телефону не може перевищувати 13 символів")
                        self.contacts[name] = new_number
                        self.refresh_listbox()
                        self.save_contacts()
                    except ValueError as e:
                        messagebox.showerror("Помилка", str(e))
            else:
                messagebox.showerror("Помилка", "Вибраний контакт не існує.")

    def delete_contact(self):
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            index = selected_contact[0]
            contacts_names = list(self.contacts.keys())
            if index < len(contacts_names):
                name = contacts_names[index]
                del self.contacts[name]
                self.refresh_listbox()
                self.save_contacts()
            else:
                messagebox.showerror("Помилка", "Вибраний контакт не існує.")

    def load_contacts(self):
        try:
            with open("contacts.txt", "r") as f:
                for line in f:
                    name, number = line.strip().split(":")
                    self.contacts[name] = number
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("contacts.txt", "w") as f:
            for name, number in self.contacts.items():
                f.write(f"{name}:{number}\n")

if __name__ == "__main__":
    ContactsApp()