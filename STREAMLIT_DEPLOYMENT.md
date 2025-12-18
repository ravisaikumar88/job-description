# Streamlit Cloud Deployment Guide

Complete guide to deploy Job Auto Formatter on Streamlit Cloud (free).

## Prerequisites

1. GitHub account
2. Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
3. Code pushed to GitHub repository

---

## Step 1: Prepare Your Code

Make sure your repository has:
- ✅ `app.py` (main Streamlit file)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `.streamlit/config.toml` (optional, for configuration)
- ✅ `packages.txt` (optional, for system packages)

---

## Step 2: Push to GitHub

If you haven't already:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

**Important**: Make sure your `.env` file is in `.gitignore` (it should be by default).

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Sign Up / Sign In

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "Sign up" or "Sign in"
3. Authorize with your GitHub account

### 3.2 Create New App

1. Click "New app" button
2. You'll see a form to configure your app

### 3.3 Configure App Settings

**Repository**: Select your GitHub repository

**Branch**: Usually `main` or `master`

**Main file path**: `app.py`

**App URL**: Choose a custom subdomain (optional)
- Example: `job-auto-formatter` → `https://job-auto-formatter.streamlit.app`

### 3.4 Advanced Settings

Click "Advanced settings" to configure:

**Python version**: 
- Select `3.11` or latest available
- Streamlit Cloud supports Python 3.8+

**Secrets** (Environment Variables):
- Click on the "Secrets" tab
- Enter secrets in **TOML format** (not plain key=value)
- Use this exact format:
  ```toml
  GOOGLE_API_KEY = "your_actual_api_key_here"
  ```
- **Important**: 
  - Use quotes around the value
  - Use `=` with spaces on both sides
  - Each secret on a new line
- Click "Save changes"

**Example:**
```toml
GOOGLE_API_KEY = "AIzaSyA83qAYeR0150n3pVxrT-iRs4ThFaYqaBE"
```

**Note**: Secrets are encrypted and only accessible to your app. Changes take about 1 minute to propagate.

### 3.5 Deploy

1. Click "Deploy" button
2. Wait 2-5 minutes for deployment
3. You'll see build logs in real-time
4. Once complete, you'll see "Your app is live!" message

---

## Step 4: Access Your App

Your app will be available at:
```
https://YOUR-APP-NAME.streamlit.app
```

Example: `https://job-auto-formatter.streamlit.app`

---

## Step 5: Update Your App

Every time you push to your GitHub repository:

1. Streamlit Cloud automatically detects changes
2. Triggers a new deployment
3. Your app updates automatically (usually 1-2 minutes)

**No manual redeploy needed!**

---

## Managing Your App

### View Logs

1. Go to your app dashboard
2. Click "Manage app"
3. View "Logs" tab for runtime logs
4. View "Metrics" for usage statistics

### Update Secrets

1. Go to app settings
2. Click "Secrets" tab
3. Edit or add new secrets
4. App will automatically restart with new secrets

### Delete App

1. Go to app settings
2. Click "Delete app"
3. Confirm deletion

---

## Troubleshooting

### Build Fails

**Error**: "Module not found"
- **Solution**: Check `requirements.txt` includes all dependencies
- Make sure version numbers are specified

**Error**: "Playwright not installed"
- **Solution**: Streamlit Cloud handles Playwright automatically
- If issues persist, check `packages.txt` is present (even if empty)

**Error**: "API key not found"
- **Solution**: Make sure you added `GOOGLE_API_KEY` in Secrets
- Check the key name matches exactly (case-sensitive)

### App Crashes

**Error**: "Timeout" or "App not responding"
- **Solution**: Some operations (Playwright) take 30-60 seconds
- This is normal for first request
- Consider adding progress indicators

**Error**: "Memory limit exceeded"
- **Solution**: Playwright uses significant memory
- Streamlit Cloud free tier has limits
- Consider optimizing code or upgrading

### Slow Performance

- **First request**: Always slow (30-60s) due to Playwright initialization
- **Subsequent requests**: Much faster (5-10s)
- **LinkedIn pages**: May take longer due to dynamic content

---

## Streamlit Cloud Limits (Free Tier)

- ✅ Unlimited apps
- ✅ Unlimited deployments
- ✅ 1GB RAM per app
- ✅ Apps stay awake (no cold starts!)
- ✅ Custom domains supported
- ✅ Private repos supported

**Note**: Free tier is generous and perfect for personal projects!

---

## Best Practices

1. **Keep secrets secure**: Never commit API keys to GitHub
2. **Test locally first**: Make sure app works before deploying
3. **Monitor usage**: Check metrics to understand usage patterns
4. **Optimize code**: Long-running operations should show progress
5. **Error handling**: Add try-catch blocks for better UX

---

## Next Steps

After deployment:

1. ✅ Test your app with various job URLs
2. ✅ Share the link with users
3. ✅ Monitor logs for any issues
4. ✅ Update as needed (auto-deploys on push)

---

## Support

- **Streamlit Docs**: [https://docs.streamlit.io](https://docs.streamlit.io)
- **Streamlit Community**: [https://discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Report bugs in your repository

---

**Congratulations! Your app is now live on Streamlit Cloud! 🎉**
