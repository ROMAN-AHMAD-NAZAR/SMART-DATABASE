# 🚂 Deploy to Railway - Step-by-Step Guide

## Prerequisites ✅
- [x] Groq API Key (you have this!)
- [x] GitHub account
- [x] This repository

---

## 📋 Deployment Steps

### Step 1: Go to Railway
1. Visit [railway.app](https://railway.app)
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with your GitHub account

### Step 2: Authorize Railway to Access GitHub
1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. **IMPORTANT**: If you don't see any repositories, click **"Configure GitHub App"**
4. This will open GitHub's authorization page
5. Choose one of these options:
   - **"All repositories"** (recommended - easiest option)
   - **"Only select repositories"** → Select "SMART-DATABASE"
6. Click **"Save"** on GitHub
7. Return to Railway (it will redirect automatically)

### Step 3: Select Your Repository
1. Now you should see your repositories listed
2. Find and click: **"ROMAN-AHMAD-NAZAR/SMART-DATABASE"**
3. Railway will automatically detect it's a Python app

### Step 4: Select Branch
- Choose **"copilot/make-app-live"** (or **"main"** if merged)
- Click **"Deploy Now"**

### Step 5: Wait for Initial Deploy
- Railway will automatically:
  - Detect Python
  - Install dependencies from `requirements.txt`
  - Start the app with gunicorn
- Initial deployment takes 2-3 minutes

### Step 6: Add Environment Variables
1. Click on your deployed service (the purple box)
2. Go to the **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these environment variables:

| Variable Name | Value |
|--------------|-------|
| `GROQ_API_KEY` | Your Groq API key (starts with `gsk_...`) |
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `False` |
| `DATABASE_FILE` | `cars.db` |

**Important**: Paste your actual Groq API key in the `GROQ_API_KEY` field!

5. Click **"Save"** after adding all variables
6. Railway will automatically redeploy with the new variables

### Step 7: Generate Public Domain
1. Go to the **"Settings"** tab
2. Scroll down to **"Networking"** section
3. Click **"Generate Domain"**
4. Railway will create a public URL: `https://your-app.up.railway.app`

### Step 8: Access Your Live App! 🎉
1. Click on the generated domain URL
2. Your app will open in a new tab
3. You should see the beautiful purple gradient UI with animated cars!

---

## ✅ Verify Deployment

### Test 1: Check Health Endpoint
Visit: `https://your-app.up.railway.app/health`

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "car_count": 108540,
  "version": "1.0.0"
}
```

### Test 2: Try a Query
1. Go to your app homepage: `https://your-app.up.railway.app`
2. Type in the chat: "What's the average price of Toyota cars?"
3. Click Send
4. Wait 5-10 seconds for the AI to respond
5. You should get a formatted answer with real data!

### Test 3: Try More Queries
- "Show me the most fuel-efficient cars"
- "List BMW models available"
- "What cars are under £15,000?"
- "Which brand has the highest average MPG?"

---

## 🐛 Troubleshooting

### Repository Not Showing Up?
**This is the most common issue!** Railway needs permission to access your GitHub repository.

**Solution:**
1. Go to [railway.app](https://railway.app) and login
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Click **"Configure GitHub App"** (you'll see this if no repos show)
4. This opens GitHub permissions page
5. On GitHub, select one of these options:
   - **"All repositories"** (easiest - gives Railway access to all your repos)
   - **"Only select repositories"** → Choose **"SMART-DATABASE"**
6. Click **"Save"** on GitHub
7. Go back to Railway and refresh the page
8. Your repository should now appear in the list!

**Still not showing?**
- Make sure you're logged into GitHub with the account that owns the repository
- Check that the repository is not private (or Railway has access to private repos)
- Try logging out of Railway and logging back in
- Clear your browser cache and try again

### Deployment Failed?
**Check the deployment logs:**
1. Click on your service in Railway dashboard
2. Click on the **"Deployments"** tab
3. Click on the failed deployment
4. Review the build logs for errors

**Common issues:**
- **Missing dependencies**: Make sure `requirements.txt` is in the root directory
- **Python version**: Railway uses Python 3.11 by default (compatible with our app)
- **Missing `GROQ_API_KEY`**: Add it in Variables tab and redeploy

### "No API key found" Error?
**Fix:**
1. Go to Railway dashboard
2. Click your service
3. Go to **"Variables"** tab
4. Verify `GROQ_API_KEY` is set correctly (starts with `gsk_...`)
5. Click **"Redeploy"** button in Deployments tab

### App Not Responding?
**Fix:**
1. Check the **"Logs"** tab for runtime errors
2. Verify all environment variables are set
3. Check that the database file `cars.db` is in the repository
4. Try redeploying: Go to Deployments → Click "..." → "Redeploy"

### Port Issues?
Railway automatically sets the `PORT` environment variable. Our app is configured to use it:
```python
port = int(os.environ.get('PORT', 5000))
```
This should work automatically - no action needed!

### Database Connection Errors?
The SQLite database `cars.db` is included in the repository and should work automatically. If you see database errors:
1. Check logs for specific error messages
2. Verify `cars.db` exists in the repository root
3. Check file permissions in deployment logs

---

## 🔄 Updating Your App

Railway automatically redeploys when you push to GitHub:

1. **Make changes** to your code
2. **Commit and push** to GitHub
3. **Railway auto-deploys** the changes
4. **Watch the progress** in the Deployments tab

To disable auto-deploy:
1. Go to **"Settings"** tab
2. Scroll to **"Service"** section
3. Toggle off **"Auto Deploy"**

---

## 💰 Cost & Billing

### Free Trial
- **$5 in credits** when you sign up (no credit card required)
- Enough for ~500 hours of app runtime
- Perfect for testing and development

### After Free Trial
- **Usage-based pricing**: Pay only for what you use
- Typical cost: **$5-10/month** for a small app like this
- Includes:
  - Compute time
  - RAM usage
  - Network egress

### Resource Usage
This app uses:
- **Memory**: ~150-200MB
- **CPU**: Minimal (only during queries)
- **Storage**: ~7MB (database)

---

## 📊 Monitoring Your App

### View Logs
1. Click on your service
2. Go to **"Logs"** tab
3. See real-time logs of your app
4. Filter by severity (Info, Warning, Error)

### View Metrics
1. Go to **"Metrics"** tab
2. See:
   - Memory usage
   - CPU usage
   - Network traffic
   - Response times

### Deployment History
1. Go to **"Deployments"** tab
2. See all past deployments
3. Roll back to previous versions if needed
4. View build logs for each deployment

---

## ⚙️ Advanced Configuration

### Custom Start Command (Optional)
Railway auto-detects Python and uses the correct command, but you can customize it:

1. Go to **"Settings"** tab
2. Scroll to **"Deploy"** section
3. Add custom start command:
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
   ```

### Environment-Specific Variables
You can set different variables for different environments:
1. Create multiple services (dev, staging, prod)
2. Each can have different environment variables
3. Deploy from different branches

---

## 🎯 Post-Deployment

### Your Live URL
Your app is now live at: `https://your-app-name.up.railway.app`

### Share Your App
- Add to your portfolio
- Share with friends and colleagues
- Tweet it with #AI #Flask #Railway
- Add the URL to your GitHub repo description

### Custom Domain (Optional)
Want your own domain like `myapp.com`?

1. Buy a domain from any registrar
2. Go to Railway **"Settings"** → **"Networking"**
3. Click **"Custom Domain"**
4. Follow Railway's instructions to set up DNS
5. Add your domain and verify

---

## 🔒 Security Best Practices

### Protect Your API Key
- ✅ Never commit `.env` files
- ✅ Use Railway's Variables tab
- ✅ Rotate keys every 90 days
- ✅ Monitor usage in Groq dashboard

### Monitor Your App
- Check logs weekly for errors
- Review metrics for unusual activity
- Set up alerts in Railway (Pro plan)

---

## 🎉 Success!

If you can access your app and run queries, **congratulations!** 

Your AI-powered car database is now **LIVE on Railway**! 🚂🎊

**Your live URL**: `https://your-app-name.up.railway.app`

---

## 📞 Need Help?

### Railway Resources
- [Railway Docs](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app/)

### App Resources
- [QUICKSTART.md](QUICKSTART.md) - Quick deployment guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Other platform options
- [README.md](README.md) - App documentation
- [GitHub Issues](https://github.com/ROMAN-AHMAD-NAZAR/SMART-DATABASE/issues) - Report problems

---

**Made with ❤️ - Now deployed on Railway!** 🚂
