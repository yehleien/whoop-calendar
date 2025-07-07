# Whoop to Google Calendar Sync

Automatically syncs your Whoop workouts and sleep data to Google Calendar.

## Setup for GitHub Actions

### 1. Create a GitHub Repository
1. Create a new repository on GitHub
2. Upload all files from this directory to the repository

### 2. Set up GitHub Secrets
Go to your repository → Settings → Secrets and variables → Actions, then add these secrets:

**Google Calendar Secrets:**
- `GOOGLE_CREDENTIALS`: The contents of your `credentials.json` file
- `GOOGLE_TOKEN`: The base64-encoded contents of your `token.pickle` file

**Whoop Secrets:**
- `WHOOP_TOKEN`: The contents of your `whoop_token.json` file
- `WHOOP_CLIENT_ID`: Your Whoop client ID
- `WHOOP_CLIENT_SECRET`: Your Whoop client secret

### 3. How to get the secret values:

**For GOOGLE_CREDENTIALS:**
```bash
cat credentials.json
```

**For GOOGLE_TOKEN:**
```bash
base64 -i token.pickle
```

**For WHOOP_TOKEN:**
```bash
cat whoop_token.json
```

### 4. Schedule
The workflow runs daily at 10:00 AM UTC (6:00 AM EST). You can also trigger it manually from the Actions tab.

### 5. Monitoring
- Check the Actions tab to see run history
- Download logs from the artifacts section
- Set up notifications in GitHub settings

## Local Setup (Alternative)
If you prefer to run locally, see the original setup instructions in the code comments. 