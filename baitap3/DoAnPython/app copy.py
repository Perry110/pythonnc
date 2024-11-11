from flask import Flask, render_template ,request , redirect , url_for ,flash, jsonify,session
import os
import psycopg2
import base64
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="logindb",
        user="postgres",
        password="123",
        port = "5432"
    )
    return conn


@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu")
        return "Không thể kết nối đến cơ sở dữ liệu", 500
    
    try:
        # Thực hiện truy vấn SQL
        cur.execute('SELECT id, name, category, old_price, new_price FROM products')
        services = cur.fetchall()
        print("Sản phẩm truy vấn được:", services)  # Log kết quả truy vấn

    except Exception as e:
        print(f"Đã có lỗi khi truy vấn dữ liệu: {e}")
        services = []

    cur.close()
    conn.close()
    
    return render_template('home.html', products = services)

@app.route("/login" , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        # Truy vấn để kiểm tra thông tin đăng nhập
        cur.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return redirect(url_for('home'))  # Đăng nhập thành công
        else:
            error = 'Tên đăng nhập hoặc mật khẩu không đúng.'
            return render_template('login.html', error=error)  # Hiển thị thông báo lỗi

    return render_template('login.html')  # Hiển thị trang đăng nhập

@app.route("/product")
def product():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Truy vấn các sản phẩm theo loại 'dog', 'cat', và 'pettag'
        cur.execute("SELECT * FROM products WHERE category = 'dog'")
        dog_products = cur.fetchall()
        
        cur.execute("SELECT * FROM products WHERE category = 'cat'")
        cat_products = cur.fetchall()
        
        cur.execute("SELECT * FROM products WHERE category = 'pettag'")
        pettags = cur.fetchall()
        
        # Truy vấn các sản phẩm có giá khuyến mãi (giảm giá)
        cur.execute("SELECT * FROM products WHERE category = 'promotion'")
        promotions = cur.fetchall()
    
    except Exception as e:
        print(f"Đã có lỗi khi truy vấn dữ liệu sản phẩm: {e}")
        dog_products = []
        cat_products = []
        pettags = []
        promotions = []
    
    cur.close()
    conn.close()
    
    return render_template('product.html', dog_products=dog_products, 
                                            cat_products=cat_products, 
                                            pettags=pettags, 
                                            promotions=promotions)

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Thêm kết nối cơ sở dữ liệu
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Cố gắng thực hiện truy vấn
            cur.execute('INSERT INTO account (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()  # Lưu thay đổi
            flash('Đăng ký thành công! Bạn có thể đăng nhập ngay.')  # Thông báo thành công
            return redirect(url_for('login'))  # Chuyển đến trang đăng nhập
        except Exception as e:
            conn.rollback()  # Nếu có lỗi, hoàn tác giao dịch
            flash(f'Đã có lỗi xảy ra: {e}')  # Hiển thị lỗi
        finally:
            cur.close()  # Đóng con trỏ
            conn.close()  # Đóng kết nối

    return render_template("register.html")  # Hiển thị trang đăng ký

# Route hiển thị trang productmanager.html
@app.route("/products")
def product_manager():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, old_price, new_price FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()
    print(products)
    return render_template("productmanager.html", products=products)


# Route để thêm mới sản phẩm
@app.route('/add_products', methods=['POST'])
def add_products():
    data = request.form
    picture = data.get('picture', 'static/image/Profile Icon.webp')
    name = data['name']
    category = data['category']
    old_price = data['old_price']
    new_price = data['new_price']

    image = request.files['image']
    if image:
        # Lưu ảnh vào thư mục static/uploads
        filename = secure_filename(image.filename)  # Đảm bảo tên file an toàn
        image_path = os.path.join('static/uploads', filename)  # Đường dẫn đầy đủ để lưu ảnh
        image.save(image_path)  # Lưu ảnh vào thư mục
        picture = image_path  # Cập nhật đường dẫn ảnh


    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (picture, name, category, old_price, new_price) VALUES (%s, %s, %s, %s, %s)",
                (picture, name, category, old_price, new_price))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('product_manager'))

# Route để cập nhật sản phẩm
@app.route('/edit_products/<int:id>', methods=['GET', 'POST'])
def edit_products(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        try:
            # Get data from the request body
            data = request.get_json()

            # Execute the SQL query with the data received from the client
            cur.execute("""
                UPDATE products 
                SET name = %s, category = %s, old_price = %s, new_price = %s
                WHERE id = %s
            """, (data['name'], data['category'], data['old_price'], data['new_price'], id))
            
            conn.commit()  # Commit the transaction
            return jsonify({"success": True})
        
        except Exception as e:
            conn.rollback()  # Rollback on error
            return jsonify({"success": False, "error": str(e)})
        
        finally:
            cur.close()
            conn.close()

    else:
        # Fetch product data to display in the form
        cur.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        
        if product:
            # Convert the product tuple to a dictionary, handling memoryview if present
            product_dict = {
                'id': product[0] if not isinstance(product[0], memoryview) else product[0].tobytes().decode('utf-8'),
                'picture': product[1] if not isinstance(product[1], memoryview) else product[1].tobytes().decode('utf-8'),
                'name': product[2] if not isinstance(product[2], memoryview) else product[2].tobytes().decode('utf-8'),
                'category': product[3] if not isinstance(product[3], memoryview) else product[3].tobytes().decode('utf-8'),
                'old_price': product[4] if not isinstance(product[4], memoryview) else product[4].tobytes().decode('utf-8'),
                'new_price': product[5] if not isinstance(product[5], memoryview) else product[5].tobytes().decode('utf-8')
            }
            return jsonify(product_dict)
        else:
            return jsonify({'error': 'Product does not exist'})

@app.route('/delete_products/<int:id>', methods=['POST'])
def delete_products(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('product_manager'))

#Giỏ hàng

@app.route('/add_to_cart/<int:product_id>', methods=['POST' ,'GET'])
def add_to_cart(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT name, new_price FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    
    if product:
        name, price = product
        cur.execute(
            "INSERT INTO cart (product_id, name, quantity, price) VALUES (%s, %s,%s, %s)",
            (product_id, name,1, price)
        )
        conn.commit()
    
    cur.close()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, quantity FROM cart")
    items = cur.fetchall()
    total_price = sum(float(item[2]) * int(item[3]) for item in items)
    cur.close()
    conn.close()
    
    return render_template('cart.html', items=items, total_price=total_price)

@app.route('/update_cart/<int:id>', methods=['POST','GET'])
def update_cart(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        try:
            # Get data from the request body
            data = request.get_json()  # Lấy dữ liệu từ request (json)
            quantity = data.get('quantity')

            # Kiểm tra xem số lượng có hợp lệ không (là số và lớn hơn 0)
            cur.execute("""
                UPDATE cart 
                SET quantity = %s 
                WHERE id = %s
            """, (quantity,id))

            conn.commit()  # Commit giao dịch

            return jsonify({"success": True})

        except Exception as e:
            conn.rollback()  # Rollback nếu có lỗi
            return jsonify({"success": False, "error": str(e)})
        finally:
            cur.close()
            conn.close()

    elif request.method == "GET":
            # Lấy thông tin sản phẩm từ giỏ hàng
            cur.execute("SELECT * FROM cart WHERE id = %s", (id,))
            items = cur.fetchone()
            cur.close()
            conn.close()

            if items:
                item_dict = {
                'id': items[0] ,
                'quantity': items[2] 
            }
                return jsonify(item_dict)

            else:
                return jsonify({'error': 'Sản phẩm không tồn tại trong giỏ hàng'})

@app.route('/delete_from_cart/<int:id>', methods=['POST'])
def delete_from_cart(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('cart'))


#Checkout

@app.route('/checkout', methods=['POST'])
def checkout():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM cart")
    conn.commit() 
    
    cur.close()
    conn.close()
    flash("Thanh toán thành công!", "success")  
    return redirect(url_for('cart'))  

if __name__ == "__main__":
    app.run(debug=True),