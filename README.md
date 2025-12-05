# 🚗 SMART-DATABASE - AI-Powered Used Car Database Assistant

An intelligent Flask web application that uses LangGraph and LLMs (Groq/OpenAI) to answer natural language questions about a used car database. The app features a beautiful, animated UI and a powerful SQL agent that can understand and respond to complex queries.

> **🚀 Ready to Deploy?** Choose your platform:
> 
> - **🚂 Railway** (Recommended): [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) - $5 free credit, auto-deploy from GitHub
> - **🌟 Render.com**: [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Free tier with 750 hours/month
> - **⚡ Quick start**: [QUICKSTART.md](QUICKSTART.md) - 5-minute guide for all platforms

## ✨ Features

- 🤖 **AI-Powered SQL Agent**: Uses LangGraph to intelligently query a SQLite database
- 💬 **Natural Language Interface**: Ask questions in plain English
- 📊 **Comprehensive Car Data**: Contains data from multiple car brands (Audi, BMW, Ford, Toyota, Mercedes, and more)
- 🎨 **Beautiful UI**: Animated gradient background with floating car emojis
- 🔄 **Conversation Memory**: Maintains context across multiple questions
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API key from either:
  - [Groq](https://console.groq.com/) (Recommended - Free tier available)
  - [OpenAI](https://platform.openai.com/) (Alternative)

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/ROMAN-AHMAD-NAZAR/SMART-DATABASE.git
cd SMART-DATABASE
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API key (GROQ_API_KEY or OPENAI_API_KEY)
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
```
http://localhost:5000
```

## 🌐 Deployment Options

### Option 1: Deploy to Heroku

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create a new Heroku app**:
```bash
heroku create your-app-name
```

3. **Set environment variables**:
```bash
heroku config:set GROQ_API_KEY=your_api_key_here
heroku config:set FLASK_ENV=production
```

4. **Deploy**:
```bash
git push heroku main
```

5. **Open the app**:
```bash
heroku open
```

### Option 2: Deploy to Render.com

1. **Create a new account** on [Render.com](https://render.com)

2. **Click "New +"** and select **"Web Service"**

3. **Connect your GitHub repository**

4. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`

5. **Add environment variables**:
   - `GROQ_API_KEY`: Your API key
   - `FLASK_ENV`: production
   - `FLASK_DEBUG`: False

6. **Click "Create Web Service"**

Alternatively, you can use the included `render.yaml` file for automated deployment.

### Option 3: Deploy to Railway

1. **Create a new account** on [Railway.app](https://railway.app)

2. **Click "New Project"** and select **"Deploy from GitHub repo"**

3. **Connect your repository**

4. **Add environment variables** in the Variables tab:
   - `GROQ_API_KEY`: Your API key
   - `FLASK_ENV`: production

5. **Deploy** - Railway will automatically detect the Python app and deploy it

### Option 4: Deploy to PythonAnywhere

1. **Sign up** at [PythonAnywhere.com](https://www.pythonanywhere.com)

2. **Open a Bash console** and clone your repo:
```bash
git clone https://github.com/ROMAN-AHMAD-NAZAR/SMART-DATABASE.git
cd SMART-DATABASE
pip install --user -r requirements.txt
```

3. **Create a web app** from the Web tab

4. **Configure WSGI file** to point to your app

5. **Set environment variables** in the web app configuration

6. **Reload** the web app

## 📊 Database Information

The application includes a pre-built SQLite database (`cars.db`) with data from multiple car brands:
- Audi
- BMW
- Ford
- Toyota
- Mercedes
- Skoda
- Hyundai
- Vauxhall
- Volkswagen

### Rebuilding the Database

If you need to rebuild the database from the CSV files:

1. Update the path in `create_db.py`:
```python
CSV_FOLDER_PATH = '/path/to/CSV_DATASET'
```

2. Run the script:
```bash
python create_db.py
```

## 🔒 Security Notes

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- Use environment variables for all sensitive configuration
- Keep your API keys secure and rotate them regularly

## 💡 Example Queries

Try asking questions like:
- "What's the average price of Toyota cars?"
- "Show me the most fuel-efficient cars"
- "Which BMW models are available?"
- "What's the price range for Ford cars from 2018?"
- "List all cars with mileage under 50,000"

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **AI/ML**: LangChain, LangGraph, Groq/OpenAI LLMs
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn (WSGI server)

## 📁 Project Structure

```
SMART-DATABASE/
├── app.py                 # Flask application entry point
├── Agent.py              # LangGraph SQL agent implementation
├── cars.db               # SQLite database
├── create_db.py          # Database creation script
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment configuration
├── render.yaml          # Render.com deployment configuration
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── templates/
│   └── index.html       # Web interface
└── CSV_DATASET/         # Source CSV files
    ├── audi.csv
    ├── bmw.csv
    ├── ford.csv
    └── ...
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### "No API key found" error
- Ensure you've created a `.env` file with either `GROQ_API_KEY` or `OPENAI_API_KEY`
- Check that the `.env` file is in the root directory of the project

### Database connection error
- Ensure `cars.db` exists in the root directory
- If missing, run `python create_db.py` to recreate it

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try creating a fresh virtual environment

### Deployment issues
- Check that all environment variables are set correctly on your hosting platform
- Ensure the PORT environment variable is properly configured
- Verify that gunicorn is installed (should be in requirements.txt)

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ using Flask, LangGraph, and AI