# AI Content Auto-Posting Agent (Perplexity Edition)

A fully automated agent that uses **Perplexity API to access Claude 3.5 Sonnet** for generating human-like AI content and publishing to LinkedIn and Medium every 6 hours after conducting deep research.

## 🌟 What's Special About This Edition

- **Uses Perplexity API** to access Claude models instead of direct Anthropic API
- **Claude 3.5 Sonnet** - Latest and most capable Claude model available on Perplexity
- **Simpler setup** - Unified API, OpenAI-compatible format
- **All original features** - Research, human-like writing, auto-posting

## 🎯 Features

- 🔍 **Deep Research**: Automatically researches latest AI trends
- ✍️ **Human-Like Content**: Natural, conversational writing (no AI clichés!)
- 📱 **Multi-Platform**: Posts to LinkedIn and Medium
- ⏰ **Automated**: Runs every 6 hours continuously
- 📊 **Smart History**: Avoids topic repetition
- 💾 **Local Backup**: Saves all content
- 🔄 **Resilient**: Auto-recovery and error handling
- 🤖 **Perplexity-Powered**: Uses Perplexity's API for Claude access

## 📋 Prerequisites

1. **Perplexity API Key** (Required)
   - Sign up at: https://www.perplexity.ai
   - Get API key: https://www.perplexity.ai/settings/api
   - Free tier available, paid plans for higher usage

2. **LinkedIn Developer Account** (Required for LinkedIn posting)
   - Create app: https://www.linkedin.com/developers/apps
   - Enable "Share on LinkedIn" product
   - Generate access token with `w_member_social` scope

3. **Medium Account** (Required for Medium posting)
   - Integration token: https://medium.com/me/settings
   - Generate under "Integration tokens" section

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
cd ai-content-agent-perplexity
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy template
cp config/.env.template config/.env

# Edit with your credentials
nano config/.env
```

Add your API keys:
```bash
PERPLEXITY_API_KEY=pplx-your-key-here
LINKEDIN_ACCESS_TOKEN=your-linkedin-token
LINKEDIN_PERSON_URN=urn:li:person:your-id
MEDIUM_INTEGRATION_TOKEN=your-medium-token
```

**Get Your LinkedIn Person URN:**
```bash
curl -X GET https://api.linkedin.com/v2/me \
  -H "Authorization: Bearer YOUR_LINKEDIN_TOKEN"
# Look for "id" field, format as: urn:li:person:ID
```

### Step 3: Test Setup

```bash
# Load environment variables
export $(cat config/.env | xargs)

# Run verification
python test_setup.py
```

If all tests pass ✓, proceed to Step 4.

### Step 4: Test Content Generation

```bash
# Generate one test post (won't publish)
python test_content_generation.py

# Review generated content
cat content/test_linkedin_*.json
```

### Step 5: Run the Agent

Choose your deployment method:

#### Option A: Direct Python
```bash
export $(cat config/.env | xargs)
python src/content_agent.py
```

#### Option B: Docker (Recommended)
```bash
docker-compose up -d
docker-compose logs -f
```

#### Option C: Background Process
```bash
export $(cat config/.env | xargs)
nohup python src/content_agent.py > logs/agent.log 2>&1 &
```

#### Option D: Systemd Service (Linux)
```bash
# Edit paths in service file
nano ai-content-agent.service

# Install service
sudo cp ai-content-agent.service /etc/systemd/system/
sudo systemctl enable ai-content-agent
sudo systemctl start ai-content-agent

# Check status
sudo systemctl status ai-content-agent
```

## 🔧 How It Works

### Content Generation Cycle (Every 6 Hours)

```
1. Research Phase (30-60 seconds)
   └─ Queries 3 AI topics using Claude via Perplexity
   └─ Gathers insights and trends
   └─ Analyzes current AI landscape

2. Topic Generation (10-15 seconds)
   └─ Creates unique topic from research
   └─ Avoids recently covered topics
   └─ Ensures engagement and relevance

3. Content Creation (30-45 seconds per platform)
   └─ LinkedIn: 3000 chars, conversational + hashtags
   └─ Medium: 2500 chars, in-depth article
   └─ Human-like writing, no AI clichés

4. Publishing (5-10 seconds per platform)
   └─ Posts to LinkedIn via API
   └─ Publishes to Medium via API
   └─ Saves local backup

5. History Update
   └─ Records topic for diversity
   └─ Maintains content quality
```

## ⚙️ Customization

### Adjust Posting Frequency

Edit `config/config.json`:
```json
{
  "agent_settings": {
    "post_interval_hours": 12  // Change from 6 to any number
  }
}
```

### Customize Research Topics

Edit the `topics` array:
```json
{
  "research_settings": {
    "topics": [
      "Your custom AI topic 1",
      "Your custom AI topic 2",
      "..."
    ]
  }
}
```

### Modify Content Style

```json
{
  "content_guidelines": {
    "tone": "casual and friendly",  // Change tone
    "avoid_phrases": ["add your phrases to avoid"],
    "include_elements": ["your requirements"]
  }
}
```

### Change Claude Model

Edit `config/config.json`:
```json
{
  "api_settings": {
    "model": "claude-3-opus"  // Options: claude-3.5-sonnet, claude-3-opus, claude-3-sonnet, claude-3-haiku
  }
}
```

## 📊 Monitoring

### View Real-Time Logs

```bash
# If running directly
tail -f logs/agent.log

# If using Docker
docker-compose logs -f

# If using systemd
journalctl -u ai-content-agent -f
```

### Check Generated Content

```bash
# List all generated posts
ls -la content/

# View specific post
cat content/linkedin_20250101_120000.json

# View recent posts
ls -lt content/ | head -10
```

### Agent Status

The agent logs:
- ✓ Each cycle start/completion
- ✓ Research progress
- ✓ Content generation status
- ✓ Publishing success/failure
- ✓ Any errors with details

## 🔍 Why Perplexity vs Direct Anthropic?

| Feature | Perplexity Edition | Direct Anthropic |
|---------|-------------------|------------------|
| **Setup** | Simpler (one API) | Requires Anthropic SDK |
| **API Format** | OpenAI-compatible | Anthropic native |
| **Latest Model** | Claude 3.5 Sonnet | Claude 4.5 Sonnet |
| **Pricing** | Perplexity pricing | Direct Anthropic pricing |
| **Billing** | Unified | Separate |
| **Best For** | Simplicity, unified API | Absolute latest models |

**This edition is perfect if:**
- ✓ You want simpler setup
- ✓ You prefer unified API management
- ✓ You're already using Perplexity
- ✓ Claude 3.5 Sonnet meets your needs

## 💰 Pricing Estimate

**Perplexity API (Claude 3.5 Sonnet):**
- Check current pricing: https://docs.perplexity.ai/docs/pricing
- Typical cost per post cycle: ~$0.10-0.30
- Daily (4 cycles): ~$0.40-1.20
- Monthly: ~$12-36

**LinkedIn & Medium APIs:**
- Free (posting is free via official APIs)

## 🛠️ Troubleshooting

### "PERPLEXITY_API_KEY not found"
```bash
export PERPLEXITY_API_KEY='pplx-your-key'
```

### "401 Unauthorized" from Perplexity
- Check your API key is correct
- Verify account has credits/active subscription
- Test key at: https://www.perplexity.ai/settings/api

### "LinkedIn API error: 401"
- Regenerate LinkedIn access token
- Ensure `w_member_social` scope is enabled
- Check token hasn't expired

### "Content not posting"
1. Check logs: `tail -f logs/agent.log`
2. Verify all API credentials
3. Run: `python test_setup.py`
4. Test individually: `python test_content_generation.py`

### "Request timeout"
- Check internet connection
- Perplexity API may be slow during peak times
- Increase timeout in code if needed

### "Rate limit exceeded"
- Wait and retry (automatic in agent)
- Upgrade Perplexity plan for higher limits
- Increase posting interval

## 📁 Project Structure

```
ai-content-agent-perplexity/
├── src/
│   └── content_agent.py          # Main agent (Perplexity integration)
├── config/
│   ├── config.json                # Agent configuration
│   └── .env.template              # Environment template
├── content/                        # Generated posts (auto-created)
├── logs/                          # Application logs (auto-created)
├── test_setup.py                  # Setup verification
├── test_content_generation.py     # Manual test
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Docker orchestration
└── requirements.txt               # Python dependencies
```

## 🔐 Security Best Practices

1. **Never commit `.env` file**
   - Already in `.gitignore`
   - Contains sensitive API keys

2. **Rotate API keys regularly**
   - LinkedIn tokens every 60 days
   - Perplexity keys every 90 days

3. **Use environment variables**
   - Never hardcode credentials
   - Use `.env` file for local dev

4. **Monitor API usage**
   - Check Perplexity dashboard regularly
   - Set up billing alerts

5. **Secure the server**
   - Run as non-root user (Docker handles this)
   - Keep system updated
   - Use firewall rules

## 🎓 Advanced Usage

### Multiple Accounts

Run multiple instances with different configs:
```bash
# Account 1
export $(cat config/.env.account1 | xargs)
python src/content_agent.py &

# Account 2
export $(cat config/.env.account2 | xargs)
python src/content_agent.py &
```

### Custom Research Integration

Modify `research_ai_topics()` to use additional APIs:
- Google Custom Search
- NewsAPI
- ArXiv for academic papers
- Twitter API for trending topics

### Webhook Notifications

Add to `.env`:
```bash
WEBHOOK_URL=https://hooks.slack.com/your-webhook
```

Agent will notify on cycle completion/errors.

## 📚 Resources

### Perplexity
- **Get API Key**: https://www.perplexity.ai/settings/api
- **Documentation**: https://docs.perplexity.ai
- **Pricing**: https://docs.perplexity.ai/docs/pricing

### Social Media APIs
- **LinkedIn Developers**: https://www.linkedin.com/developers/
- **Medium API**: https://github.com/Medium/medium-api-docs

### Support
- Check logs first: `tail -100 logs/agent.log`
- Run diagnostics: `python test_setup.py`
- Test content: `python test_content_generation.py`

## 🤝 Contributing

Found a bug or want to improve the agent? 
- Test thoroughly before deploying
- Keep API keys secure
- Document any changes

## 📄 License

MIT License - Free to use and modify

## ⚠️ Disclaimer

This agent generates content autonomously. Always:
- Review content quality regularly
- Ensure compliance with platform policies
- Respect rate limits and terms of service
- Monitor for any issues

---

**Ready to start?** Run `python test_setup.py` to begin! 🚀
