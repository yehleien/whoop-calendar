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
- `GOOGLE_TOKEN`: The contents of your `token.pickle` file (base64 encoded)

**Whoop Secrets:**
- `WHOOP_TOKEN`: The contents of your `whoop_token.json` file
- `WHOOP_CLIENT_ID`: `1173921f-1774-46c9-a6a4-78052162a7dc`
- `WHOOP_CLIENT_SECRET`: `97e155a8a6c40212150d68dfa70b5eff3e4784b50bc19e444ec8bd349a4fadb7`

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