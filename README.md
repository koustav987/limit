# 🌱 Crop Yield Predictor

A complete web application for predicting crop yields using machine learning. Built with Flask backend API and React frontend interface.

## 📋 Features

- **Machine Learning Prediction**: Uses Random Forest and Linear Regression models
- **Interactive Web Interface**: Modern React-based UI with real-time predictions
- **RESTful API**: Flask backend with comprehensive endpoints
- **Data Validation**: Input validation and error handling
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Status**: API connection monitoring
- **Multiple Prediction Modes**: Single and bulk predictions

## 🏗️ Architecture

```
Crop Yield Predictor
├── Backend (Flask API)
│   ├── Machine Learning Models
│   ├── Data Processing
│   └── REST API Endpoints
└── Frontend (React)
    ├── Interactive Forms
    ├── Real-time Predictions
    └── Results Visualization
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (with pip)
- **Node.js 14+** (with npm)
- **Git** (optional)

### Option 1: Automated Setup (Recommended)

1. **Download the setup script** and make it executable:
```bash
chmod +x setup.sh
./setup.sh
```

2. **Copy the application files**:
```bash
# Copy Flask backend code to backend/app.py
# Copy React component code to frontend/src/App.tsx
```

3. **Start the application**:
```bash
./start_all.sh
```

### Option 2: Manual Setup

#### Backend Setup

1. **Create project directory**:
```bash
mkdir crop-yield-predictor
cd crop-yield-predictor
```

2. **Setup Flask backend**:
```bash
mkdir backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install Flask Flask-CORS pandas numpy scikit-learn joblib matplotlib seaborn gunicorn

# Save requirements
pip freeze > requirements.txt
```

3. **Create app.py** with the Flask backend code provided above.

#### Frontend Setup

1. **Setup React frontend**:
```bash
cd ../
npx create-react-app frontend
cd frontend

# Install additional dependencies
npm install lucide-react
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind
npx tailwindcss init -p
```

2. **Configure Tailwind CSS** in `tailwind.config.js`:
```javascript
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

3. **Update src/index.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

4. **Replace src/App.js** with the React component code provided above.

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend directory:
```env
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
MODEL_PATH=./crop_yield_model.pkl
```

### API Configuration

The backend API runs on `http://localhost:5000` by default. Update the `API_BASE_URL` in the React frontend if needed.

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Returns API status and model availability.

### Get Feature Options
```http
GET /features
```
Returns available options for categorical features and ranges for numerical features.

### Single Prediction
```http
POST /predict
Content-Type: application/json

{
  "Area": "Punjab",
  "Crop": "Wheat",
  "Soil_Type": "Loamy",
  "Temperature": 25.5,
  "Humidity": 65.0,
  "PH": 6.5,
  "Annual_Rainfall": 850
}
```

### Bulk Predictions
```http
POST /bulk_predict
Content-Type: application/json

{
  "predictions": [
    {
      "Area": "Punjab",
      "Crop": "Wheat",
      ...
    },
    {
      "Area": "Haryana",
      "Crop": "Rice",
      ...
    }
  ]
}
```

## 🎯 Usage

1. **Start the application**:
   - Run `./start_all.sh` for both services
   - Or start individually with `./start_backend.sh` and `./start_frontend.sh`

2. **Access the application**:
   - Frontend UI: http://localhost:3000
   - Backend API: http://localhost:5000

3. **Make predictions**:
   - Fill in the form with crop and environmental data
   - Click "Predict Yield" to get results
   - View detailed predictions and input summary

## 📊 Input Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| Area | Categorical | Geographic region | Punjab, Haryana |
| Crop | Categorical | Type of crop | Wheat, Rice, Maize |
| Soil Type | Categorical | Soil classification | Loamy, Clay, Sandy |
| Temperature | Numerical | Average temperature (°C) | 25.5 |
| Humidity | Numerical | Relative humidity (%) | 65.0 |
| pH | Numerical | Soil pH level | 6.5 |
| Annual Rainfall | Numerical | Total rainfall (mm) | 850 |

## 🐳 Docker Deployment

### Build and run with Docker Compose:

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Individual Docker commands:

```bash
# Build backend image
docker build -t crop-yield-backend .

# Run backend container
docker run -p 5000:5000 crop-yield-backend
```

## 🧪 Testing

### Backend API Testing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test prediction endpoint
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"Area":"Punjab","Crop":"Wheat","Soil_Type":"Loamy","Temperature":25.5,"Humidity":65.0,"PH":6.5,"Annual_Rainfall":850}'
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Ensure Flask backend is running on port 5000
   - Check CORS configuration
   - Verify API_BASE_URL in frontend

2. **Model Loading Error**:
   - Ensure all dependencies are installed
   - Check model file permissions
   - Verify scikit-learn version compatibility

3. **Frontend Build Errors**:
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

4. **Port Conflicts**:
   - Change backend port in app.py
   - Update API_BASE_URL in frontend
   - Check for other services using ports 3000/5000

### Debug Mode

Enable debug mode for detailed error messages:
```bash
# Backend
export FLASK_DEBUG=True
python app.py

# Frontend
npm start
```

## 📁 Project Structure

```
crop-yield-predictor/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── crop_yield_model.pkl   # Trained model (generated)
│   └── venv/                  # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main React component
│   │   └── index.css         # Tailwind CSS
│   ├── public/
│   └── package.json          # Node.js dependencies
├── docker-compose.yml        # Docker services
├── Dockerfile               # Backend container
├── start_all.sh            # Launch script
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Scikit-learn for machine learning algorithms
- Flask for the web framework
- React for the frontend framework
- Tailwind CSS for styling
- Lucide React for icons

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Create an issue in the repository

---

**Made with ❤️ for sustainable agriculture** 🌾