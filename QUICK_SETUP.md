# 🚀 Quick Setup Guide for Streamlit Cloud

## What You Need to Do NOW:

### 1. ✅ Push Latest Code to GitHub

```bash
git add .
git commit -m "Fix Workday extraction and add Playwright setup"
git push
```

### 2. ✅ Install Playwright Browser in Streamlit Cloud

**Go to Streamlit Cloud Dashboard:**
1. Open your app: https://share.streamlit.io
2. Click on your app → **"Settings"** or **"⚙️"** icon
3. Look for **"Build command"** or **"Post-install command"** field
4. Add this command:
   ```
   python -m playwright install chromium
   ```
5. Click **"Save"** or **"Redeploy"**

### 3. ✅ Verify Environment Variables

In Streamlit Cloud Settings → **"Secrets"** tab, make sure you have:

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### 4. ✅ Wait for Redeployment

- Streamlit Cloud will automatically redeploy (2-5 minutes)
- Watch the build logs for any errors
- Look for "Playwright" installation messages

### 5. ✅ Test Your App

Try this URL:
```
https://sprinklr.wd1.myworkdayjobs.com/en-US/careers/job/Product-Engineer_111920-JOB
```

It should now extract **Sprinklr** job details correctly!

---

## 📋 Files Updated:

- ✅ `app.py` - Fixed Workday detection and improved extraction
- ✅ `packages.txt` - Added Playwright system dependencies
- ✅ `requirements.txt` - Already has Playwright
- ✅ `setup.sh` - Created (optional, if Streamlit Cloud supports it)

## ❌ If Build Command Doesn't Work:

Some Streamlit Cloud plans don't support build commands. In that case:

1. **Check if `packages.txt` helps** - It's already updated with dependencies
2. **Contact Streamlit Support** - Ask about Playwright browser installation
3. **Alternative**: Consider using Render/Railway which definitely support Playwright

---

## 🎯 Expected Result:

After setup, your app should:
- ✅ Detect Workday URLs automatically
- ✅ Use Playwright for dynamic content
- ✅ Extract correct company/job information
- ✅ No more "Amazon" hallucinations!

---

**Need help?** Check `STREAMLIT_CLOUD_SETUP.md` for detailed troubleshooting.

