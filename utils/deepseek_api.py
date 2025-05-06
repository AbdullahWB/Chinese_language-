"""
Utility class for interacting with the DeepSeek API using OpenAI SDK.
"""

import os
import json
from typing import Dict, Any, Optional, Tuple
from decouple import config
import logging
import time
from openai import OpenAI
from django.conf import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekAPI:
    """A class to handle interactions with the DeepSeek API using OpenAI SDK."""
    
    def __init__(self):
        """Initialize the DeepSeek API client."""
        self.api_key = settings.DEEPSEEK_API_KEY
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-chat"

    def test_connection(self) -> Tuple[bool, str]:
        """Test the connection to the DeepSeek API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=50
            )
            return True, "Connection successful"
        except Exception as e:
            logger.error(f"API connection error: {str(e)}")
            return False, f"Connection failed: {str(e)}"

    def generate_response(self, user_message: str) -> str:
        """Generate a response to a user message.
        
        Args:
            user_message: The message from the user
            
        Returns:
            str: The generated response or error message
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Chinese language learning assistant. You can help with translations, grammar explanations, and general language learning questions. Always provide explanations in both English and Chinese when appropriate."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"

    def get_grammar_explanation(self, title: str, pattern: str, example: str, language: str = 'en') -> Dict[str, Any]:
        """Get an explanation for a grammar point."""
        try:
            prompt = self._construct_grammar_prompt(title, pattern, example, language)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Chinese language expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            explanation = response.choices[0].message.content
            return self._parse_grammar_response(explanation)
        except Exception as e:
            logger.error(f"Error getting grammar explanation: {str(e)}")
            return {
                "error": True,
                "message": str(e)
            }

    def _construct_grammar_prompt(self, title: str, pattern: str, example: str, language: str) -> str:
        """Construct the prompt for grammar explanation."""
        if language == 'zh':
            return f"""请解释以下中文语法点：
标题：{title}
语法规则：{pattern}
例句：{example}

请提供以下格式的解释：
1. 详细解释
2. 使用说明
3. 更多例子
4. 常见错误"""
        else:
            return f"""Please explain the following Chinese grammar point:
Title: {title}
Pattern: {pattern}
Example: {example}

Please provide the explanation in the following format:
1. Detailed Explanation
2. Usage Notes
3. Additional Examples
4. Common Mistakes"""

    def _parse_grammar_response(self, response: str) -> Dict[str, Any]:
        """Parse the API response into structured data."""
        try:
            sections = response.split('\n\n')
            explanation = {
                "detailed_explanation": "",
                "usage_notes": "",
                "additional_examples": "",
                "common_mistakes": "",
                "error": False
            }
            
            current_section = "detailed_explanation"
            for section in sections:
                if "Usage Notes" in section or "使用说明" in section:
                    current_section = "usage_notes"
                elif "Additional Examples" in section or "更多例子" in section:
                    current_section = "additional_examples"
                elif "Common Mistakes" in section or "常见错误" in section:
                    current_section = "common_mistakes"
                
                explanation[current_section] += section + "\n"
            
            return explanation
        except Exception as e:
            logger.error(f"Error parsing grammar response: {str(e)}")
            return {
                "error": True,
                "message": f"Failed to parse response: {str(e)}"
            }

# Create a singleton instance
deepseek_api = DeepSeekAPI()