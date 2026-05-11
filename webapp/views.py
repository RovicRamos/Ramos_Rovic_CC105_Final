from django.shortcuts import render
import pickle
import pandas as pd
import os
from django.conf import settings

# Load model
BASE_DIR = settings.BASE_DIR
with open(os.path.join(BASE_DIR, 'best_bike_model.pkl'), 'rb') as f:
    model = pickle.load(f)
with open(os.path.join(BASE_DIR, 'model_columns.pkl'), 'rb') as f:
    model_columns = pickle.load(f)

def home(request):
    # Default values for when the page first loads
    default_values = {
        'hour': 12, 'temp': 20.0, 'humidity': 50, 'wind': 1.5,
        'vis': 2000, 'dew': 10.0, 'solar': 1.0, 'rain': 0.0, 'snow': 0.0,
        'season': 'Spring', 'holiday': 'No Holiday', 'functioning': 'Yes'
    }

    if request.method == 'POST':
        # Create a dictionary of 0s for all model columns
        input_data = {col: 0 for col in model_columns}
        
        # 1. Grab inputs (same as before)
        input_data['Hour'] = int(request.POST.get('hour', 0))
        input_data['Temperature(°C)'] = float(request.POST.get('temp', 0))
        input_data['Humidity(%)'] = float(request.POST.get('humidity', 0))
        input_data['Wind speed (m/s)'] = float(request.POST.get('wind', 0))
        input_data['Visibility (10m)'] = float(request.POST.get('vis', 0))
        input_data['Dew point temperature(°C)'] = float(request.POST.get('dew', 0))
        input_data['Solar Radiation (MJ/m2)'] = float(request.POST.get('solar', 0))
        input_data['Rainfall(mm)'] = float(request.POST.get('rain', 0))
        input_data['Snowfall (cm)'] = float(request.POST.get('snow', 0))
        
        # 2. Categorical mapping (same as before)
        season = request.POST.get('season')
        if f'Seasons_{season}' in input_data: input_data[f'Seasons_{season}'] = 1
        holiday = request.POST.get('holiday')
        if f'Holiday_{holiday}' in input_data: input_data[f'Holiday_{holiday}'] = 1
        functioning = request.POST.get('functioning')
        if f'Functioning Day_{functioning}' in input_data: input_data[f'Functioning Day_{functioning}'] = 1

        # Predict
        df_pred = pd.DataFrame([input_data])
        result = model.predict(df_pred)[0]
        prediction = max(0, int(result))

        # IMPORTANT: Pass the submitted POST data back to the template to keep the values!
        return render(request, 'index.html', {'prediction': prediction, 'values': request.POST})
    
    # If it's a GET request (first load or reset), send the default values
    return render(request, 'index.html', {'values': default_values})