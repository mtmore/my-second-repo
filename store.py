"""
Mini Store Management System

A console-based application for simulating a store with two user types:
1. Store Manager - Add products, set prices and inventory
2. Customer - Browse products, manage cart, and checkout
"""

class Product:
    """
    A class to represent a product in the store.
    
    Attributes:
        name (str): The name of the product
        price (float): The price of the product
        stock (int): The available stock quantity
    """
    
    def __init__(self, name, price, stock):
        """
        Initialize a new Product instance.
        
        Args:
            name (str): Product name
            price (float): Product price
            stock (int): Initial stock quantity
        """
        self.name = name
        self.price = price
        self.stock = stock
    
    def __str__(self):
        """
        Return string representation of the product.
        
        Returns:
            str: Formatted string with product details
        """
        return f"{self.name} - ${self.price:.2f} (Stock: {self.stock})"


class CartItem:
    """
    A class to represent an item in the shopping cart.
    
    Attributes:
        product (Product): The product object
        quantity (int): The quantity in cart
    """
    
    def __init__(self, product, quantity):
        """
        Initialize a new CartItem instance.
        
        Args:
            product (Product): The product to add to cart
            quantity (int): Quantity of the product
        """
        self.product = product
        self.quantity = quantity
    
    def get_total_price(self):
        """
        Calculate total price for this cart item.
        
        Returns:
            float: Total price (price * quantity)
        """
        return self.product.price * self.quantity
    
    def __str__(self):
        """
        Return string representation of the cart item.
        
        Returns:
            str: Formatted string with cart item details
        """
        return f"{self.product.name} x{self.quantity} - ${self.get_total_price():.2f}"


class Cart:
    """
    A class to manage the shopping cart operations.
    
    Attributes:
        items: List of cart items
    """
    
    def __init__(self):
        """Initialize an empty shopping cart."""
        self.items = []
    
    def add_to_cart(self, product, quantity):
        """
        Add a product to the shopping cart.
        
        Args:
            product (Product): The product to add
            quantity (int): Quantity to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        if quantity <= 0:
            print("❌ Quantity must be positive!")
            return False
        
        if quantity > product.stock:
            print(f"❌ Not enough stock! Available: {product.stock}")
            return False
        
        # Check if product already in cart
        for item in self.items:
            if item.product.name == product.name:
                if item.quantity + quantity > product.stock:
                    print(f"❌ Cannot add {quantity} more. Total would exceed available stock!")
                    return False
                item.quantity += quantity
                print(f"✅ Added {quantity} x {product.name} to cart.")
                return True
        
        # Add new item to cart
        self.items.append(CartItem(product, quantity))
        print(f"✅ Added {quantity} x {product.name} to cart.")
        return True
    
    def remove_from_cart(self, product_name):
        """
        Remove a product from the shopping cart.
        
        Args:
            product_name (str): Name of the product to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, item in enumerate(self.items):
            if item.product.name.lower() == product_name.lower():
                removed_item = self.items.pop(i)
                print(f"🗑️ Removed {removed_item.product.name} from cart.")
                return True
        print("❌ Product not found in cart!")
        return False
    
    def view_cart(self):
        """Display the contents of the shopping cart."""
        if not self.items:
            print("🛒 Your cart is empty!")
            return
        
        print("🛒 Your cart:")
        for item in self.items:
            print(f" - {item}")
        
        print(f"💰 Total: ${self.total_price():.2f}")
    
    def total_price(self):
        """
        Calculate the total price of all items in cart.
        
        Returns:
            float: Total price of cart
        """
        return sum(item.get_total_price() for item in self.items)
    
    def checkout(self):
        """Process the checkout and update product stock."""
        if not self.items:
            print("❌ Cart is empty!")
            return
        
        print("🧾 Final Checkout:")
        for item in self.items:
            print(f" - {item}")
            # Update product stock
            item.product.stock -= item.quantity
        
        print(f"💳 Total amount due: ${self.total_price():.2f}")
        print("🎉 Thank you for shopping with us!")
        self.items.clear()


class Store:
    """
    Main store class managing all operations and user interfaces.
    
    Attributes:
        products: List of products in store
        manager_username (str): Manager login username
        manager_password (str): Manager login password
    """
    
    def __init__(self):
        """Initialize the store with default credentials and empty product list."""
        self.products = []
        self.manager_username = "admin"
        self.manager_password = "1234"
    
    def add_product(self, name, price, stock):
        """
        Add a new product to the store inventory.
        
        Args:
            name (str): Product name
            price (float): Product price
            stock (int): Initial stock quantity
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if price <= 0:
            print("❌ Price must be positive!")
            return False
        
        if stock < 0:
            print("❌ Stock cannot be negative!")
            return False
        
        new_product = Product(name, price, stock)
        self.products.append(new_product)
        print(f"✅ Product added: {new_product}")
        return True
    
    def list_products(self):
        """Display all available products in the store."""
        if not self.products:
            print("📭 No products available in the store.")
            return
        
        print("Available products:")
        for i, product in enumerate(self.products, 1):
            print(f"[{i}] {product}")
    
    def find_product(self, name):
        """
        Find a product by its name (case-insensitive).
        
        Args:
            name (str): Product name to search for
            
        Returns:
            Product: Found product object or None
        """
        for product in self.products:
            if product.name.lower() == name.lower():
                return product
        return None
    
    def manager_login(self):
        """
        Authenticate store manager credentials.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        print("\n" + "-" * 32)
        print("🔐 Store Manager Login")
        print("-" * 32)
        
        username = input("Username: ")
        password = input("Password: ")
        
        if username == self.manager_username and password == self.manager_password:
            print("✅ Login successful! Welcome, Manager.")
            return True
        else:
            print("❌ Login failed! Please try again or return to main menu.")
            return False
    
    def manager_menu(self):
        """Menu for store manager operations."""
        while True:
            print("\n" + "-" * 32)
            print("📦 Manager Menu")
            print("-" * 32)
            print("1. Add Products")
            print("2. View Products")
            print("3. Back to Main Menu")
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self.add_products_menu()
            elif choice == "2":
                self.list_products()
            elif choice == "3":
                print("Returning to main menu...")
                break
            else:
                print("❌ Invalid choice!")
    
    def add_products_menu(self):
        """Menu for adding new products to the store inventory."""
        print("\n" + "-" * 32)
        print("📦 Add Products")
        print("-" * 32)
        
        while True:
            name = input("Enter product name (or 'done' to finish): ")
            if name.lower() == 'done':
                break
            
            try:
                price = float(input("Enter product price: "))
                stock = int(input("Enter product stock quantity: "))
                
                self.add_product(name, price, stock)
                
            except ValueError:
                print("❌ Invalid input! Please enter valid numbers.")
    
    def customer_menu(self):
        """Customer interface for browsing and purchasing products."""
        cart = Cart()
        
        while True:
            print("\n" + "-" * 20)
            print("🛍️ CUSTOMER PORTAL")
            print("-" * 20)
            print("Hello, dear customer!")
            self.list_products()
            
            print("\nWhat would you like to do?")
            print("1. Add item to cart")
            print("2. Remove item from cart")
            print("3. View cart")
            print("4. Checkout")
            print("5. Return to main menu")
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                product_name = input("Enter product name: ")
                product = self.find_product(product_name)
                
                if product:
                    try:
                        quantity = int(input("Enter quantity: "))
                        cart.add_to_cart(product, quantity)
                    except ValueError:
                        print("❌ Please enter a valid number!")
                else:
                    print("❌ Product not found!")
            
            elif choice == "2":
                product_name = input("Enter product name to remove: ")
                cart.remove_from_cart(product_name)
            
            elif choice == "3":
                cart.view_cart()
            
            elif choice == "4":
                cart.checkout()
                break
            
            elif choice == "5":
                print("Returning to main menu...")
                break
            
            else:
                print("❌ Invalid choice! Please select 1-5.")


def main():
    """
    Main function to run the Store Management System.
    
    Handles the main menu and directs to appropriate portals.
    """
    store = Store()
    
    # Add some sample products
    store.add_product("Laptop", 1200.0, 5)
    store.add_product("Mouse", 25.0, 20)
    
    while True:
        print("\n" + "=" * 48)
        print("🛍️  MINI STORE MANAGEMENT SYSTEM")
        print("=" * 48)
        print("👋 Welcome! Please select your role:")
        print("1. Store Manager")
        print("2. Customer")
        print("3. Exit Program")
        
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            if store.manager_login():
                store.manager_menu()
        
        elif choice == "2":
            store.customer_menu()
        
        elif choice == "3":
            print("👋 Goodbye! See you next time.")
            break
        
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.")


if __name__ == "__main__":
    """Entry point of the application."""
    main()