import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import time
from tkinter import font as tkfont

class AnimatedButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_bg = self.cget("style")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self.configure(style='Hover.TButton')
        
    def on_leave(self, e):
        self.configure(style=self.default_bg)

class ContractFarmingPlatform:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 FarmConnect - Contract Farming Platform")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        # Configure color scheme
        self.colors = {
            'primary': '#4CAF50',
            'secondary': '#8BC34A',
            'accent': '#FFC107',
            'background': '#F5F5F5',
            'text': '#212121',
            'error': '#F44336',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'info': '#2196F3'
        }
        
        # Configure styles with colors
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Background styles
        self.style.configure('.', background=self.colors['background'])
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], 
                           foreground=self.colors['text'], font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), 
                           foreground=self.colors['primary'])
        
        # Button styles
        self.style.configure('TButton', background=self.colors['primary'], 
                           foreground='white', borderwidth=1)
        self.style.map('TButton',
                      background=[('active', self.colors['secondary']),
                                 ('disabled', '#BDBDBD')])
        
        self.style.configure('Hover.TButton', background=self.colors['secondary'])
        self.style.configure('Accent.TButton', background=self.colors['accent'])
        self.style.configure('Danger.TButton', background=self.colors['error'])
        
        # Entry styles
        self.style.configure('TEntry', fieldbackground='white', 
                           foreground=self.colors['text'])
        
        # Combobox styles
        self.style.configure('TCombobox', fieldbackground='white')
        
        # Treeview styles
        self.style.configure('Treeview', background='white', 
                           fieldbackground='white', foreground=self.colors['text'])
        self.style.configure('Treeview.Heading', background=self.colors['primary'], 
                           foreground='white', font=('Arial', 10, 'bold'))
        self.style.map('Treeview', 
                      background=[('selected', self.colors['secondary'])])
        
        # Status colors
        self.status_colors = {
            'Pending': self.colors['warning'],
            'Accepted': self.colors['success'],
            'Rejected': self.colors['error'],
            'Delivered': '#4CAF50',
            'Paid': '#2196F3'
        }
        
        # Initialize data stores
        self.farmers = []
        self.buyers = []
        self.contracts = []
        self.products = [
            "Wheat", "Rice", "Corn", "Soybeans", 
            "Potatoes", "Tomatoes", "Cotton", "Coffee"
        ]
        
        # Current session
        self.current_user = None
        self.user_type = None
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_login_screen()
    
    def show_notification(self, message, message_type='info'):
        """Show animated notification message"""
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)
        notification.geometry(f"+{self.root.winfo_rootx()+self.root.winfo_width()//2-150}+{self.root.winfo_rooty()+self.root.winfo_height()-100}")
        
        color = self.colors.get(message_type, self.colors['info'])
        label = ttk.Label(
            notification, 
            text=message, 
            background=color,
            foreground='white',
            padding=10,
            font=('Arial', 10, 'bold'),
            relief='solid',
            borderwidth=1
        )
        label.pack()
        
        # Animate notification
        notification.attributes('-alpha', 0)
        for i in range(1, 11):
            notification.attributes('-alpha', i/10)
            notification.update()
            time.sleep(0.02)
        
        notification.after(3000, notification.destroy)
    
    def clear_frame(self, frame=None):
        """Destroy all widgets in the specified frame"""
        frame = frame or self.main_frame
        for widget in frame.winfo_children():
            widget.destroy()
    
    def validate_contact(self, contact):
        """Validate phone number format"""
        return re.match(r'^[0-9]{10,15}$', contact)
    
    def validate_password(self, password):
        """Validate password strength"""
        return len(password) >= 6
    
    def show_login_screen(self):
        """Display the login/registration screen"""
        self.clear_frame()
        self.current_user = None
        self.user_type = None
        
        # Main container
        container = ttk.Frame(self.main_frame, style='TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Login Section
        login_frame = ttk.LabelFrame(
            container, 
            text=" Login ", 
            padding=(20, 10), 
            style='TFrame'
        )
        login_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(login_frame, text="User Type:", style='Header.TLabel').grid(row=0, column=0, sticky="w", pady=5)
        self.user_type_var = tk.StringVar(value="Farmer")
        user_type_combo = ttk.Combobox(
            login_frame, 
            textvariable=self.user_type_var, 
            values=["Farmer", "Buyer"], 
            state="readonly",
            width=18
        )
        user_type_combo.grid(row=0, column=1, pady=5, sticky="ew")
        
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(login_frame, width=20)
        self.username_entry.grid(row=1, column=1, pady=5, sticky="ew")
        
        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(login_frame, show="•", width=20)
        self.password_entry.grid(row=2, column=1, pady=5, sticky="ew")
        
        login_btn = AnimatedButton(
            login_frame, 
            text="Login", 
            command=self.login,
            style='TButton'
        )
        login_btn.grid(row=3, column=1, pady=10, sticky="e")
        
        # Registration Section
        reg_frame = ttk.LabelFrame(
            container, 
            text=" New User Registration ", 
            padding=(20, 10), 
            style='TFrame'
        )
        reg_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        fields = [
            ("Full Name:", "reg_name"),
            ("Contact No:", "reg_contact"),
            ("Location:", "reg_location"),
            ("Username:", "reg_username"),
            ("Password:", "reg_password")
        ]
        
        for i, (label, attr) in enumerate(fields):
            ttk.Label(reg_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(reg_frame, width=20)
            entry.grid(row=i, column=1, pady=5, sticky="ew")
            setattr(self, attr, entry)
            
            # Add validation for specific fields
            if label == "Contact No:":
                entry.config(validate="key", validatecommand=(self.root.register(self.validate_contact_input), '%P'))
            elif label == "Password:":
                entry.config(show="•")
        
        reg_btn = AnimatedButton(
            reg_frame, 
            text="Register", 
            command=self.register,
            style='TButton'
        )
        reg_btn.grid(row=len(fields), column=1, pady=10, sticky="e")
        
        # Configure grid weights
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)
        
        login_frame.columnconfigure(1, weight=1)
        reg_frame.columnconfigure(1, weight=1)
    
    def validate_contact_input(self, value):
        """Validation for contact number input"""
        return value.isdigit() or value == ""
    
    def login(self):
        """Handle user login with visual feedback"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()
        
        if not username or not password:
            self.show_notification("Please enter both username and password", "error")
            return
        
        users = self.farmers if user_type == "Farmer" else self.buyers
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                self.user_type = user_type.lower()
                self.show_notification(f"Welcome back, {user['name']}!", "success")
                self.show_dashboard()
                return
        
        self.show_notification("Invalid username or password", "error")
    
    def register(self):
        """Handle registration with visual feedback"""
        try:
            user_type = self.user_type_var.get()
            
            # Get and validate all fields
            fields = {
                'name': self.reg_name.get().strip(),
                'contact': self.reg_contact.get().strip(),
                'location': self.reg_location.get().strip(),
                'username': self.reg_username.get().strip(),
                'password': self.reg_password.get()
            }
            
            # Validate required fields
            if not all(fields.values()):
                missing = [k for k, v in fields.items() if not v]
                self.show_notification(f"Missing fields: {', '.join(missing)}", "error")
                return
                
            # Validate contact number
            if not re.match(r'^[0-9]{10,15}$', fields['contact']):
                self.show_notification("Invalid contact number (10-15 digits)", "error")
                return
                
            # Validate password strength
            if len(fields['password']) < 6:
                self.show_notification("Password must be at least 6 characters", "error")
                return
                
            # Check for existing username
            all_users = self.farmers + self.buyers
            if any(user['username'].lower() == fields['username'].lower() for user in all_users):
                self.show_notification("Username already exists", "error")
                return
                
            # Create user profile
            user_profile = {
                **fields,
                'products' if user_type == "Farmer" else 'interests': [],
                'registration_date': datetime.now().strftime("%Y-%m-%d")
            }
            
            # Add to appropriate user list
            if user_type == "Farmer":
                self.farmers.append(user_profile)
                icon = "👨‍🌾"
            else:
                self.buyers.append(user_profile)
                icon = "👔"
                
            self.show_notification(f"{icon} Registration successful! Please login.", "success")
            self.clear_registration_form()
            
        except Exception as e:
            self.show_notification(f"Error: {str(e)}", "error")
    
    def clear_registration_form(self):
        """Clear all registration fields"""
        self.reg_name.delete(0, tk.END)
        self.reg_contact.delete(0, tk.END)
        self.reg_location.delete(0, tk.END)
        self.reg_username.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)
    
    def show_dashboard(self):
        """Show the appropriate dashboard based on user type"""
        self.clear_frame()
        
        # Header with user info
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text=f"Welcome, {self.current_user['name']} ({self.user_type.capitalize()})",
            style='Header.TLabel',
            font=('Arial', 14, 'bold')
        ).pack(side=tk.LEFT)
        
        logout_btn = AnimatedButton(
            header_frame, 
            text="🚪 Logout", 
            command=self.show_login_screen,
            style='Danger.TButton'
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Navigation
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        if self.user_type == "farmer":
            buttons = [
                ("🌱 My Products", self.show_farmer_products),
                ("🔍 Find Buyers", self.find_buyers),
                ("📜 My Contracts", self.show_my_contracts)
            ]
        else:
            buttons = [
                ("👨‍🌾 Find Farmers", self.find_farmers),
                ("📜 My Contracts", self.show_my_contracts)
            ]
            
        for text, command in buttons:
            btn = AnimatedButton(
                nav_frame, 
                text=text, 
                command=command,
                style='TButton'
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show default content
        if self.user_type == "farmer":
            self.show_farmer_products()
        else:
            self.find_farmers()
    
    def show_farmer_products(self):
        """Display farmer's products and management interface"""
        self.clear_content_frame()
        
        # Current products
        products_frame = ttk.LabelFrame(
            self.content_frame, 
            text=" My Products ",
            padding=10
        )
        products_frame.pack(fill=tk.X, padx=5, pady=5)
        
        if not self.current_user['products']:
            ttk.Label(
                products_frame, 
                text="No products added yet",
                style='TLabel'
            ).pack()
        else:
            for product in self.current_user['products']:
                product_frame = ttk.Frame(products_frame)
                product_frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(
                    product_frame, 
                    text=f"{product['name']} - {product['quantity']} kg - ₹{product['price']}/kg",
                    style='TLabel'
                ).pack(side=tk.LEFT)
                
                ttk.Button(
                    product_frame, 
                    text="Remove", 
                    command=lambda p=product: self.remove_product(p),
                    style='Danger.TButton'
                ).pack(side=tk.RIGHT)
        
        # Add new product
        add_frame = ttk.LabelFrame(
            self.content_frame, 
            text=" Add New Product ",
            padding=10
        )
        add_frame.pack(fill=tk.X, padx=5, pady=5)
        
        fields = [
            ("Product:", "new_product", ttk.Combobox(add_frame, values=self.products, state="readonly")),
            ("Quantity (kg):", "new_quantity", ttk.Entry(add_frame)),
            ("Price per kg (₹):", "new_price", ttk.Entry(add_frame)),
            ("Harvest Date:", "new_harvest", ttk.Entry(add_frame))
        ]
        
        for i, (label, attr, widget) in enumerate(fields):
            ttk.Label(add_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
            widget.grid(row=i, column=1, sticky="ew", pady=2)
            setattr(self, attr, widget)
            add_frame.columnconfigure(1, weight=1)
        
        ttk.Button(
            add_frame, 
            text="Add Product", 
            command=self.add_product,
            style='TButton'
        ).grid(row=len(fields), column=1, pady=5, sticky="e")
    
    def add_product(self):
        """Add a new product to farmer's inventory"""
        try:
            product = {
                'name': self.new_product.get(),
                'quantity': float(self.new_quantity.get()),
                'price': float(self.new_price.get()),
                'harvest_date': self.new_harvest.get(),
                'added_date': datetime.now().strftime("%Y-%m-%d")
            }
            
            if not all(product.values()):
                raise ValueError("All fields are required")
                
            if product['quantity'] <= 0 or product['price'] <= 0:
                raise ValueError("Quantity and price must be positive numbers")
                
        except ValueError as e:
            self.show_notification(f"Invalid input: {str(e)}", "error")
            return
            
        self.current_user['products'].append(product)
        self.show_farmer_products()
        self.show_notification("Product added successfully!", "success")
    
    def remove_product(self, product):
        """Remove a product from farmer's inventory"""
        self.current_user['products'].remove(product)
        self.show_farmer_products()
        self.show_notification("Product removed successfully!", "success")
    
    def find_buyers(self):
        """Display list of buyers for farmers to connect with"""
        self.clear_content_frame()
        
        if not self.buyers:
            ttk.Label(
                self.content_frame, 
                text="No buyers registered yet",
                style='TLabel'
            ).pack()
            return
            
        for buyer in self.buyers:
            buyer_frame = ttk.LabelFrame(
                self.content_frame, 
                text=buyer['name'],
                padding=10
            )
            buyer_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(
                buyer_frame, 
                text=f"Contact: {buyer['contact']} | Location: {buyer['location']}",
                style='TLabel'
            ).pack(anchor=tk.W)
            
            # Show matching products
            matching_products = self.current_user['products']
            
            if matching_products:
                ttk.Label(
                    buyer_frame, 
                    text="Available Products:",
                    style='Header.TLabel'
                ).pack(anchor=tk.W)
                
                for product in matching_products:
                    product_text = f"{product['name']} - {product['quantity']} kg - ₹{product['price']}/kg"
                    ttk.Label(
                        buyer_frame, 
                        text=product_text,
                        style='TLabel'
                    ).pack(anchor=tk.W)
                
                ttk.Button(
                    buyer_frame, 
                    text="Propose Contract", 
                    command=lambda b=buyer: self.propose_contract(b),
                    style='Accent.TButton'
                ).pack(pady=5)
            else:
                ttk.Label(
                    buyer_frame, 
                    text="No products available to offer",
                    style='TLabel'
                ).pack()
    
    def find_farmers(self):
        """Display list of farmers for buyers to connect with"""
        self.clear_content_frame()
        
        if not self.farmers:
            ttk.Label(
                self.content_frame, 
                text="No farmers registered yet",
                style='TLabel'
            ).pack()
            return
            
        for farmer in self.farmers:
            farmer_frame = ttk.LabelFrame(
                self.content_frame, 
                text=farmer['name'],
                padding=10
            )
            farmer_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(
                farmer_frame, 
                text=f"Contact: {farmer['contact']} | Location: {farmer['location']}",
                style='TLabel'
            ).pack(anchor=tk.W)
            
            if farmer['products']:
                ttk.Label(
                    farmer_frame, 
                    text="Available Products:",
                    style='Header.TLabel'
                ).pack(anchor=tk.W)
                
                for product in farmer['products']:
                    product_text = f"{product['name']} - {product['quantity']} kg - ₹{product['price']}/kg"
                    ttk.Label(
                        farmer_frame, 
                        text=product_text,
                        style='TLabel'
                    ).pack(anchor=tk.W)
                
                ttk.Button(
                    farmer_frame, 
                    text="Propose Contract", 
                    command=lambda f=farmer: self.propose_contract(f),
                    style='Accent.TButton'
                ).pack(pady=5)
            else:
                ttk.Label(
                    farmer_frame, 
                    text="No products available",
                    style='TLabel'
                ).pack()
    
    def propose_contract(self, counterparty):
        """Show contract proposal form"""
        self.clear_content_frame()
        
        contract_frame = ttk.LabelFrame(
            self.content_frame, 
            text=" Contract Proposal ",
            padding=15
        )
        contract_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Counterparty info
        ttk.Label(
            contract_frame, 
            text=f"Contract with: {counterparty['name']} ({'Buyer' if self.user_type == 'farmer' else 'Farmer'})",
            style='Header.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=5, sticky="w")
        
        # Product selection
        products = self.current_user['products'] if self.user_type == "farmer" else counterparty['products']
        
        if not products:
            ttk.Label(
                contract_frame, 
                text="No products available for contract",
                style='TLabel'
            ).grid(row=1, column=0, columnspan=2)
            return
            
        ttk.Label(contract_frame, text="Select Product:").grid(row=1, column=0, sticky="w", pady=5)
        self.contract_product = ttk.Combobox(
            contract_frame, 
            state="readonly",
            values=[f"{p['name']} - {p['quantity']} kg" for p in products]
        )
        self.contract_product.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Contract details
        fields = [
            ("Quantity (kg):", "contract_quantity"),
            ("Price per kg (₹):", "contract_price"),
            ("Delivery Date:", "contract_delivery"),
            ("Payment Terms:", "contract_payment")
        ]
        
        for i, (label, attr) in enumerate(fields, start=2):
            ttk.Label(contract_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            
            if label == "Payment Terms:":
                widget = ttk.Combobox(
                    contract_frame, 
                    values=[
                        "50% advance, 50% on delivery", 
                        "100% on delivery", 
                        "30% advance, 70% on delivery"
                    ],
                    state="readonly"
                )
            else:
                widget = ttk.Entry(contract_frame)
                
            widget.grid(row=i, column=1, sticky="ew", pady=5)
            setattr(self, attr, widget)
        
        contract_frame.columnconfigure(1, weight=1)
        
        ttk.Button(
            contract_frame, 
            text="Submit Proposal", 
            command=lambda: self.create_contract(counterparty),
            style='Accent.TButton'
        ).grid(row=len(fields)+2, column=1, pady=10, sticky="e")
    
    def create_contract(self, counterparty):
        """Create a new contract agreement"""
        try:
            # Get selected product
            product_idx = self.contract_product.current()
            if product_idx == -1:
                raise ValueError("Please select a product")
                
            # Get product details
            if self.user_type == "farmer":
                product = self.current_user['products'][product_idx]
            else:
                product = counterparty['products'][product_idx]
            
            # Validate contract details
            quantity = float(self.contract_quantity.get())
            price = float(self.contract_price.get())
            delivery_date = self.contract_delivery.get()
            payment_terms = self.contract_payment.get()
            
            if quantity <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive numbers")
                
            if not delivery_date or not payment_terms:
                raise ValueError("All fields are required")
                
            if quantity > product['quantity']:
                raise ValueError(f"Quantity cannot exceed available {product['quantity']} kg")
                
        except ValueError as e:
            self.show_notification(f"Invalid input: {str(e)}", "error")
            return
            
        # Create contract
        contract = {
            'id': len(self.contracts) + 1,
            'farmer': self.current_user['username'] if self.user_type == "farmer" else counterparty['username'],
            'buyer': counterparty['username'] if self.user_type == "farmer" else self.current_user['username'],
            'product': product['name'],
            'quantity': quantity,
            'price': price,
            'total_value': quantity * price,
            'delivery_date': delivery_date,
            'payment_terms': payment_terms,
            'status': 'Pending',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.contracts.append(contract)
        self.show_notification("Contract proposal created successfully!", "success")
        self.show_my_contracts()
    
    def show_my_contracts(self):
        """Display user's contracts"""
        self.clear_content_frame()
        
        contracts_frame = ttk.LabelFrame(
            self.content_frame, 
            text=" My Contracts ",
            padding=10
        )
        contracts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get user's contracts
        if self.user_type == "farmer":
            user_contracts = [c for c in self.contracts if c['farmer'] == self.current_user['username']]
        else:
            user_contracts = [c for c in self.contracts if c['buyer'] == self.current_user['username']]
        
        if not user_contracts:
            ttk.Label(
                contracts_frame, 
                text="No contracts found",
                style='TLabel'
            ).pack()
            return
            
        # Create treeview
        columns = ("id", "product", "quantity", "price", "total", "status", "counterparty", "delivery")
        tree = ttk.Treeview(
            contracts_frame, 
            columns=columns, 
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("product", text="Product")
        tree.heading("quantity", text="Qty (kg)")
        tree.heading("price", text="Price (₹/kg)")
        tree.heading("total", text="Total (₹)")
        tree.heading("status", text="Status")
        tree.heading("counterparty", text="Counterparty")
        tree.heading("delivery", text="Delivery Date")
        
        tree.column("id", width=50, anchor=tk.CENTER)
        tree.column("product", width=100)
        tree.column("quantity", width=80, anchor=tk.E)
        tree.column("price", width=80, anchor=tk.E)
        tree.column("total", width=100, anchor=tk.E)
        tree.column("status", width=100)
        tree.column("counterparty", width=120)
        tree.column("delivery", width=100)
        
        # Add data
        for contract in user_contracts:
            counterparty = contract['buyer'] if self.user_type == "farmer" else contract['farmer']
            tree.insert("", tk.END, values=(
                contract['id'],
                contract['product'],
                contract['quantity'],
                f"₹{contract['price']}",
                f"₹{contract['total_value']}",
                contract['status'],
                counterparty,
                contract['delivery_date']
            ), tags=(contract['status'],))
            
            # Configure tag colors for status
            tree.tag_configure(contract['status'], foreground=self.status_colors.get(contract['status'], 'black'))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(contracts_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(contracts_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            action_frame, 
            text="View Details", 
            command=lambda: self.view_contract_details(tree),
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        if self.user_type == "farmer":
            ttk.Button(
                action_frame, 
                text="Mark as Delivered", 
                command=lambda: self.update_contract_status(tree, "Delivered"),
                style='Accent.TButton'
            ).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Button(
                action_frame, 
                text="Accept", 
                command=lambda: self.update_contract_status(tree, "Accepted"),
                style='TButton'
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                action_frame, 
                text="Reject", 
                command=lambda: self.update_contract_status(tree, "Rejected"),
                style='Danger.TButton'
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                action_frame, 
                text="Make Payment", 
                command=lambda: self.make_payment(tree),
                style='Accent.TButton'
            ).pack(side=tk.LEFT, padx=5)
    
    def view_contract_details(self, tree):
        """Show detailed view of selected contract"""
        selected = tree.focus()
        if not selected:
            self.show_notification("Please select a contract first", "warning")
            return
            
        item = tree.item(selected)
        contract_id = item['values'][0]
        contract = next((c for c in self.contracts if c['id'] == contract_id), None)
        
        if not contract:
            return
            
        # Create details window
        details_win = tk.Toplevel(self.root)
        details_win.title(f"Contract #{contract_id} Details")
        details_win.geometry("500x450")
        
        # Main frame
        main_frame = ttk.Frame(details_win, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            main_frame, 
            text=f"Contract #{contract_id}", 
            style='Header.TLabel'
        ).pack(pady=10)
        
        # Details
        details = [
            ("Product:", contract['product']),
            ("Quantity:", f"{contract['quantity']} kg"),
            ("Price:", f"₹{contract['price']}/kg"),
            ("Total Value:", f"₹{contract['total_value']}"),
            ("Farmer:", contract['farmer']),
            ("Buyer:", contract['buyer']),
            ("Delivery Date:", contract['delivery_date']),
            ("Payment Terms:", contract['payment_terms']),
            ("Status:", contract['status']),
            ("Created At:", contract['created_at']),
            ("Last Updated:", contract['updated_at'])
        ]
        
        for label, value in details:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
            ttk.Label(frame, text=value).pack(side=tk.LEFT)
        
        # Close button
        ttk.Button(
            main_frame, 
            text="Close", 
            command=details_win.destroy,
            style='TButton'
        ).pack(pady=10)
    
    def update_contract_status(self, tree, status):
        """Update the status of the selected contract"""
        selected = tree.focus()
        if not selected:
            self.show_notification("Please select a contract first", "warning")
            return
            
        item = tree.item(selected)
        contract_id = item['values'][0]
        
        for contract in self.contracts:
            if contract['id'] == contract_id:
                contract['status'] = status
                contract['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.show_my_contracts()
        self.show_notification(f"Contract status updated to {status}", "success")
    
    def make_payment(self, tree):
        """Simulate payment processing for the selected contract"""
        selected = tree.focus()
        if not selected:
            self.show_notification("Please select a contract first", "warning")
            return
            
        item = tree.item(selected)
        contract_id = item['values'][0]
        contract = next((c for c in self.contracts if c['id'] == contract_id), None)
        
        if not contract:
            return
            
        # Simulate payment processing
        self.show_notification(
            f"Payment of ₹{contract['total_value']} processed successfully!",
            "success"
        )
        
        contract['status'] = "Paid"
        contract['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.show_my_contracts()
    
    def clear_content_frame(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon and title
    try:
        root.iconbitmap('farm_icon.ico')  # Provide your icon file
    except:
        pass  # Use default if icon not found
    
    # Set default font
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=10)
    
    app = ContractFarmingPlatform(root)
    root.mainloop()