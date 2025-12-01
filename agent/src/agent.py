"""
HoneyGo Dynamic Pricing Agent - ReAct Agent with LangSmith Observability

This agent makes intelligent pricing decisions by:
1. Analyzing ride characteristics (distance, passengers, city)
2. Checking historical data for similar rides
3. Fetching weather conditions
4. Calculating optimal price balancing rider satisfaction and driver earnings
5. Providing explainable reasoning for transparency
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import LangChainTracer
from langsmith import Client
import os
from typing import Dict, Any

from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    GOOGLE_API_KEY,
    AGENT_MODEL,
    AGENT_TEMPERATURE,
    AGENT_MAX_ITERATIONS,
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    LANGSMITH_TRACING,
    VERBOSE
)
from tools import PricingCalculatorTool, DatabaseQueryTool, WeatherDataTool


# Initialize LangSmith client for observability
if LANGSMITH_TRACING and LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
    langsmith_client = Client()
    print(f"✅ LangSmith observability enabled - Project: {LANGSMITH_PROJECT}")
else:
    print("⚠️  LangSmith observability disabled - Set LANGSMITH_API_KEY to enable")


# Define the agent prompt
PRICING_AGENT_PROMPT = PromptTemplate.from_template("""
You are an expert dynamic pricing agent for HoneyGo ride-sharing platform.

Your goal is to determine the optimal price that:
1. Maximizes rider satisfaction (fair pricing)
2. Ensures driver earnings are competitive (retention)
3. Responds to real-time market conditions
4. Considers weather, traffic, and demand

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT: Always provide detailed reasoning for your pricing decision.
Consider: distance, city market, weather conditions, historical data, driver earnings.

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")


class HoneyGoPricingAgent:
    """Main pricing agent with LangSmith observability"""
    
    def _initialize_llm_with_fallback(self):
        """
        Initialize LLM with automatic fallback chain for resilience.
        Tries providers in order: OpenAI → Google AI → Anthropic
        Uses whichever API key is available and working.
        """
        errors = []
        
        # Strategy 1: Try explicit LLM_PROVIDER first if set
        if LLM_PROVIDER == "google" and GOOGLE_API_KEY:
            try:
                llm = ChatGoogleGenerativeAI(
                    model=AGENT_MODEL,
                    temperature=AGENT_TEMPERATURE,
                    google_api_key=GOOGLE_API_KEY
                )
                print(f"✅ Using Google AI (Gemini): {AGENT_MODEL}")
                return llm
            except Exception as e:
                errors.append(f"Google AI failed: {str(e)}")
                print(f"⚠️  Google AI failed, trying fallback...")
        
        # Strategy 2: Try OpenAI (most common for hackathons)
        if OPENAI_API_KEY:
            try:
                llm = ChatOpenAI(
                    model=AGENT_MODEL if LLM_PROVIDER == "openai" else "gpt-4-turbo-preview",
                    temperature=AGENT_TEMPERATURE,
                    openai_api_key=OPENAI_API_KEY
                )
                print(f"✅ Using OpenAI: {llm.model_name}")
                return llm
            except Exception as e:
                errors.append(f"OpenAI failed: {str(e)}")
                print(f"⚠️  OpenAI failed, trying fallback...")
        
        # Strategy 3: Fallback to Google AI if not tried yet
        if LLM_PROVIDER != "google" and GOOGLE_API_KEY:
            try:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    temperature=AGENT_TEMPERATURE,
                    google_api_key=GOOGLE_API_KEY
                )
                print(f"✅ Using Google AI (fallback): gemini-pro")
                return llm
            except Exception as e:
                errors.append(f"Google AI (fallback) failed: {str(e)}")
                print(f"⚠️  Google AI failed, trying Anthropic...")
        
        # Strategy 4: Final fallback to Anthropic
        if ANTHROPIC_API_KEY:
            try:
                from langchain_anthropic import ChatAnthropic
                llm = ChatAnthropic(
                    model="claude-3-sonnet-20240229",
                    temperature=AGENT_TEMPERATURE,
                    anthropic_api_key=ANTHROPIC_API_KEY
                )
                print(f"✅ Using Anthropic Claude (fallback): claude-3-sonnet")
                return llm
            except Exception as e:
                errors.append(f"Anthropic failed: {str(e)}")
        
        # All providers failed
        error_msg = "❌ No LLM provider available!\n"
        error_msg += "Tried: " + " → ".join(errors) + "\n"
        error_msg += "Please add at least one API key to .env:\n"
        error_msg += "  - OPENAI_API_KEY (recommended)\n"
        error_msg += "  - GOOGLE_API_KEY (free/cheap)\n"
        error_msg += "  - ANTHROPIC_API_KEY (alternative)\n"
        raise RuntimeError(error_msg)
    
    def __init__(self):
        """Initialize the agent with tools and LLM"""
        
        # Initialize LLM with fallback chain for resilience
        self.llm = self._initialize_llm_with_fallback()
        
        # Initialize tools
        self.tools = [
            PricingCalculatorTool(),
            DatabaseQueryTool(),
            WeatherDataTool(),
        ]
        
        # Create the ReAct agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=PRICING_AGENT_PROMPT
        )
        
        # Create agent executor with LangSmith tracing
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=VERBOSE,
            max_iterations=AGENT_MAX_ITERATIONS,
            handle_parsing_errors=True,
            return_intermediate_steps=True  # Important for LangSmith traces
        )
        
        print("✅ HoneyGo Pricing Agent initialized")
        print(f"   Model: {AGENT_MODEL}")
        print(f"   Tools: {len(self.tools)}")
        print(f"   LangSmith: {'Enabled' if LANGSMITH_TRACING else 'Disabled'}")
    
    def calculate_price(self, ride_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate optimal price for a ride request
        
        Args:
            ride_request: Dict with keys:
                - pickup_location: str
                - dropoff_location: str
                - distance: float (miles)
                - duration: int (minutes)
                - passenger_count: int
                - city: str
                - loyalty_tier: str (optional)
                - is_scheduled: bool
                - scheduled_time: str (optional)
        
        Returns:
            Dict with pricing decision and reasoning
        """
        
        # Build the agent input
        agent_input = f"""
        Calculate the optimal price for this ride:
        
        Pickup: {ride_request.get('pickup_location')}
        Dropoff: {ride_request.get('dropoff_location')}
        City: {ride_request.get('city')}
        Distance: {ride_request.get('distance')} miles
        Duration: {ride_request.get('duration')} minutes
        Passengers: {ride_request.get('passenger_count')}
        Loyalty Tier: {ride_request.get('loyalty_tier', 'new')}
        Scheduled: {ride_request.get('is_scheduled', False)}
        
        Steps to follow:
        1. Query historical data for similar rides in {ride_request.get('city')}
        2. Get weather conditions (current or forecast if scheduled)
        3. Calculate base price using the pricing calculator
        4. Provide final recommendation with detailed reasoning
        
        Focus on: fair pricing, driver earnings, market conditions, and transparency.
        """
        
        try:
            # Run the agent
            result = self.agent_executor.invoke({"input": agent_input})
            
            return {
                "success": True,
                "pricing_decision": result["output"],
                "reasoning_steps": result.get("intermediate_steps", []),
                "agent_trace": "View in LangSmith dashboard" if LANGSMITH_TRACING else "LangSmith disabled"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_trace": "Error occurred - check LangSmith for details"
            }


# Example usage
if __name__ == "__main__":
    # Test the agent
    agent = HoneyGoPricingAgent()
    
    test_ride = {
        "pickup_location": "Phoenix Sky Harbor Airport",
        "dropoff_location": "Arizona State University",
        "city": "Phoenix",
        "distance": 8.5,
        "duration": 18,
        "passenger_count": 1,
        "loyalty_tier": "gold",
        "is_scheduled": False
    }
    
    print("\n" + "="*60)
    print("Testing HoneyGo Pricing Agent")
    print("="*60 + "\n")
    
    result = agent.calculate_price(test_ride)
    
    print("\n" + "="*60)
    print("Result:")
    print("="*60)
    print(result)

