import streamlit as st
import requests
import json

st.set_page_config(page_title="Sales Predictor", layout="centered")
st.title("📊 Sales per Customer Predictor")
st.markdown("Enter order details to predict the expected sales per customer.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        benefit = st.number_input("Benefit per order", value=91.25)
        discount = st.number_input("Order Item Discount", value=13.11)
        discount_rate = st.number_input("Discount Rate", value=0.04)
        product_price_item = st.number_input("Order Item Product Price", value=327.75)
        profit_ratio = st.number_input("Profit Ratio", value=0.29)
        quantity = st.number_input("Quantity", value=1, step=1)
        product_price = st.number_input("Product Price", value=327.75)
    with col2:
        days_real = st.number_input("Days shipping (real)", value=3, step=1)
        days_sched = st.number_input("Days shipping (scheduled)", value=4, step=1)
        pay_type = st.selectbox("Payment Type", ["DEBIT", "TRANSFER", "CASH", "PAYMENT"])
        category = st.selectbox("Category", ["Sporting Goods", "Electronics", "Clothing"])
        segment = st.selectbox("Customer Segment", ["Consumer", "Corporate", "Home Office"])
        market = st.selectbox("Market", ["Pacific Asia", "Europe", "US", "LATAM"])
        region = st.selectbox("Region", ["Southeast Asia", "South Asia", "Oceania"])
        shipping = st.selectbox("Shipping Mode", ["Standard Class", "First Class", "Same Day"])

    submitted = st.form_submit_button("Predict Sales")

if submitted:
    payload = {
        "Benefit_per_order": benefit,
        "Order_Item_Discount": discount,
        "Order_Item_Discount_Rate": discount_rate,
        "Order_Item_Product_Price": product_price_item,
        "Order_Item_Profit_Ratio": profit_ratio,
        "Order_Item_Quantity": int(quantity),
        "Product_Price": product_price,
        "Days_for_shipping_real": int(days_real),
        "Days_for_shipment_scheduled": int(days_sched),
        "Type": pay_type,
        "Category_Name": category,
        "Customer_Segment": segment,
        "Market": market,
        "Order_Region": region,
        "Shipping_Mode": shipping
    }
    try:
        response = requests.post("http://localhost:8000/predict", json=payload)
        result = response.json()
        st.success(f"Predicted Sales per Customer: **${result['Sales_per_customer']:.2f}**")
        st.caption(f"Inference time: {result['inference_time_ms']} ms")
    except Exception as e:
        st.error(f"API error: {e}")
