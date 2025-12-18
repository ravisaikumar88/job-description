# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "Backend error" or "Cannot connect to backend"

**Root Cause**: Render's free tier services automatically sleep after 15 minutes of inactivity. When a request is made to a sleeping service, it takes 20-40 seconds to wake up (cold start).

**Solutions**:

#### Option 1: Wait and Retry (Quick Fix)
- If you see an error, wait 30-60 seconds and try again
- The first request after sleep will be slow, but subsequent requests will be fast

#### Option 2: Set Up Keep-Alive (Recommended)
Keep your Render service awake by pinging it every 10-14 minutes.

**Using cron-job.org (Free)**:
1. Go to https://cron-job.org
2. Sign up for a free account
3. Create a new cron job:
   - **URL**: `https://job-description-1wnm.onrender.com/health`
   - **Schedule**: Every 10 minutes
   - **Method**: GET
4. Save and activate

**Using UptimeRobot (Free)**:
1. Go to https://uptimerobot.com
2. Sign up for a free account
3. Add a new monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://job-description-1wnm.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
4. Save

#### Option 3: Upgrade Render Plan
- Upgrade to a paid Render plan ($7/month) to prevent sleeping
- Services on paid plans stay awake 24/7

---

### Issue: CORS Errors

**Symptoms**: Browser console shows CORS errors

**Solution**: 
1. Check that `ALLOWED_ORIGINS` environment variable in Render includes your frontend URL
2. Or set `ALLOWED_ORIGINS=*` to allow all origins (current default)
3. Redeploy backend after changing environment variables

---

### Issue: Environment Variables Not Working

**For Vercel (Frontend)**:
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add: `VITE_API_URL` = `https://job-description-1wnm.onrender.com`
4. **Important**: Redeploy after adding environment variables
5. Environment variables are only available at build time for Vite apps

**For Render (Backend)**:
1. Go to your Render service dashboard
2. Navigate to Environment tab
3. Verify these variables are set:
   - `GOOGLE_API_KEY`: Your Gemini API key
   - `ALLOWED_ORIGINS`: `*` or your frontend URL
4. **Important**: Redeploy after changing environment variables

---

### Issue: Frontend Shows "Processing..." Forever

**Possible Causes**:
1. Backend is sleeping (cold start taking 30-60 seconds)
2. Network timeout
3. Backend crashed

**Solutions**:
1. Check browser console (F12) for detailed error messages
2. Check Render logs for backend errors
3. Try accessing backend directly: `https://job-description-1wnm.onrender.com/health`
4. If backend is sleeping, wait 30-60 seconds and retry

---

### Issue: "Gemini API Key Not Found"

**Solution**:
1. Verify `GOOGLE_API_KEY` is set in Render environment variables
2. Check that the key is correct (no extra spaces)
3. Redeploy backend after setting the key

---

### Testing Your Setup

1. **Test Backend Health**:
   ```
   curl https://job-description-1wnm.onrender.com/health
   ```
   Should return: `{"status": "healthy", "service": "Job Auto Formatter API"}`

2. **Test Backend Root**:
   ```
   curl https://job-description-1wnm.onrender.com/
   ```
   Should return: `{"status": "Job Auto Formatter API is running", "gemini_key_loaded": true}`

3. **Test Frontend-Backend Connection**:
   - Open browser console (F12)
   - Go to Network tab
   - Try to extract a job URL
   - Check if request to `/extract` endpoint succeeds

---

### Quick Checklist

- [ ] Backend is deployed on Render
- [ ] Frontend is deployed on Vercel
- [ ] `VITE_API_URL` is set in Vercel environment variables
- [ ] `GOOGLE_API_KEY` is set in Render environment variables
- [ ] `ALLOWED_ORIGINS` is set in Render (or defaults to `*`)
- [ ] Both services have been redeployed after setting environment variables
- [ ] Keep-alive service is set up (optional but recommended)

---

### Need More Help?

1. Check Render logs: Render Dashboard → Your Service → Logs
2. Check Vercel logs: Vercel Dashboard → Your Project → Deployments → View Function Logs
3. Check browser console: F12 → Console tab
4. Check network requests: F12 → Network tab
