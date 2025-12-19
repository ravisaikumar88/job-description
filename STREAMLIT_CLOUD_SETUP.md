# Streamlit Cloud Setup - Post Deployment

## ✅ Current Method (New Streamlit Cloud Dashboard)

**Streamlit Cloud removed the "Build commands" UI.** Now you must use files in your GitHub repo.

---

## 📋 Required Files

### 1. `packages.txt`

Contains:
```
playwright
chromium
```

### 2. `postBuild` (no extension, executable)

Contains:
```
python -m playwright install chromium
```

⚠️ **Important**: 
- File name is exactly `postBuild` (no `.sh`, no `.txt`)
- Must be executable (GitHub handles this automatically)
- One command per line

---

## ✅ Step-by-Step Setup

### Step 1: Verify Files in Your Repo

Make sure these files exist:

```
your-repo/
├─ app.py
├─ requirements.txt
├─ packages.txt        ← Should contain: playwright, chromium
└─ postBuild           ← Should contain: python -m playwright install chromium
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add Playwright setup files"
git push
```

### Step 3: Streamlit Cloud Auto-Rebuilds

- Streamlit Cloud detects the push
- Runs `postBuild` script automatically
- Installs Playwright browser during build
- Deploys your app

### Step 4: Verify Environment Variables

In Streamlit Cloud Dashboard:
1. Go to your app → **Settings** → **Secrets**
2. Ensure you have:

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### Step 5: Test

Try a Workday URL:
```
https://sprinklr.wd1.myworkdayjobs.com/en-US/careers/job/Product-Engineer_111920-JOB
```

---

## 🔧 Troubleshooting

### Build Fails with "Playwright not found"

**Check:**
1. ✅ `packages.txt` exists and contains `playwright`
2. ✅ `postBuild` exists (no extension) and contains install command
3. ✅ Files are committed and pushed to GitHub
4. ✅ Check build logs in Streamlit Cloud dashboard

### "Executable doesn't exist" Error

**Solution:**
- The `postBuild` script should install the browser
- Check build logs to see if `postBuild` ran successfully
- Verify the command in `postBuild` is correct: `python -m playwright install chromium`

### Still Getting Wrong Company Extraction

**Check:**
1. ✅ Latest `app.py` is pushed (with Workday detection fixes)
2. ✅ Test with a fresh deployment
3. ✅ Check app logs for any errors

---

## 📝 What Changed in Streamlit Cloud

**Old Method (No Longer Available):**
- ❌ Build commands in UI settings
- ❌ Post-install commands in dashboard

**New Method (Current):**
- ✅ `packages.txt` for system packages
- ✅ `postBuild` script for post-install commands
- ✅ All configuration via files in repo

---

## 🎯 Expected Result

After successful setup:
- ✅ Playwright browser installed automatically
- ✅ Workday URLs detected and processed correctly
- ✅ Correct company/job information extracted
- ✅ No more "Amazon" or wrong company hallucinations

---

## 🚀 Next Steps

1. ✅ Push code with `postBuild` and updated `packages.txt`
2. ✅ Wait for auto-rebuild (2-5 minutes)
3. ✅ Test with Workday URLs
4. ✅ Monitor logs if issues occur

---

**Need Help?** Check build logs in Streamlit Cloud dashboard for detailed error messages.
