# Streamlit Cloud Setup - Post Deployment

Since you've already deployed to Streamlit Cloud, here's what you need to do:

## ✅ Step 1: Verify Your Files

Make sure these files are in your GitHub repository:

- ✅ `app.py` (with latest changes)
- ✅ `requirements.txt` (with `playwright>=1.40.0`)
- ✅ `packages.txt` (can be empty, but file must exist)

## ✅ Step 2: Install Playwright Browsers

**IMPORTANT**: Streamlit Cloud needs Playwright browsers installed. You have two options:

### Option A: Add Build Command (Recommended)

1. Go to your Streamlit Cloud app dashboard
2. Click "Settings" or "Manage app"
3. Look for "Build command" or "Post-install command"
4. Add this command:
   ```bash
   python -m playwright install chromium && python -m playwright install-deps chromium
   ```
5. Save and redeploy

### Option B: Manual Installation via Streamlit Cloud Shell

If Option A doesn't work:

1. Go to Streamlit Cloud dashboard
2. Find "Shell" or "Terminal" access (if available)
3. Run:
   ```bash
   python -m playwright install chromium
   python -m playwright install-deps chromium
   ```

### Option C: Use setup.sh (Alternative)

If Streamlit Cloud supports setup scripts:

1. Make sure `setup.sh` is in your repo
2. Make it executable: `chmod +x setup.sh`
3. Streamlit Cloud should run it automatically

## ✅ Step 3: Verify Environment Variables

1. Go to Streamlit Cloud app settings
2. Click "Secrets" tab
3. Make sure you have:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
4. Save changes

## ✅ Step 4: Push Latest Code

Make sure your latest code changes are pushed to GitHub:

```bash
git add .
git commit -m "Fix Workday extraction and Playwright setup"
git push
```

Streamlit Cloud will automatically redeploy.

## ✅ Step 5: Test Your App

1. Wait for deployment to complete (2-5 minutes)
2. Test with the Sprinklr Workday URL:
   ```
   https://sprinklr.wd1.myworkdayjobs.com/en-US/careers/job/Product-Engineer_111920-JOB
   ```
3. Check if it extracts the correct job information

## 🔧 Troubleshooting

### If Playwright still doesn't work:

1. **Check build logs** in Streamlit Cloud dashboard
2. **Look for errors** about Playwright browser installation
3. **Try adding to packages.txt**:
   ```
   libnss3
   libatk-bridge2.0-0
   libdrm2
   libxkbcommon0
   libxcomposite1
   libxdamage1
   libxfixes3
   libxrandr2
   libgbm1
   libasound2
   ```

### If you get "Executable doesn't exist" error:

The Playwright browser isn't installed. Follow Step 2 above.

### If extraction still shows wrong company:

1. Check the app logs in Streamlit Cloud
2. Verify the URL is correct
3. The AI might be hallucinating - the updated prompt should fix this

## 📝 Current Status Checklist

- [ ] Latest code pushed to GitHub
- [ ] Playwright browsers installed (Step 2)
- [ ] GOOGLE_API_KEY set in Secrets
- [ ] App redeployed successfully
- [ ] Tested with Workday URL
- [ ] Extraction works correctly

## 🚀 Next Steps

Once everything works:
1. Share your app URL with users
2. Monitor usage in Streamlit Cloud dashboard
3. Check logs if users report issues

---

**Note**: If Streamlit Cloud doesn't support build commands, you may need to:
- Use a different deployment platform (Render, Railway) that supports Playwright
- Or use an alternative scraping method that doesn't require Playwright

