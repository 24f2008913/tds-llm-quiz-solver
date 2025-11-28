"""
LLM Handler - Manages interactions with Language Models
"""
import os
import logging
from typing import Optional, Union, Dict, Any
import json

logger = logging.getLogger(__name__)


class LLMHandler:
    """Handles interactions with OpenAI and Anthropic LLMs"""
    
    def __init__(self, model: Optional[str] = None):
        # AI Pipe configuration
        self.aipipe_token = os.getenv('AIPIPE_TOKEN')
        self.openai_base_url = os.getenv('OPENAI_BASE_URL', 'https://aipipe.org/openai/v1')
        self.model = model or os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')
        self.temperature = float(os.getenv('TEMPERATURE', 0.1))
        self.max_tokens = int(os.getenv('MAX_TOKENS', 4096))
        
        # Initialize OpenAI client with AI Pipe
        self.openai_client = None
        
        if self.aipipe_token:
            from openai import OpenAI
            self.openai_client = OpenAI(
                api_key=self.aipipe_token,
                base_url=self.openai_base_url
            )
            logger.info(f"AI Pipe client initialized with base URL: {self.openai_base_url}")
        else:
            logger.warning("AI Pipe token not configured")
    
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """
        Generate a completion using the configured LLM
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Temperature override
            max_tokens: Max tokens override
            json_mode: Whether to request JSON output
        
        Returns:
            Generated text
        """
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens
        
        # All models go through AI Pipe's OpenAI-compatible endpoint
        return self._openai_completion(prompt, system_prompt, temp, max_tok, json_mode)
    
    def _openai_completion(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        json_mode: bool
    ) -> str:
        """Generate completion using AI Pipe"""
        if not self.openai_client:
            raise ValueError("AI Pipe token not configured")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            
            response = self.openai_client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI Pipe API error: {str(e)}")
            raise
    
    def analyze_quiz_question(self, question_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a quiz question and determine how to solve it
        
        Args:
            question_text: The quiz question text
            context: Additional context (HTML, links, etc.)
        
        Returns:
            Analysis with task type, required actions, etc.
        """
        system_prompt = """You are an expert data analyst and programmer. 
Analyze quiz questions and determine the best approach to solve them.
Return your analysis as JSON with these fields:
- task_type: (e.g., "data_analysis", "web_scraping", "pdf_processing", "visualization")
- steps: array of steps needed to solve
- data_sources: URLs or files mentioned
- answer_format: expected format (number, string, json, image)
- tools_needed: list of tools/libraries needed
"""
        
        prompt = f"""Question: {question_text}

Context:
{json.dumps(context, indent=2)}

Analyze this question and provide a structured plan to solve it."""
        
        response = self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=True
        )
        
        return json.loads(response)
    
    def generate_answer(self, question: str, data: Any, analysis: Dict[str, Any]) -> Any:
        """
        Generate the final answer based on question and processed data
        
        Args:
            question: The quiz question
            data: Processed data
            analysis: Question analysis
        
        Returns:
            The answer in appropriate format
        """
        system_prompt = """You are a precise data analyst answering quiz questions.
CRITICAL: Return ONLY the raw answer value. No JSON, no code blocks, no markdown, no explanations.
Examples:
- If asked for a number: return "42"  
- If asked for a secret code: return "ABC123"
- If asked for text: return just the text
Never wrap your answer in JSON or code blocks."""
        
        prompt = f"""Question: {question}

Data Summary:
{str(data)[:2000]}  # Truncate to avoid token limits

Task Analysis:
{json.dumps(analysis, indent=2)}

Return ONLY the answer value. No extra formatting, no code blocks, no JSON structure."""
        
        response = self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt
        )
        
        # Try to parse answer based on expected format
        answer_format = analysis.get('answer_format', 'string')
        
        if answer_format == 'number':
            try:
                return int(response.strip())
            except ValueError:
                try:
                    return float(response.strip())
                except ValueError:
                    return response.strip()
        elif answer_format == 'boolean':
            return response.strip().lower() in ['true', 'yes', '1']
        elif answer_format == 'json':
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return response
        else:
            return response.strip()
