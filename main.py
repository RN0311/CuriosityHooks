import openai
from typing import List, Dict
import json
import time
from datetime import datetime

class TweetEnhancer:
    def __init__(self, api_key: str):
        openai.api_key = ""

        self.prompt_strategies = {
            "curiosity_gap": self._create_curiosity_gap_prompt,
            "emotional_hook": self._create_emotional_hook_prompt,
            "value_proposition": self._create_value_prop_prompt,
            "story_hook": self._create_story_hook_prompt
        }

    def _create_curiosity_gap_prompt(self, tweet: str) -> str:
        """Creates a prompt that focuses on generating curiosity through information gaps"""
        return """Transform this tweet to create curiosity by hinting at valuable information without revealing everything.
        Use techniques like:
        - Pose a thought-provoking question
        - Hint at unexpected results
        - Create anticipation
        
        Original tweet: "{tweet}"
        
        Provide response in JSON format:
        {{
            "enhanced_tweet": "the enhanced version",
            "technique_used": "specific technique used",
            "engagement_elements": ["list of engaging elements added"]
        }}"""

    def _create_emotional_hook_prompt(self, tweet: str) -> str:
        """Creates a prompt that focuses on emotional engagement"""
        return """Transform this tweet to create emotional resonance while maintaining authenticity.
        Use techniques like:
        - Personal connection
        - Relatable situations
        - Emotional triggers (triumph, surprise, wonder)
        
        Original tweet: "{tweet}"
        
        Provide response in JSON format:
        {{
            "enhanced_tweet": "the enhanced version",
            "emotion_type": "primary emotion targeted",
            "engagement_elements": ["list of engaging elements added"]
        }}"""

    def _create_value_prop_prompt(self, tweet: str) -> str:
        """Creates a prompt that emphasizes value proposition"""
        return """Transform this tweet to highlight clear value to the reader.
        Use techniques like:
        - Clear benefit statement
        - Problem-solution framing
        - Actionable insights
        
        Original tweet: "{tweet}"
        
        Provide response in JSON format:
        {{
            "enhanced_tweet": "the enhanced version",
            "value_offered": "main benefit to reader",
            "engagement_elements": ["list of engaging elements added"]
        }}"""

    def _create_story_hook_prompt(self, tweet: str) -> str:
        """Creates a prompt that uses storytelling elements"""
        return """Transform this tweet to include storytelling elements that hook attention.
        Use techniques like:
        - Open story loops
        - Intriguing scenarios
        - Personal narratives
        
        Original tweet: "{tweet}"
        
        Provide response in JSON format:
        {{
            "enhanced_tweet": "the enhanced version",
            "story_element": "type of story hook used",
            "engagement_elements": ["list of engaging elements added"]
        }}"""

    def enhance_tweet(self, tweet: str, strategy: str = "curiosity_gap") -> Dict:
        """Enhance a single tweet using specified strategy"""
        if strategy not in self.prompt_strategies:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        prompt = self.prompt_strategies[strategy](tweet)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in creating engaging social media content that hooks reader attention while maintaining authenticity."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            result['original_tweet'] = tweet
            result['strategy_used'] = strategy
            return result
            
        except Exception as e:
            print(f"Error enhancing tweet: {str(e)}")
            return {"error": str(e), "original_tweet": tweet}

    def enhance_batch(self, tweets: List[str], strategies: List[str] = None) -> List[Dict]:
        """Enhance a batch of tweets, optionally using different strategies"""
        if strategies is None:
            strategies = ["curiosity_gap"] * len(tweets)
        
        results = []
        for tweet, strategy in zip(tweets, strategies):
            result = self.enhance_tweet(tweet, strategy)
            results.append(result)
            time.sleep(1) 
        
        return results

def analyze_effectiveness(original_tweets: List[str], enhanced_results: List[Dict]) -> Dict:
    """Analyze the effectiveness of enhancements"""
    analysis = {
        "total_tweets": len(original_tweets),
        "strategies_used": {},
        "avg_length_change": 0,
        "enhancement_elements": {}
    }
    
    for result in enhanced_results:
        if "error" in result:
            continue
            
        strategy = result["strategy_used"]
        analysis["strategies_used"][strategy] = analysis["strategies_used"].get(strategy, 0) + 1
        
        for element in result.get("engagement_elements", []):
            analysis["enhancement_elements"][element] = analysis["enhancement_elements"].get(element, 0) + 1
        
        original_len = len(result["original_tweet"])
        enhanced_len = len(result["enhanced_tweet"])
        analysis["avg_length_change"] += (enhanced_len - original_len)
    
    analysis["avg_length_change"] /= len(enhanced_results)
    
    return analysis

if __name__ == "__main__":
    sample_tweets = [
        "Just released our new product features",
        "Here's how I learned to code in Python",
        "Check out these productivity tips",
        "New research shows interesting results about sleep patterns"
    ]

    enhancer = TweetEnhancer("")
    
    strategies = ["curiosity_gap", "emotional_hook", "value_proposition", "story_hook"]
    results = enhancer.enhance_batch(sample_tweets, strategies)
    
    for result in results:
        if "error" not in result:
            print("\nOriginal:", result["original_tweet"])
            print("Enhanced:", result["enhanced_tweet"])
            print("Strategy:", result["strategy_used"])
            print("Elements:", result["engagement_elements"])
            print("-" * 50)
    
    analysis = analyze_effectiveness(sample_tweets, results)
    print("\nAnalysis:", json.dumps(analysis, indent=2))
