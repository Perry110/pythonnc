import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

#Connect with PostgreSQL 
conn = psycopg2.connect(
    host ="localhost" ,
    database = "petshop" ,
    user = "postgres",
    password = "123",
    port = "5432"
)

cur = conn.cursor()

# Hàm thêm sản phẩm
def add_product():
    id = entry_id.get()
    name = entry_name.get()
    category = entry_category.get()
    price = entry_price.get()
    
    try: 
        cur.execute("INSERT INTO products (id, name, category, price) VALUES (%s ,%s, %s, %s)", (id, name, category, price))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
    except: 
        messagebox.showerror("Error", "All fields are required!")
    
    clear_entries()

# Hàm hiển thị tất cả sản phẩm
def show_products():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    
    for row in rows:
            tree.insert("", tk.END, values=row)

# Hàm xóa sản phẩm theo ID
def delete_product():
    product_id = entry_id.get()
    
    try:
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
    except : 
        messagebox.showerror("Error", "ID is required!")
    
    clear_entries()

# Hàm sửa sản phẩm theo ID
def update_product():
    product_id = entry_id.get()
    name = entry_name.get()
    category = entry_category.get()
    price = entry_price.get()
    
    try :
        cur.execute("UPDATE products SET name = %s, category = %s, price = %s WHERE id = %s", (name, category, price, product_id))
        conn.commit()
        messagebox.showinfo("Success", "Product updated successfully!")
    except : 
        messagebox.showerror("Error", "All fields are required!")
    
    clear_entries()

# Hàm xóa các trường nhập
def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_price.delete(0, tk.END)
 
root = tk.Tk()
root.title("Product Management")

# Nhãn và ô nhập cho các trường
tk.Label(root, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Product Name").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Category").grid(row=2, column=0)
entry_category = tk.Entry(root)
entry_category.grid(row=2, column=1)

tk.Label(root, text="Price").grid(row=3, column=0)
entry_price = tk.Entry(root)
entry_price.grid(row=3, column=1)

# Các nút chức năng
tk.Button(root, text="Add Product", command=add_product).grid(row=4, column=0)
tk.Button(root, text="Update Product", command=update_product).grid(row=4, column=1)
tk.Button(root, text="Delete Product", command=delete_product).grid(row=4, column=2)
tk.Button(root, text="Show All Products", command=show_products).grid(row=5, column=1)

# Tạo Treeview để chia cột
tree = ttk.Treeview(root, columns=("id", "name", "category", "price"), show="headings", height=8)
tree.grid(row=6, column=0, columnspan=2)

# Định nghĩa tiêu đề cho các cột
tree.heading("id", text="ID")
tree.heading("name", text="Tên sản phẩm")
tree.heading("category", text="Loại sản phẩm")
tree.heading("price", text="Giá")

# Đặt chiều rộng cho các cột
tree.column("id", width=50)
tree.column("name", width=150)
tree.column("category", width=100)
tree.column("price", width=100)

# Chạy chương trình
root.mainloop()

# Đóng kết nối khi thoát
cur.close()
conn.close()

    
