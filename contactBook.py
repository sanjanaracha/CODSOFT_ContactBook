import tkinter as tk
from tkinter import ttk, messagebox

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.configure(bg="#5E6E55")  # Set background color
        self.contacts = []

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Frame for form inputs
        form_frame = ttk.Frame(self.root, padding="10")
        form_frame.grid(row=0, column=0, sticky="ew")
        form_frame.configure(style="Custom.TFrame")

        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, sticky="w")

        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w")
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(form_frame, textvariable=self.phone_var, width=30)
        self.phone_entry.grid(row=1, column=1, sticky="w")

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=2, column=1, sticky="w")

        # Address
        ttk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky="w")
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(form_frame, textvariable=self.address_var, width=30)
        self.address_entry.grid(row=3, column=1, sticky="w")

        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.add_button = ttk.Button(buttons_frame, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = ttk.Button(buttons_frame, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = ttk.Button(buttons_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.clear_button = ttk.Button(buttons_frame, text="Clear Fields", command=self.clear_fields)
        self.clear_button.grid(row=0, column=3, padx=5)

        # Search frame
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, sticky="w")

        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_contacts)
        self.search_button.grid(row=0, column=2, padx=5)

        self.show_all_button = ttk.Button(search_frame, text="Show All", command=self.show_all_contacts)
        self.show_all_button.grid(row=0, column=3, padx=5)

        # Contacts list frame
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.grid(row=2, column=0, sticky="nsew")

        self.contacts_tree = ttk.Treeview(list_frame, columns=("Name", "Phone", "Email", "Address"), show="headings", selectmode="browse")
        self.contacts_tree.heading("Name", text="Name")
        self.contacts_tree.heading("Phone", text="Phone")
        self.contacts_tree.heading("Email", text="Email")
        self.contacts_tree.heading("Address", text="Address")
        self.contacts_tree.column("Name", width=150)
        self.contacts_tree.column("Phone", width=100)
        self.contacts_tree.column("Email", width=150)
        self.contacts_tree.column("Address", width=200)
        self.contacts_tree.pack(side="left", fill="both", expand=True)

        self.contacts_tree.bind("<<TreeviewSelect>>", self.on_contact_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Configure root resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required fields.")
            return

        # Validate phone number: must be 10 digits
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showwarning("Input Error", "Phone number must be a 10-digit number.")
            return

        # Validate email: must contain '@' and '.'
        if email and ('@' not in email or '.' not in email):
            messagebox.showwarning("Input Error", "Email must contain '@' and '.' symbols.")
            return

        # Check for duplicate contact by name and phone
        for contact in self.contacts:
            if contact["name"] == name and contact["phone"] == phone:
                messagebox.showwarning("Duplicate Contact", "This contact already exists.")
                return

        contact = {"name": name, "phone": phone, "email": email, "address": address}
        self.contacts.append(contact)
        self.refresh_contacts()
        self.clear_fields()

    def refresh_contacts(self, contacts=None):
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)

        if contacts is None:
            contacts = self.contacts

        for contact in contacts:
            self.contacts_tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"], contact["address"]))

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.contacts_tree.selection_remove(self.contacts_tree.selection())

    def on_contact_select(self, event):
        selected = self.contacts_tree.selection()
        if selected:
            item = self.contacts_tree.item(selected[0])
            values = item["values"]
            self.name_var.set(values[0])
            self.phone_var.set(values[1])
            self.email_var.set(values[2])
            self.address_var.set(values[3])

    def update_contact(self):
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")
            return

        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required fields.")
            return

        # Validate phone number: must be 10 digits
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showwarning("Input Error", "Phone number must be a 10-digit number.")
            return

        # Validate email: must contain '@' and '.'
        if email and ('@' not in email or '.' not in email):
            messagebox.showwarning("Input Error", "Email must contain '@' and '.' symbols.")
            return

        index = self.contacts_tree.index(selected[0])
        self.contacts[index] = {"name": name, "phone": phone, "email": email, "address": address}
        self.refresh_contacts()
        self.clear_fields()

    def delete_contact(self):
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")
            return

        index = self.contacts_tree.index(selected[0])
        del self.contacts[index]
        self.refresh_contacts()
        self.clear_fields()

    def search_contacts(self):
        query = self.search_var.get().strip().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        filtered = [c for c in self.contacts if query in c["name"].lower() or query in c["phone"].lower()]
        if not filtered:
            messagebox.showinfo("Search", "No contacts found.")
        self.refresh_contacts(filtered)

    def show_all_contacts(self):
        self.refresh_contacts()
        self.search_var.set("")

if __name__ == "__main__":
    root = tk.Tk()

    # Define style for background color
    style = ttk.Style()
    style.configure("Custom.TFrame", background="#f0f4f8")
    style.configure("Treeview", background="white", fieldbackground="white")

    # Define style for Add Contact button with green background
    style.configure("Add.TButton",
                    foreground="white",
                    background="#4CAF50",
                    borderwidth=1,
                    focusthickness=3,
                    focuscolor='none')
    style.map("Add.TButton",
              background=[('active', '#45a049'), ('!disabled', '#4CAF50')],
              foreground=[('active', 'white'), ('!disabled', 'white')])

    app = ContactBookApp(root)
    root.mainloop()
