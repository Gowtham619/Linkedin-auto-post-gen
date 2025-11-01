"""
AI Content Generation & Auto-Posting Agent - HUMAN-LIKE VERSION
Uses Perplexity API to access Claude models
Generates authentic, human-like AI content with titles for LinkedIn
Posts to LinkedIn and Medium every 6 hours
macOS Compatible Version
"""

import os
import time
import json
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import schedule
import logging
from dotenv import load_dotenv

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / 'config' / '.env')
LOGS_DIR = PROJECT_ROOT / 'logs'
CONTENT_DIR = PROJECT_ROOT / 'content'
CONFIG_DIR = PROJECT_ROOT / 'config'

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
CONTENT_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PerplexityClaudeClient:
    """Client for accessing Claude models via Perplexity API"""
    
    def __init__(self):
        """Initialize Perplexity client"""
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable required")
        
        self.base_url = "https://api.perplexity.ai"
        self.default_model = "sonar"
        logger.info("Perplexity Claude client initialized")
    
    def create_completion(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> str:
        """
        Create a completion using Claude via Perplexity
        
        Args:
            prompt: The prompt to send to Claude
            max_tokens: Maximum tokens in response
            temperature: Randomness (0.0-1.0)
            model: Claude model to use (default: sonar)
        
        Returns:
            Generated text response
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                logger.error(f"Perplexity API error: {response.status_code} - {response.text}")
                raise Exception(f"API Error {response.status_code}: {response.text}")
        
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            raise Exception("API request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")


class AIContentAgent:
    """Agent for researching AI topics and generating authentic human-like content"""
    
    def __init__(self, config_path: str):
        self.load_config(config_path)
        self.claude_client = PerplexityClaudeClient()
        self.content_history = []
        self.load_content_history()
        logger.info("AI Content Agent initialized successfully")
        
    def load_config(self, config_path: str):
        """Load configuration from JSON file"""
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                config_file = CONFIG_DIR / 'config.json'
            
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            raise
    
    def load_content_history(self):
        """Load previously generated content to avoid repetition"""
        history_file = CONTENT_DIR / 'history.json'
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    self.content_history = json.load(f)
                logger.info(f"Loaded {len(self.content_history)} items from content history")
            except Exception as e:
                logger.warning(f"Could not load content history: {str(e)}")
                self.content_history = []
        else:
            logger.info("No content history found, starting fresh")
    
    def save_content_history(self, content: Dict):
        """Save generated content to history"""
        self.content_history.append({
            'timestamp': datetime.now().isoformat(),
            'title': content['title'],
            'topic': content['topic']
        })
        
        # Keep only last 50 entries
        self.content_history = self.content_history[-50:]
        
        history_file = CONTENT_DIR / 'history.json'
        try:
            with open(history_file, 'w') as f:
                json.dump(self.content_history, f, indent=2)
            logger.info("Content history updated")
        except Exception as e:
            logger.error(f"Failed to save history: {str(e)}")
    
    def research_ai_topics(self) -> List[Dict]:
        """Deep research on current AI trends and topics"""
        logger.info("Starting deep research on AI topics...")
        
        research_queries = self.config['research_settings']['topics']
        
        # Select random queries to keep content diverse
        num_queries = self.config['research_settings']['queries_per_cycle']
        selected_queries = random.sample(research_queries, k=min(num_queries, len(research_queries)))
        
        research_results = []
        for query in selected_queries:
            try:
                logger.info(f"Researching: {query}")
                insights = self._generate_research_insights(query)
                
                result = {
                    'query': query,
                    'insights': insights
                }
                research_results.append(result)
                logger.info(f"✓ Completed research for: {query}")
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Research error for '{query}': {str(e)}")
        
        return research_results
    
    def _generate_research_insights(self, query: str) -> str:
        """Generate research insights using Claude via Perplexity"""
        prompt = f"""You are an AI research assistant. Provide 3-5 key insights about: {query}

Focus on:
- Recent developments and trends
- Real-world applications and use cases
- Impact on businesses and society
- Future implications and predictions
- Specific examples where possible

Keep insights factual, specific, current, and actionable.
Write in a clear, professional yet conversational tone."""

        try:
            insights = self.claude_client.create_completion(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7
            )
            return insights
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return f"Research insights for {query} (placeholder due to error)"
    
    def generate_content_topic(self, research_results: List[Dict]) -> str:
        """Generate a unique content topic based on research"""
        logger.info("Generating unique content topic...")
        
        # Combine research insights
        combined_insights = "\n\n".join([
            f"Topic: {r['query']}\nInsights: {r['insights']}" 
            for r in research_results
        ])
        
        # Get recent topics to avoid repetition
        recent_topics = [h['topic'] for h in self.content_history[-10:]]
        
        prompt = f"""Based on the following AI research insights, suggest ONE specific, engaging article topic that would be valuable for LinkedIn and Medium audiences.

Research Insights:
{combined_insights}

Recent topics to AVOID repeating:
{', '.join(recent_topics) if recent_topics else 'None'}

Requirements:
- Must be specific and actionable (not generic)
- Should appeal to professionals, tech leaders, and AI enthusiasts
- Must be completely different from recent topics
- Should provide unique value or fresh perspective
- Should be timely and relevant to current AI landscape
- Make it sound intriguing and click-worthy

Respond with ONLY the topic title (8-12 words maximum). No quotes, no explanation, just the title."""

        try:
            topic = self.claude_client.create_completion(
                prompt=prompt,
                max_tokens=100,
                temperature=0.8
            )
            topic = topic.strip().strip('"').strip("'")
            logger.info(f"Generated topic: {topic}")
            return topic
        except Exception as e:
            logger.error(f"Error generating topic: {str(e)}")
            # Fallback topic
            fallback_topics = [
                "Why I Stopped Trusting AI Blindly (And What Changed)",
                "The $50K Mistake That Taught Me About AI Implementation",
                "3 AI Tools That Actually Save Me 10 Hours a Week",
                "What Nobody Tells You About Building AI Products"
            ]
            return random.choice(fallback_topics)
    
    def generate_human_like_content(self, topic: str, platform: str) -> Optional[Dict]:
        """Generate authentic, human-like content with title for specified platform"""
        logger.info(f"Generating {platform.upper()} content for: {topic}")
        
        # Platform-specific parameters
        platform_config = self.config['agent_settings']['max_content_length']
        guidelines = self.config['content_guidelines']
        
        if platform == "linkedin":
            max_length = platform_config.get('linkedin', 3000)
            style = "authentic personal story, conversational like talking to a friend"
            include_hashtags = True
            structure_note = "LinkedIn post with title at top"
        else:  # medium
            max_length = platform_config.get('medium', 5000)
            style = "thoughtful, personal essay with depth"
            include_hashtags = False
            structure_note = "Full article with ## headings"
        
        # Build avoid phrases list
        avoid_phrases = ', '.join(guidelines['avoid_phrases'])
        
        # Generate content under limit
        target_length = max_length - 250 if platform == "linkedin" else max_length - 500
        
        prompt = f"""You are writing an authentic, personal LinkedIn post about: "{topic}"

CRITICAL: Make this sound like a REAL HUMAN wrote it, not AI. Be conversational, personal, and genuine.

FORMAT FOR LINKEDIN POST:
[Start with a catchy title using emoji - keep it under 60 characters]

[Leave one blank line]

[Then your hook - first 210 characters MUST grab attention because that's what shows before "see more"]

WRITING STYLE - MAKE IT HUMAN:
✓ Write like you're texting a smart friend about something exciting you discovered
✓ Start with a personal story, "last week...", "I remember when...", "here's what shocked me..."
✓ Use contractions liberally: I'm, you're, don't, can't, won't, it's, there's
✓ Include 2-3 personal opinions or hot takes
✓ Use metaphors and analogies: "it's like...", "imagine if...", "think of it as..."
✓ Add 1-2 light emojis for emphasis (but don't overdo it)
✓ Vary sentence length: Mix super short punchy ones. With longer explanatory ones that flow naturally.
✓ Use casual transitions: "Look", "Here's the thing", "Real talk", "But here's what's crazy"
✓ Include rhetorical questions: "What if I told you...?", "Sound familiar?"
✓ Share specific numbers, examples, or real situations
✓ Show vulnerability or admit mistakes: "I was wrong about...", "This surprised me..."
✓ Add strategic line breaks for mobile readability (every 2-3 sentences)
✓ Use symbols sparingly: → ✓ • for visual structure

AVOID THESE AI RED FLAGS:
✗ NEVER use: {avoid_phrases}
✗ Don't start every sentence the same way
✗ Don't make every paragraph the same length
✗ Don't sound preachy or lecture-y
✗ Don't use corporate jargon or buzzwords
✗ Don't be overly formal or stiff

CONTENT STRUCTURE:
1. Eye-catching title with emoji (1 line)
2. Blank line
3. Hook (first 210 chars - make them count!)
4. Personal story or observation (2-3 short paragraphs)
5. Key insight with specific example (1-2 paragraphs)
6. Practical takeaway or lesson (1-2 paragraphs)
7. Relatable conclusion or question (1 paragraph)
8. Call to action: "What's your take?" or "Have you seen this too?"
9. Blank line
10. 3-5 hashtags on separate lines

TONE: Friendly expert sharing a coffee chat, not a textbook

CHARACTER LIMIT: MUST stay under {target_length} characters (count carefully!)

EXAMPLE OF HUMAN STYLE:
"Last Tuesday, I watched our AI model completely fail at something a 5-year-old could do. 

And honestly? It was the best thing that happened all week.

Here's why..."

Now write the complete LinkedIn post about "{topic}" in this authentic, human style. Make me believe a real person wrote this."""

        try:
            content = self.claude_client.create_completion(
                prompt=prompt,
                max_tokens=self.config['api_settings']['max_tokens'],
                temperature=0.85  # Higher temperature for more natural variation
            )
            
            # Extract title from content (first line)
            lines = content.split('\n', 1)
            if len(lines) > 1:
                title = lines[0].strip()
                # Remove emojis and extra formatting from title for storage
                title_clean = ''.join(char for char in title if char.isalnum() or char.isspace() or char in ['-', ':', '!', '?']).strip()
            else:
                title_clean = topic
            
            # AGGRESSIVE TRIMMING - Always enforce strict limit
            if len(content) > max_length:
                logger.warning(f"Content too long ({len(content)} chars), trimming to {max_length}")
                
                # Find last complete sentence before limit with safety buffer
                trim_position = max_length - 100
                
                # Look for sentence endings
                last_period = content[:trim_position].rfind('.')
                last_exclamation = content[:trim_position].rfind('!')
                last_question = content[:trim_position].rfind('?')
                
                # Use the last sentence ending found
                cut_position = max(last_period, last_exclamation, last_question)
                
                if cut_position > 0:
                    content = content[:cut_position + 1]
                else:
                    # Fallback: cut at last space
                    content = content[:trim_position].rsplit(' ', 1)[0] + "..."
            
            # FINAL VALIDATION
            if len(content) > max_length:
                logger.error(f"Content still too long after trimming: {len(content)} chars")
                content = content[:max_length - 3] + "..."
            
            final_length = len(content)
            logger.info(f"✓ Final content length: {final_length} characters (limit: {max_length})")
            
            result = {
                'topic': topic,
                'title': title_clean if 'title_clean' in locals() else topic,
                'content': content,
                'platform': platform,
                'generated_at': datetime.now().isoformat(),
                'character_count': final_length
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return None
    
    def post_to_linkedin(self, content: Dict) -> bool:
        """Post content with title to LinkedIn using their API"""
        logger.info("Posting to LinkedIn...")
        
        # The content already includes the title at the top
        post_content = content['content']
        
        # LinkedIn strict limit is 3000 characters
        LINKEDIN_LIMIT = 3000
        
        if len(post_content) > LINKEDIN_LIMIT:
            logger.error(f"Content exceeds LinkedIn limit: {len(post_content)} characters")
            # Emergency trim
            trim_position = LINKEDIN_LIMIT - 100
            last_period = post_content[:trim_position].rfind('.')
            if last_period > 0:
                post_content = post_content[:last_period + 1]
            else:
                post_content = post_content[:LINKEDIN_LIMIT - 3] + "..."
            logger.warning(f"Emergency trim applied, new length: {len(post_content)}")
        
        # Final check
        if len(post_content) > LINKEDIN_LIMIT:
            logger.error(f"Content STILL too long: {len(post_content)}, forcing hard trim")
            post_content = post_content[:LINKEDIN_LIMIT - 3] + "..."
        
        logger.info(f"Final post length: {len(post_content)} characters")
        logger.info(f"Post preview (first 150 chars): {post_content[:150]}...")
        
        try:
            url = "https://api.linkedin.com/v2/ugcPosts"
            
            headers = {
                "Authorization": f"Bearer {os.environ.get('LINKEDIN_ACCESS_TOKEN')}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            person_urn = os.environ.get('LINKEDIN_PERSON_URN')
            
            payload = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": post_content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            logger.info(f"Sending {len(post_content)} character post to LinkedIn API")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                logger.info("✓ Successfully posted to LinkedIn")
                return True
            else:
                logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {str(e)}")
            return False
    
    def post_to_medium(self, content: Dict) -> bool:
        """Post full article to Medium using their API"""
        logger.info("Posting to Medium...")
        
        # Check if Medium token is configured
        if not os.environ.get('MEDIUM_INTEGRATION_TOKEN'):
            logger.info("Medium token not configured, skipping Medium post")
            return False
        
        try:
            integration_token = os.environ.get('MEDIUM_INTEGRATION_TOKEN')
            
            headers = {
                "Authorization": f"Bearer {integration_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Get user ID
            user_response = requests.get(
                "https://api.medium.com/v1/me",
                headers=headers,
                timeout=30
            )
            
            if user_response.status_code != 200:
                logger.error(f"Failed to get Medium user: {user_response.text}")
                return False
            
            user_id = user_response.json()['data']['id']
            
            # Post article
            url = f"https://api.medium.com/v1/users/{user_id}/posts"
            
            payload = {
                "title": content['title'],
                "contentFormat": "markdown",
                "content": content['content'],
                "publishStatus": "public",
                "tags": ["artificial-intelligence", "ai", "technology", "machine-learning", "innovation"]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                post_url = response.json()['data']['url']
                logger.info(f"✓ Successfully posted to Medium: {post_url}")
                return True
            else:
                logger.error(f"Medium API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error posting to Medium: {str(e)}")
            return False
    
    def save_content_locally(self, content: Dict):
        """Save generated content locally as backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform = content['platform']
        filename = CONTENT_DIR / f"{platform}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(content, f, indent=2)
            
            # Also save as readable text file
            text_filename = CONTENT_DIR / f"{platform}_{timestamp}.txt"
            with open(text_filename, 'w') as f:
                f.write(f"TITLE: {content['title']}\n")
                f.write(f"PLATFORM: {content['platform']}\n")
                f.write(f"GENERATED: {content['generated_at']}\n")
                f.write(f"LENGTH: {content['character_count']} characters\n")
                f.write("\n" + "="*70 + "\n\n")
                f.write(content['content'])
            
            logger.info(f"Content saved: {filename} and {text_filename}")
        except Exception as e:
            logger.error(f"Failed to save content locally: {str(e)}")
    
    def run_content_cycle(self):
        """Complete content generation and posting cycle"""
        logger.info("=" * 70)
        logger.info("STARTING NEW CONTENT GENERATION CYCLE")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        
        try:
            # Step 1: Deep research
            logger.info("\n[1/5] Conducting deep research on AI topics...")
            research_results = self.research_ai_topics()
            
            if not research_results:
                logger.error("❌ Research failed, skipping cycle")
                return
            
            logger.info(f"✓ Completed research on {len(research_results)} topics")
            
            # Step 2: Generate topic
            logger.info("\n[2/5] Generating unique content topic...")
            topic = self.generate_content_topic(research_results)
            logger.info(f"✓ Topic: {topic}")
            
            # Step 3: Generate LinkedIn content with title
            logger.info("\n[3/5] Generating authentic LinkedIn post with title...")
            linkedin_content = self.generate_human_like_content(topic, "linkedin")
            
            if linkedin_content:
                self.save_content_locally(linkedin_content)
                logger.info(f"✓ Post title: {linkedin_content['title']}")
                
                # Post to LinkedIn
                if self.post_to_linkedin(linkedin_content):
                    logger.info("✓ LinkedIn posting successful")
                else:
                    logger.warning("⚠ LinkedIn posting failed (content saved locally)")
            else:
                logger.error("❌ LinkedIn content generation failed")
            
            time.sleep(5)  # Small delay between posts
            
            # Step 4: Generate Medium article (if configured)
            if 'medium' in self.config['agent_settings'].get('platforms', ['linkedin']):
                logger.info("\n[4/5] Generating Medium article...")
                medium_content = self.generate_human_like_content(topic, "medium")
                
                if medium_content:
                    self.save_content_locally(medium_content)
                    
                    # Post to Medium
                    if self.post_to_medium(medium_content):
                        logger.info("✓ Medium posting successful")
                    else:
                        logger.warning("⚠ Medium posting failed (content saved locally)")
                else:
                    logger.error("❌ Medium content generation failed")
            else:
                logger.info("\n[4/5] Medium not configured, skipping")
            
            # Step 5: Update history
            logger.info("\n[5/5] Updating content history...")
            if linkedin_content:
                self.save_content_history(linkedin_content)
            
            logger.info("\n" + "=" * 70)
            logger.info("✓ CONTENT CYCLE COMPLETED SUCCESSFULLY")
            logger.info(f"Next cycle in {self.config['agent_settings']['post_interval_hours']} hours")
            logger.info("=" * 70 + "\n")
            
        except Exception as e:
            logger.error(f"❌ Error in content cycle: {str(e)}")
            logger.exception("Full traceback:")


def main():
    """Main function to run the agent continuously"""
    logger.info("=" * 70)
    logger.info("AI CONTENT AGENT - AUTHENTIC HUMAN-LIKE POSTS")
    logger.info("Generates LinkedIn posts with titles in natural, conversational style")
    logger.info("Using Perplexity API to access Claude models")
    logger.info("=" * 70)
    
    try:
        # Check for required environment variables
        required_vars = ['PERPLEXITY_API_KEY']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.error("Please set all required variables before starting the agent")
            return
        
        # Initialize agent
        config_path = CONFIG_DIR / "config.json"
        agent = AIContentAgent(str(config_path))
        
        # Get posting interval
        interval_hours = agent.config['agent_settings']['post_interval_hours']
        
        # Schedule posts
        schedule.every(interval_hours).hours.do(agent.run_content_cycle)
        
        # Run immediately on startup
        logger.info(f"Running initial content generation cycle...")
        agent.run_content_cycle()
        
        logger.info(f"\n✓ Agent is now running continuously")
        logger.info(f"✓ Posts will be generated every {interval_hours} hours")
        logger.info(f"✓ Each post includes a catchy title at the top")
        logger.info(f"✓ Content styled to sound authentically human")
        logger.info(f"✓ Press Ctrl+C to stop\n")
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("\n\n" + "=" * 70)
        logger.info("Agent stopped by user")
        logger.info("=" * 70)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.exception("Full traceback:")


if __name__ == "__main__":
    main()
