# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- Streamlit Cloud account (free tier available at https://streamlit.io/cloud)
- This repository pushed to GitHub

## Step 1: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/XtenHire_AI.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Select:
   - **Repository**: `your-username/XtenHire_AI`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy"

## Step 3: Wait for Deployment

- Your app will build and deploy automatically
- First deployment takes 2-3 minutes
- You'll get a public URL like: `https://xtenhire-ai.streamlit.app`

## Configuration

### Environment Variables (if needed)
If you need to set environment variables for deployment:

1. Go to your app settings (⋯ menu → Settings)
2. Click "Secrets"
3. Add secrets as `KEY=value` pairs
4. Reference in code: `st.secrets["KEY"]`

### Resource Limits (Free Tier)
- Max 3 public apps
- Dedicated compute for 3 hours/day
- Shared compute after that
- 1 GB file upload limit

## Customization

### Update Title/Icon
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Page title
- Icon/favicon

### Environment-Specific Settings
For local vs. cloud differences:
```python
import streamlit as st

if st.secrets.get("ENVIRONMENT") == "production":
    # Production-specific settings
    pass
```

## Troubleshooting

### "ModuleNotFoundError"
- Ensure all imports have corresponding packages in `requirements.txt`
- Check spelling of package names (case-sensitive)

### "PDF parsing fails on cloud"
- pdfplumber requires system dependencies
- Streamlit Cloud includes common dependencies
- If issues persist, use PyPDF2 as fallback (already implemented)

### "App is slow"
- First load is slower due to package installation
- Subsequent loads are cached
- Monitor compute usage in Settings → Resource Limits

### "Secrets not found"
- Make sure to add secrets through Streamlit Cloud UI, not locally
- Local `.streamlit/secrets.toml` is NOT synced

## Local Testing Before Deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model (recommended but optional)
python -m spacy download en_core_web_sm

# Run locally
streamlit run app.py
```

## Updates & Redeployment

Every time you push to `main` branch:
```bash
git add .
git commit -m "Update app"
git push origin main
```

Your Streamlit Cloud app will automatically redeploy with the latest code.

## Support
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud FAQ](https://docs.streamlit.io/streamlit-cloud/get-started)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)
