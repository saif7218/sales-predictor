import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from autogluon.tabular import TabularPredictor
import logging
from pathlib import Path
import time
import sys

# Setup logging
log_dir = Path("../logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sales Prediction API", version="1.0")

# Load model at startup
MODEL_PATH = "../models/autogluon_model"
if not Path(MODEL_PATH).exists():
    logger.error(f"Model not found at {MODEL_PATH}")
    sys.exit(1)

predictor = TabularPredictor.load(MODEL_PATH)
logger.info("AutoGluon model loaded successfully")

# Define expected input schema
class PredictionInput(BaseModel):
    Benefit_per_order: float
    Order_Item_Discount: float
    Order_Item_Discount_Rate: float
    Order_Item_Product_Price: float
    Order_Item_Profit_Ratio: float
    Order_Item_Quantity: int
    Product_Price: float
    Days_for_shipping_real: int
    Days_for_shipment_scheduled: int
    Type: str
    Category_Name: str
    Customer_Segment: str
    Market: str
    Order_Region: str
    Shipping_Mode: str

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([input_data.model_dump()])
        
        # Rename columns to match training data
        df.columns = [
            "Benefit per order", "Order Item Discount", "Order Item Discount Rate",
            "Order Item Product Price", "Order Item Profit Ratio", "Order Item Quantity",
            "Product Price", "Days for shipping (real)", "Days for shipment (scheduled)",
            "Type", "Category Name", "Customer Segment", "Market", "Order Region", "Shipping Mode"
        ]
        
        # Predict
        start = time.time()
        pred = predictor.predict(df)
        inference_time = time.time() - start
        
        result = float(pred[0])
        logger.info(f"Prediction: {result:.2f} | Time: {inference_time:.4f}s")
        
        return {
            "Sales_per_customer": result,
            "inference_time_ms": round(inference_time * 1000, 2)
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
