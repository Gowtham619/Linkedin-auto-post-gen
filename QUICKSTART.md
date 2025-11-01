# Quick Start Guide - AI Content Agent (Perplexity Edition)

## 5-Minute Setup

### Step 1: Get Perplexity API Key

1. Go to https://www.perplexity.ai
2. Sign up or log in
3. Navigate to: https://www.perplexity.ai/settings/api
4. Click "Generate API Key"
5. Copy your key (starts with `pplx-`)

### Step 2: Get LinkedIn Credentials

1. Go to https://www.linkedin.com/developers/apps
2. Create a new app (or select existing)
3. Request access to:
   - "Sign In with LinkedIn"
   - "Share on LinkedIn"
4. Go to "Auth" tab
5. Generate access token with `w_member_social` scope
6. Copy the token

**Get your Person URN:**
```bash
curl -X GET https://api.linkedin.com/v2/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Your URN: `urn:li:person:THE_ID_FROM_RESPONSE`

### Step 3: Get Medium Token

1. Go to https://medium.com/me/settings
2. Scroll to "Integration tokens"
3. Enter description: "AI Content Agent"
4. Click "Get integration token"
5. Copy the token

### Step 4: Install & Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp config/.env.template config/.env
nano config/.env
```

Paste your credentials:
```bash
PERPLEXITY_API_KEY=pplx-your-key
LINKEDIN_ACCESS_TOKEN=your-linkedin-token
LINKEDIN_PERSON_URN=urn:li:person:your-id
MEDIUM_INTEGRATION_TOKEN=your-medium-token
```

### Step 5: Test Everything

```bash
# Load environment
export $(cat config/.env | xargs)

# Test setup
python test_setup.py
```

✓ All tests should pass

### Step 6: Test Content Generation

```bash
# Generate one test post (won't publish)
python test_content_generation.py

# Review output
cat content/test_linkedin_*.json
```

### Step 7: Run the Agent

**Choose your method:**

#### Quick Run (Terminal)
```bash
export $(cat config/.env | xargs)
python src/content_agent.py
```

#### Docker (Best for Production)
```bash
docker-compose up -d
docker-compose logs -f
```

#### Background Process
```bash
export $(cat config/.env | xargs)
nohup python src/content_agent.py > logs/agent.log 2>&1 &
```

## What Happens Next?

The agent will:
1. ✓ Research AI topics (30-60 seconds)
2. ✓ Generate content for LinkedIn & Medium
3. ✓ Post automatically
4. ✓ Wait 6 hours
5. ✓ Repeat forever

## Monitoring

```bash
# View logs
tail -f logs/agent.log

# Check generated content
ls -la content/

# Stop agent
# If Docker: docker-compose down
# If background: pkill -f content_agent.py
# If terminal: Ctrl+C
```

## Customization

### Change Posting Frequency
Edit `config/config.json`:
```json
{
  "agent_settings": {
    "post_interval_hours": 12  // Change to 3, 6, 12, 24, etc.
  }
}
```

### Modify Research Topics
Edit `config/config.json` → `research_settings` → `topics`

### Adjust Content Style
Edit `config/config.json` → `content_guidelines`

## Troubleshooting

### API Key Issues
```bash
# Test Perplexity connection
python test_setup.py
```

### Content Not Posting
1. Check logs: `tail -f logs/agent.log`
2. Verify all credentials in `.env`
3. Run full test: `python test_setup.py`

### LinkedIn Token Expired
- Tokens expire after ~60 days
- Regenerate at: https://www.linkedin.com/developers/apps
- Update `.env` file

## Common Commands

```bash
# Start agent
python src/content_agent.py

# Start with Docker
docker-compose up -d

# View logs
tail -f logs/agent.log

# Stop Docker
docker-compose down

# Test setup
python test_setup.py

# Generate test content
python test_content_generation.py

# View generated posts
ls -lt content/
```

## Cost Estimate

**Per Day (4 cycles):**
- Perplexity API: ~$0.40-1.20
- LinkedIn: Free
- Medium: Free

**Monthly:** ~$12-36

## Next Steps

1. ✓ Let it run for 24 hours
2. ✓ Review generated content quality
3. ✓ Adjust settings if needed
4. ✓ Monitor engagement on posts
5. ✓ Customize topics based on audience

## Support

**Check first:**
- Logs: `tail -100 logs/agent.log`
- Setup: `python test_setup.py`
- README.md for detailed docs

**Common issues:**
- API keys not set → Check `.env` file
- Import errors → Run `pip install -r requirements.txt`
- Permission denied → Check file permissions

---

**Ready?** Run `python test_setup.py` to begin! 🚀

## Key Differences from Standard Edition

This Perplexity edition:
- ✓ Uses Perplexity API (simpler setup)
- ✓ Accesses Claude 3.5 Sonnet
- ✓ OpenAI-compatible API format
- ✓ Unified billing through Perplexity
- ✓ Same great features & quality

Perfect for users who want simplicity and unified API management!
