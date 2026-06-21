from prophet import Prophet
import pandas as pd
from typing import Dict, List
import os

class ExpenseForecaster:
    def __init__(self):
        self.models = {}
    
    def prepare_data(self, dates: List, amounts: List) -> pd.DataFrame:
        """Prepare data for Prophet"""
        df = pd.DataFrame({
            'ds': pd.to_datetime(dates),
            'y': amounts
        })
        return df.sort_values('ds')
    
    def train_forecast_model(self, category: str, dates: List, amounts: List):
        """Train forecast model for a category"""
        if len(dates) < 10:  # Need minimum data points
            return
        
        df = self.prepare_data(dates, amounts)
        
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            interval_width=0.95
        )
        
        with open(os.devnull, 'w') as f:
            model.fit(df)
        
        self.models[category] = model
    
    def forecast(self, category: str, periods: int = 30) -> Dict:
        """Generate forecast for a category"""
        if category not in self.models:
            return None
        
        model = self.models[category]
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        return {
            'dates': forecast['ds'].tolist(),
            'predictions': forecast['yhat'].tolist(),
            'lower_bound': forecast['yhat_lower'].tolist(),
            'upper_bound': forecast['yhat_upper'].tolist()
        }
    
    def forecast_total_expenses(self, dates: List, amounts: List, periods: int = 30) -> Dict:
        """Forecast total expenses"""
        if len(dates) < 10:
            return None
        
        df = self.prepare_data(dates, amounts)
        
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        with open(os.devnull, 'w') as f:
            model.fit(df)
        
        with open('/dev/null', 'w') as f:
            model.fit(df)
        
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        return {
            'dates': forecast['ds'].tolist(),
            'predictions': forecast['yhat'].tolist(),
            'lower_bound': forecast['yhat_lower'].tolist(),
            'upper_bound': forecast['yhat_upper'].tolist()
        }
