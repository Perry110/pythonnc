# Sử dụng Python image
FROM python:3.10

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép các file yêu cầu (requirements.txt) vào container và cài đặt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Sao chép mã nguồn ứng dụng vào container
COPY . /app

# Đặt biến môi trường cho Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose port mà Flask sẽ chạy
EXPOSE 5000

# Chạy ứng dụng
CMD ["flask", "run", "--host=0.0.0.0"]