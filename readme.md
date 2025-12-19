# 📊 Etsy Dashboard - Frontend

Free Etsy analytics dashboard with Finance, Customer Intelligence, and SEO insights for Etsy sellers.

![Etsy Dashboard](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)

## 🎯 Overview

This is the **frontend application** for Etsy Dashboard - a comprehensive analytics platform that helps Etsy sellers:
- 💰 Track **real profit margins** after ALL Etsy fees
- 👥 Analyze **customer behavior** and lifetime value
- 🔍 Optimize **SEO** for better Etsy search rankings

**Live Demo:** [etsydashboard.com](https://etsydashboard.com) *(to be deployed)*

---

## 🚀 Features

### Public Landing Pages (SEO Optimized)
- **Home** (`/`) - Main landing page with dashboard overview
- **Fee Calculator** (`/calculate-etsy-fees`) - Free Etsy fees calculator
- **Product Comparison** (`/etsy-analytics-tool`) - Compare with competitors

### Protected Dashboards (Authentication Required)
- **Finance Pro** - Real profit tracking, fee breakdowns, ROI analysis
- **Customer Intelligence** - LTV, geographic data, retention metrics
- **SEO Analyzer** - Listing scores, optimization tips, keyword analysis

### Premium Features
- Unlimited analyses (vs 10/week free)
- AI-powered recommendations
- Priority optimization lists
- Advanced profitability insights

---

## 📁 Project Structure

```
etsydashboard-frontend/
│
├── .streamlit/              # Streamlit configuration
│   ├── config.toml          # UI theme & server settings
│   └── secrets.toml.example # Template for API keys
│
├── pages/                   # Protected app pages
│   ├── auth.py              # Signup/Login
│   ├── 1_📊_Dashboard.py   # Main dashboard hub
│   └── 2_✨_Premium.py     # Upgrade & subscription
│
├── landings/                # SEO landing pages (public)
│   ├── calculate_fees.py    # Free calculator
│   └── analytics_tool.py    # Product comparison
│
├── components/              # Reusable UI components
│   ├── seo_meta.py          # Meta tags & schema markup
│   ├── calculators.py       # Fee calculators, scenarios
│   ├── charts.py            # Plotly visualizations
│   └── ui_elements.py       # Headers, CTAs, cards
│
├── utils/                   # Utility functions
│   ├── helpers.py           # Formatting, validation, calculations
│   └── api_client.py        # Backend API communication
│
├── assets/                  # Static files
│   └── .gitkeep
│
├── Home.py                  # 🏠 Main entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

**Total:** ~5,590 lines of Python code

---

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/etsydashboard-frontend.git
cd etsydashboard-frontend
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Secrets
```bash
# Copy example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit with your values
nano .streamlit/secrets.toml
```

**Required secrets:**
```toml
[api]
backend_url = "https://your-backend-api.com"  # Your backend URL
api_key = "your-secret-api-key"               # API authentication key

[supabase]
url = "https://xxxx.supabase.co"
anon_key = "your-supabase-anon-key"

[stripe]
publishable_key = "pk_test_..."  # For premium subscriptions
```

### 5. Run the Application
```bash
streamlit run Home.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended for MVP)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud dashboard
5. Deploy!

**Pros:** Free, easy, automatic HTTPS
**Cons:** Limited to Streamlit Cloud features

### Option 2: Custom VPS/Cloud (Production)

#### Deploy on Railway/Render/Fly.io

**Example: Railway Deployment**

1. Create `railway.toml`:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "streamlit run Home.py --server.port $PORT"
```

2. Add environment variables in Railway dashboard
3. Push to GitHub and connect to Railway
4. Automatic deployment!

#### Deploy on AWS/GCP/Azure

See detailed guide: [DEPLOYMENT.md](DEPLOYMENT.md) *(to be created)*

### Option 3: Docker (Advanced)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "Home.py"]
```

```bash
docker build -t etsydashboard-frontend .
docker run -p 8501:8501 etsydashboard-frontend
```

---

## 🔧 Configuration

### Streamlit Settings

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"        # Accent color
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F9FA"
textColor = "#2C3E50"

[server]
port = 8501
enableCORS = false
```

### API Integration

The frontend communicates with a **private backend API** for:
- User authentication
- Data analysis (finance, customer, SEO)
- Premium features (AI recommendations)
- Subscription management

See `utils/api_client.py` for API endpoints.

---

## 📊 SEO Optimization

### Meta Tags & Schema Markup

All landing pages include:
- ✅ Optimized title & meta description
- ✅ OpenGraph & Twitter Card tags
- ✅ Schema.org markup (Product, FAQ, SoftwareApplication)
- ✅ Canonical URLs

### Target Keywords

| Page | Primary Keyword | Monthly Searches |
|------|----------------|------------------|
| Home | "etsy dashboard" | 1,600 |
| Calculator | "calculate etsy fees" | 3,600 |
| Tool | "etsy analytics tool" | 170 |

### Performance

- Lighthouse Score: 90+ (target)
- Mobile responsive
- Fast load times

---

## 🧪 Development

### Project Conventions

- **Code Style:** PEP 8
- **Docstrings:** Google style
- **Imports:** Absolute imports preferred
- **Components:** Reusable, single responsibility

### Adding New Pages

1. Create file in `pages/` or `landings/`
2. Use SEO components from `components/seo_meta.py`
3. Follow existing page structure
4. Test locally before deploying

### Adding New Components

```python
# components/my_component.py
def render_my_component(param1, param2):
    """
    Brief description
    
    Args:
        param1: Description
        param2: Description
    """
    st.markdown("""
        <!-- Your HTML/CSS here -->
    """, unsafe_allow_html=True)
```

---

## 🔐 Security

### Authentication
- User authentication handled via backend API
- Session state managed by Streamlit
- Passwords hashed (bcrypt) on backend

### Data Protection
- All API calls use HTTPS
- API keys stored in `.streamlit/secrets.toml` (gitignored)
- No sensitive data in frontend code

### Best Practices
- ✅ Input validation on all forms
- ✅ CSRF protection enabled
- ✅ SQL injection prevention (backend)
- ✅ XSS sanitization

---

## 📈 Analytics

### User Tracking (Optional)

To enable Google Analytics:

```python
from components.seo_meta import inject_google_analytics

inject_google_analytics("G-XXXXXXXXXX")
```

### Metrics to Track
- Page views per landing
- Conversion rate (landing → signup)
- Upgrade rate (free → premium)
- Feature usage (dashboard visits)

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
pip install -r requirements.txt --force-reinstall
```

**2. API connection failed**
- Check `secrets.toml` has correct backend URL
- Verify backend API is running
- Check network/firewall settings

**3. Streamlit not starting**
```bash
# Check if port 8501 is in use
lsof -i :8501

# Kill process and restart
kill -9 <PID>
streamlit run Home.py
```

**4. Secrets not loading**
- Ensure file is `.streamlit/secrets.toml` (not `.example`)
- Check TOML syntax is valid
- Restart Streamlit after editing secrets

---

## 🤝 Contributing

This is a **private commercial project**. If you have access and want to contribute:

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "Add feature"`
3. Push to branch: `git push origin feature/my-feature`
4. Open a Pull Request

### Code Review Checklist
- [ ] Code follows PEP 8
- [ ] Docstrings added
- [ ] No hardcoded secrets
- [ ] Tested locally
- [ ] SEO meta tags updated (if landing page)

---

## 📝 License

**Proprietary License**

Copyright © 2024 Etsy Dashboard. All rights reserved.

This software and associated documentation files are proprietary and confidential. 
Unauthorized copying, distribution, or use is strictly prohibited.

---

## 📞 Support

### Documentation
- [User Guide](docs/USER_GUIDE.md) *(to be created)*
- [API Documentation](docs/API.md) *(to be created)*
- [Deployment Guide](docs/DEPLOYMENT.md) *(to be created)*

### Contact
- **Email:** support@etsydashboard.com
- **Issues:** GitHub Issues (private repo)
- **Website:** [etsydashboard.com](https://etsydashboard.com)

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Finance Pro Dashboard
- ✅ Customer Intelligence Dashboard
- ✅ SEO Analyzer Dashboard
- ✅ Fee Calculator
- ✅ Premium Subscriptions

### Version 1.1 (Next)
- [ ] CSV auto-upload from Etsy API
- [ ] Email reports
- [ ] Mobile app (React Native)
- [ ] Multi-language support

### Version 2.0 (Future)
- [ ] Competitor tracking
- [ ] Inventory management
- [ ] Multi-shop support
- [ ] White-label solution

---

## 🙏 Acknowledgments

- **Streamlit** - Web framework
- **Plotly** - Visualizations
- **Anthropic Claude** - AI development assistance

---

**Built with ❤️ for Etsy sellers worldwide**

*Last Updated: December 19, 2025*