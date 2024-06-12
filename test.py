import PySimpleGUI as sg

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Email: {self.email}"

class ContactKeeper:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, email):
        if name in self.contacts:
            sg.popup("Contact already exists.")
        else:
            self.contacts[name] = Contact(name, phone, email)
            sg.popup(f"Contact {name} added.")

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            sg.popup(f"Contact {name} deleted.")
        else:
            sg.popup("Contact not found.")

    def search_contact(self, name):
        if name in self.contacts:
            sg.popup(str(self.contacts[name]))
        else:
            sg.popup("Contact not found.")

    def display_contacts(self):
        if self.contacts:
            contacts_str = '\n'.join([str(contact) for contact in self.contacts.values()])
            sg.popup(contacts_str)
        else:
            sg.popup("No contacts to display.")

    def edit_contact(self, name, phone=None, email=None):
        if name in self.contacts:
            if phone:
                self.contacts[name].phone = phone
            if email:
                self.contacts[name].email = email
            sg.popup(f"Contact {name} updated.")
        else:
            sg.popup("Contact not found.")

    def add_multiple_contacts(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    name, phone, email = line.strip().split(',')
                    self.add_contact(name, phone, email)
        except FileNotFoundError:
            sg.popup("File not found.")
        except ValueError:
            sg.popup("Error reading contacts from file. Please ensure each line is in the format: name,phone,email.")

def main():
    keeper = ContactKeeper()

    layout = [
        [sg.Text('Contact Keeper')],
        [sg.Button('Add Contact'), sg.Button('Delete Contact'), sg.Button('Search Contact')],
        [sg.Button('Display Contacts'), sg.Button('Edit Contact'), sg.Button('Add Multiple Contacts from File')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Contact Keeper', layout)

    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Add Contact':
            name, phone, email = sg.popup_get_text('Enter name'), sg.popup_get_text('Enter phone number'), sg.popup_get_text('Enter email')
            if name and phone and email:
                keeper.add_contact(name, phone, email)
        elif event == 'Delete Contact':
            name = sg.popup_get_text('Enter name of the contact to delete')
            if name:
                keeper.delete_contact(name)
        elif event == 'Search Contact':
            name = sg.popup_get_text('Enter name to search')
            if name:
                keeper.search_contact(name)
        elif event == 'Display Contacts':
            keeper.display_contacts()
        elif event == 'Edit Contact':
            name = sg.popup_get_text('Enter name of the contact to edit')
            if name:
                phone = sg.popup_get_text('Enter new phone number (leave blank to keep current)')
                email = sg.popup_get_text('Enter new email (leave blank to keep current)')
                keeper.edit_contact(name, phone if phone else None, email if email else None)
        elif event == 'Add Multiple Contacts from File':
            filename = sg.popup_get_file('Select file to load contacts from')
            if filename:
                keeper.add_multiple_contacts(filename)

    window.close()

if __name__ == "__main__":
    main()
