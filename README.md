# Crop Yield Predictor Web Application

This web application deploys your crop yield prediction model trained in Google Colab as a user-friendly web interface.

## 📁 Project Structure

```
crop-yield-webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── crop_yield_model.pkl  # Your trained model (from Colab)
├── templates/
│   ├── index.html        # Main input form
│   └── result.html       # Prediction results page
└── uploads/              # Directory for file uploads
```

## 🚀 Deployment Options

### Option 1: Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy Your Model**
   - Download `crop_yield_model.pkl` from your Colab environment
   - Place it in the project root directory

3. **Run the Application**
   ```bash
   python app.py
   ```
   
4. **Access the App**
   - Open your browser and go to `http://localhost:5000`

### Option 2: Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t crop-yield-app .
   ```

2. **Run Container**
   ```bash
   docker run -p 5000:5000 crop-yield-app
   ```

### Option 3: Cloud Deployment (Heroku)

1. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add Procfile**
   Create a file named `Procfile` with:
   ```
   web: gunicorn app:app
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy crop yield predictor"
   git push heroku main
   ```

### Option 4: Cloud Deployment (Railway/Render)

1. **Railway:**
   - Connect your GitHub repository to Railway
   - Railway will automatically detect Python and deploy

2. **Render:**
   - Connect your GitHub repository to Render
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`

## 📋 Features

### Web Interface
- **User-friendly Form**: Enter crop and environmental parameters
- **Real-time Predictions**: Get instant yield predictions
- **Responsive Design**: Works on desktop and mobile devices
- **Input Validation**: Ensures data quality before prediction

### API Endpoints
- `GET /` - Main prediction form
- `POST /predict` - Web form submission
- `POST /api/predict` - JSON API for programmatic access
- `POST /upload_model` - Upload new model files

### API Usage Example
```python
import requests
import json

url = "http://your-app-url.com/api/predict"
data = {
    "Area": "Punjab",
    "Crop": "Wheat",
    "Soil_Type": "Loamy",
    "Temperature": 27.5,
    "Humidity": 60.2,
    "PH": 6.5,
    "Annual_Rainfall": 850
}

response = requests.post(url, json=data)
result = response.json()
print(f"Predicted Yield: {result['prediction']}")
```

## 🔧 Configuration

### Environment Variables
You can set these environment variables for production:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

### Model Updates
- Use the `/upload_model` endpoint to update the model without redeploying
- Or replace `crop_yield_model.pkl` and restart the application

## 📊 Model Information

The application expects a scikit-learn pipeline with:
- **Preprocessing**: OneHotEncoder for categorical features, StandardScaler for numerical
- **Model**: Any regression model (Linear Regression, Random Forest, etc.)
- **Input Features**: Area, Crop, Soil_Type, Temperature, Humidity, PH, Annual_Rainfall
- **Output**: Predicted yield value

## 🛠️ Troubleshooting

### Common Issues

1. **Model File Not Found**
   - Ensure `crop_yield_model.pkl` is in the project root
   - Check file permissions

2. **Import Errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.7+)

3. **Prediction Errors**
   - Ensure input data matches training data format
   - Check for missing categorical values in the model's encoder

4. **Port Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

### Performance Optimization

1. **Caching**: Implement Redis caching for frequent predictions
2. **Load Balancing**: Use multiple Gunicorn workers
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
   ```
3. **Database**: Store predictions in a database for analytics

## 📈 Monitoring

Add logging and monitoring:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Add to your Flask routes
app.logger.info(f"Prediction made: {prediction}")
```

## 🔒 Security Considerations

1. **Input Validation**: All inputs are validated before processing
2. **File Upload Security**: Only .pkl files allowed for model uploads
3. **Rate Limiting**: Consider adding rate limiting for production
4. **HTTPS**: Always use HTTPS in production

## 📝 License

This project is open-source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Flask and scikit-learn documentation
- Open an issue in the repository