import urllib.parse
from dotenv import load_dotenv
import os
import asyncio
import logging
import traceback
import json
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerSSE, MCPServerStdio
import logfire

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

# Get environment variables
base_url = os.getenv("CORAL_SSE_URL")
agentID = os.getenv("CORAL_AGENT_ID")

logfire.configure()  
logfire.instrument_pydantic_ai() 

coral_params = {
    "agentId": agentID,
    "agentDescription": "ACI Dev agent capable of searching for relevant functions based on user intent and executing those functions with the required parameters."
}

query_string = urllib.parse.urlencode(coral_params)

async def get_mcp_tools(server):
    """Get tools from an MCP server."""
    try:
        async with server:
            tools_result = await server.list_tools()
            return tools_result.tools if hasattr(tools_result, 'tools') else []
    except Exception as e:
        logger.warning(f"Could not get tools from MCP server: {str(e)}")
        return []

async def main():
    try:
        # Setup MCP servers
        CORAL_SERVER_URL = f"{base_url}?{query_string}"
        logger.info(f"Connecting to Coral Server: {CORAL_SERVER_URL}")
        
        # Initialize Coral MCP server (SSE)
        coral_server = MCPServerSSE(
            url=CORAL_SERVER_URL,
            sse_read_timeout=600,
            timeout=600,
        )
        
        # Initialize ACI MCP server (stdio)
        aci_server = MCPServerStdio(
            command='uvx',
            args=[
                'aci-mcp', 
                'unified-server', 
                '--linked-account-owner-id', os.getenv("ACI_OWNER_ID"), 
                '--port', '8000', 
                '--allowed-apps-only'
            ],
            env={"ACI_API_KEY": os.getenv("ACI_API_KEY")},
            timeout=600,
        )
        
        # Get tools from MCP servers before creating agent
        logger.info("Getting tools from MCP servers...")
        coral_tools = await get_mcp_tools(coral_server)
        aci_tools = await get_mcp_tools(aci_server)
        
        
        
        # Create system prompt with tool descriptions
        system_prompt = """You are ACIDev agent interacting with tools from Coral Server and ACI MCP Server. Your task is to perform any instructions coming from other agents.

Follow these steps in order:
1. Call wait_for_mentions (timeoutMs: 30000) to receive mentions from other agents.
2. When you receive a mention, keep the thread ID and the sender ID.
3. Take 2 seconds to think about the content (instruction) of the message and check only from the list of your tools available for you to action.
4. Check the tool schema and make a plan in steps for the task you want to perform.
5. Use ACI_SEARCH_FUNCTIONS to search for the function you need to call.
6. Use ACI_EXECUTE_FUNCTION to call the function you need to call.
7. Take 3 seconds and think about the content and see if you have executed the instruction to the best of your ability and the tools. Make this your response as "answer".
8. Use send_message tool to send a message in the same thread ID to the sender ID you received the mention from, with content: "answer".
9. If any error occurs, use send_message to send a message in the same thread ID to the sender ID you received the mention from, with content: "error".
10. Always respond back to the sender agent even if you have no answer or error.

Available ACI Tools and Schemas:

1. ACI_SEARCH_FUNCTIONS
Description: This function allows you to find relevant executable functions and their schemas that can help complete your tasks.
Schema: {
    "intent": {
        "type": "string",
        "description": "Use this to find relevant functions you might need. Returned results of this function will be sorted by relevance to the intent."
    }
}

2. ACI_EXECUTE_FUNCTION
Description: Execute a specific retrieved function. Provide the executable function name, and the required function parameters for that function.
Schema: {
    "function_name": {
        "type": "string",
        "description": "The name of the function to execute"
    },
    "function_arguments": {
        "type": "object",
        "description": "A dictionary containing key-value pairs of input parameters required by the specified function. The parameter names and types must match those defined in the function definition previously retrieved. If the function requires no parameters, provide an empty object.",
        "additionalProperties": true
    }
}

You have access to coral tools for communication and aci tools for ACI operations."""
        
        # Initialize agent with complete system prompt including tool descriptions
        agent = Agent(
            model=f"{os.getenv('MODEL_PROVIDER', 'openai')}:{os.getenv('MODEL_NAME', 'gpt-4o-mini')}",
            system_prompt=system_prompt,
            mcp_servers=[coral_server, aci_server]
        )

        logger.info("Multi Server Connection Established")
        
        # Initialize message history
        message_history = []

        # Run the agent with MCP servers
        async with agent.run_mcp_servers():
            logger.info("=== CONNECTION ESTABLISHED ===")
            
            while True:
                try:
                    logger.info("Starting new agent invocation")
                    
                    # Run the agent to wait for mentions and process them
                    result = await agent.run(
                        "Call wait for mentions to wait for instructions from other agents",
                        message_history=message_history
                    )
                    
                    logger.info(f"Agent result: {result.output}")
                    
                    # Update message history with new messages
                    message_history.extend(result.new_messages())
                    
                    # Log the current message history size
                    logger.debug(f"Current message history size: {len(message_history)}")
                    
                    logger.info("Completed agent invocation, restarting loop")
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error in agent loop: {str(e)}")
                    logger.error(traceback.format_exc())
                    await asyncio.sleep(5)

    except Exception as e:
        logger.error(f"Error in main setup: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(main())
