# 🛒 UrbanShop

UrbanShop is a simple e-commerce web application developed using **Python**, **Streamlit**, and **Supabase**. It allows users to browse products, manage their wishlist and cart, place orders, and update their profile. The application also includes an Admin Dashboard for product management.

---

## 🚀 Features

### 👤 User Module
- User Registration & Login
- Product Search
- Category Filter
- Product Sorting
- Wishlist Management
- Shopping Cart
- Checkout
- Order History
- Profile Management
- Logout

### 🛠️ Admin Module
- Secure Admin Access (Role-Based)
- Dashboard Statistics
- Add New Products
- Edit Products
- Delete Products
- Upload Product Images (Supabase Storage)

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- Supabase (PostgreSQL)

### Authentication
- Supabase Authentication

### Storage
- Supabase Storage

---

## 📂 Database Tables

- products
- profiles
- categories
- wishlist
- cart
- orders

---

## 📁 Project Structure

```
UrbanShop/
│
├── app.py
├── requirements.txt
├── .env
│
├── database/
│   └── supabase.py
│
├── utils/
│   ├── database.py
│   └── storage.py
│
├── pages/
│   ├── 1_Login.py
│   ├── 2_Signup.py
│   ├── 3_Home.py
│   ├── 4_Profile.py
│   ├── 5_Wishlist.py
│   ├── 6_Cart.py
│   ├── 7_Admin.py
│   ├── 9_Checkout.py
│   └── 10_Order_History.py
│
└── assets/
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/shravani-mahadik/UrbanShop.git
```

### Go to project folder

```bash
cd UrbanShop
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create `.env`

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### Run the application

```bash
streamlit run app.py
```

---

## 👨‍💻 User Workflow

1. Register/Login
2. Browse Products
3. Search & Filter Products
4. Add Products to Wishlist
5. Move Products to Cart
6. Checkout
7. View Order History
8. Update Profile

---

## 👨‍💼 Admin Workflow

1. Login as Admin
2. View Dashboard Statistics
3. Add Products
4. Upload Product Images
5. Edit Product Details
6. Delete Products


## 🔮 Future Enhancements

- Product Reviews & Ratings
- Payment Gateway Integration
- Email Notifications
- Order Tracking
- Sales Analytics Dashboard
- Responsive Mobile UI

---

## 👩‍💻 Developed By

**Shravani Mahadik**

Computer Engineering Student

---

## 📄 License

This project is developed for educational and internship purposes.
