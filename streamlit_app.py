import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Title of the application
st.title("Motorcycle Price Prediction App")

# Header
st.header("Predict the Price of Your Motorcycle")

# Subheader
st.subheader("Find out the price and value of your motorcycle using this app.")

# Kullanıcıyı bilgilendiren bir resim ekleyelim
from PIL import Image
import streamlit as st

# Aynı dizinde bir görsel
image = Image.open("Motorcycle.jpg")
st.image(image, caption="Motorcycle", width=400)

# Gerekli dosyaları yükleyelim
top_6_feature_names = joblib.load("top_6_feature_names.joblib")

# Modeli yükleme (Eğer bir modeliniz varsa buraya ekleyin)
# with open('bike_price_model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

def predict_price(seller_type, owner, km_driven, year, name, engine_capacity, fuel_type, color):
    # Base fiyat
    base_price = 45000

    # Fiyat hesaplama
    price = base_price

    # Satıcı türü etkisi
    if seller_type == "Dealer":
        price += 3000  # Dealer fiyatları genellikle daha yüksek

    # Sahiplik etkisi
    if owner == "2nd owner":
        price -= 1500
    elif owner == "3rd owner":
        price -= 3000
    elif owner == "4th owner ve üstü":
        price -= 4500

    # Km etkisi
    price -= int(km_driven) * 0.5  # Km başına 0.5 TL düşüş

    # Model yılı etkisi (Daha eski modeller genellikle daha ucuzdur)
    price -= (2025 - int(year)) * 1000  # Yıl farkı başına 1000 TL düşüş

    # Motor hacmi etkisi
    price += (int(engine_capacity) * 100)  # Motor hacmi arttıkça fiyat artar

    # Yakıt türü etkisi
    if fuel_type == "Electric":
        price += 5000  # Elektrikli motosikletler daha pahalı olabilir
    elif fuel_type == "Diesel":
        price += 1000  # Dizel motorlar genellikle daha ucuz olabilir

    # Renk etkisi
    if color == "Red":
        price += 2000  # Kırmızı renk popüler ve fiyatı arttırabilir
    elif color == "Black":
        price += 1500  # Siyah renk oldukça popüler, hafif fiyat artışı
    elif color == "Blue":
        price += 1000  # Mavi renk popüler ve fiyatı hafif arttırabilir
    elif color == "White":
        price -= 500   # Beyaz renk bazen daha ucuz olabilir
    elif color == "Silver":
        price -= 1000  # Gümüş renk bazen daha ucuz olabilir
    elif color == "Green":
        price -= 1500  # Yeşil gibi daha az tercih edilen renkler fiyatı düşürebilir
    elif color == "Yellow":
        price -= 2000  # Sarı gibi nadir renkler genellikle daha ucuz olabilir

    # Model etkisi (Bazı modeller daha pahalı olabilir)
    if name in ["CBR 1000RR", "R1", "Hayabusa"]:
        price += 10000  # Performans motosikletleri daha pahalı olabilir
    elif name in ["CB Shine", "FZ S V3", "Pulsar 150"]:
        price -= 5000  # Daha ekonomik modeller genellikle daha ucuz

    return price

# Motosiklet markaları ve modelleri
bike_models = {
    "Honda": ["CBR 1000RR", "CBR 500R", "CB Shine", "CBR 150R"],
    "Yamaha": ["YZF-R15", "FZ S V3", "FZ25", "R1"],
    "Suzuki": ["Gixxer", "GSX-R1000", "Hayabusa"],
    "Kawasaki": ["Ninja 300", "Z900", "Versys 650"],
    "Bajaj": ["Pulsar NS200", "Pulsar 150", "Dominar 400"],
    "Royal Enfield": ["Classic 350", "Bullet 350", "Himalayan", "Interceptor 650"]
}

# Kullanıcının gireceği parametreler
brand = st.selectbox("Select Brand", list(bike_models.keys()))
model = st.selectbox("Select Model", bike_models[brand])
seller_type = st.selectbox("Seller Type", ["Individual", "Dealer"])
owner = st.selectbox("Which Owner", ["1st owner", "2nd owner", "3rd owner", "4th owner ve üstü"])
km_driven = st.text_input("Mileage Information", "5650")
year = st.text_input("Model Year (For example: 2016)", "2020")
engine_capacity = st.selectbox("engine capacity (in cc)", ["100", "125", "150", "200", "250", "300", "350", "400"])
fuel_type = st.selectbox("Fuel Type", ["Petroleum", "Electric", "Diesel"])
color = st.selectbox("Color", ["Red", "Black", "Blue", "White", "Silver", "Green", "Yellow"])

# Fiyat hesaplamasını başlatacak buton
if st.button("Calculate Predicted Price"):
    predicted_price = predict_price(seller_type, owner, km_driven, year, model, engine_capacity, fuel_type, color)
    st.write(f"Predicted Sales Price: {predicted_price} TL")



