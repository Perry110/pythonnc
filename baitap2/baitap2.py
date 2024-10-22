import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 
import calendar
from datetime import datetime

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DatabaseApp")

        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')

        self.create_widgets()

    def create_widgets(self):
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            
            self.open_main_window()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the database: {e}")

    def open_main_window(self):
        self.root.withdraw()  # Đóng cửa sổ kết nối
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Booking Calendar")

        BookingCalendarApp(self.main_window, self.cursor, self.conn)  # Khởi tạo ứng dụng chính

class BookingCalendarApp:
    def __init__(self, root, cursor, conn):
        self.root = root
        self.cursor = cursor
        self.conn = conn

        # Biến toàn cục cho lịch và ngày đã đặt
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        # Thiết lập giao diện chính
        self.setup_ui()

        # Cập nhật lịch
        self.update_calendar()

    def setup_ui(self):
        # Khung chính để chứa tất cả các thành phần
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Khung cho việc nhập tên và dịch vụ
        self.entry_frame = ttk.Frame(self.main_frame)
        self.entry_frame.pack(fill=tk.X, pady=10)

        self.name_label = ttk.Label(self.entry_frame, text="Enter name:")
        self.name_label.grid(row=0, column=0, padx=10)
        self.name_entry = ttk.Entry(self.entry_frame)
        self.name_entry.grid(row=0, column=1, padx=10, sticky=tk.W)

        self.service_label = ttk.Label(self.entry_frame, text="Service:")
        self.service_label.grid(row=1, column=0, padx=10)
        self.service_entry = ttk.Entry(self.entry_frame)
        self.service_entry.grid(row=1, column=1, padx=10, sticky=tk.W)

        # Khung chỉnh tháng
        self.month_frame = ttk.Frame(self.main_frame)
        self.month_frame.pack(pady=10)

        self.prev_month_button = ttk.Button(self.month_frame, text="<", command=lambda: self.change_month(-1))
        self.prev_month_button.pack(side="left", padx=10)

        self.month_label = ttk.Label(self.month_frame, text=f"Month: {calendar.month_name[self.current_month]}")
        self.month_label.pack(side="left", padx=10)

        self.next_month_button = ttk.Button(self.month_frame, text=">", command=lambda: self.change_month(1))
        self.next_month_button.pack(side="left", padx=10)

        # Khung lịch
        self.calendar_frame = ttk.Frame(self.main_frame)
        self.calendar_frame.pack(pady=10)

        # Treeview để hiển thị các ngày đã đặt
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Name', 'Service', 'Day'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Service', text='Service')
        self.tree.heading('Day', text='Day')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Khung nút hành động
        self.action_buttons_frame = ttk.Frame(self.main_frame)
        self.action_buttons_frame.pack(pady=10)

        # Nút Xóa
        self.btn_delete = ttk.Button(self.action_buttons_frame, text="Delete", command=self.delete_booking)
        self.btn_delete.pack(pady=10)

        # Nút Đóng ở dưới cùng
        self.btn_close = ttk.Button(self.action_buttons_frame, text="Close", command=self.root.quit)
        self.btn_close.pack(pady=10)

    def update_calendar(self):
        # Xóa hiển thị lịch hiện tại
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Tạo lịch cho tháng hiện tại
        days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]

        for day in range(1, days_in_month + 1):
            day_frame = ttk.Frame(self.calendar_frame, relief="solid", borderwidth=1)
            day_frame.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=5, pady=5)

            day_label = ttk.Label(day_frame, text=f"{day}/{self.current_month}")
            day_label.pack()

            book_btn = ttk.Button(day_frame, text="Book", command=lambda d=day: self.book_day(d))
            book_btn.pack()

    def book_day(self, day):
        name = self.name_entry.get()
        service = self.service_entry.get()
        if not name or not service:
            messagebox.showerror("Error", "Please enter your name and service.")
            return
        
        # Chèn đặt chỗ vào database
        self.cursor.execute(
            "INSERT INTO bookdays (name, service, day) VALUES (%s, %s, %s)",
            (name, service, f"{day}/{self.current_month}/{self.current_year}")
        )
        self.conn.commit()

        # Cập nhật Treeview với dữ liệu từ database
        self.load_bookings()

    def load_bookings(self):
        # Tải đặt chỗ từ database và hiển thị trong Treeview
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM bookdays")
        bookings = self.cursor.fetchall()
        for booking in bookings:
            self.tree.insert('', 'end', values=booking)

    def delete_booking(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                item_values = self.tree.item(item, 'values')
                # Xóa đặt chỗ khỏi database
                self.cursor.execute(
                    "DELETE FROM bookdays WHERE id = %s",
                    (item_values[0],)  # Giả sử cột đầu tiên là ID
                )
                self.conn.commit()
                self.tree.delete(item)  # Xóa khỏi Treeview
            messagebox.showinfo("Success", "Selected bookings deleted successfully.")
        else:
            messagebox.showwarning("Warning", "No booking selected.")

    def change_month(self, delta):
        # Thay đổi tháng và cập nhật lịch
        self.current_month += delta
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        elif self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.month_label.config(text=f"Month: {calendar.month_name[self.current_month]}")
        self.update_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

