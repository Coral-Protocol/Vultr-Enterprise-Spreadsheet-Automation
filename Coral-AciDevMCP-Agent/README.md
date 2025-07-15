## [ACI DEV MCP Agent](https://github.com/Coral-Protocol/Coral-AciDevMCP-Agent)

ACI Dev agent capable of searching for relevant functions based on user intent and executing those functions with the required parameters.  

Link- [https://www.aci.dev/](https://www.aci.dev/)


## Responsibility
ACI.dev is the open-source infrastructure layer for AI-agent tool-use and VibeOps. It gives AI agents intent-aware access to 600+ tools with multi-tenant auth, granular permissions, and dynamic tool discovery—exposed as either direct function calls or through a Unified Model-Context-Protocol (MCP) server.

## Details
- **Framework**: Pydantic-AI
- **Tools used**: ACI Dev MCP Server Tools, Coral Server Tools
- **AI model**: OpenAI GPT-4o
- **Date added**: June 4, 2025
- **Reference**: [ACI DEV Repo](https://github.com/aipotheosis-labs/aci)
- **License**: MIT
- **Demo Video**: [Link](https://getrapidemo.com/videos/ad451996-4be1-4568-af3f-4dae227fb2c9)

## Setup the Agent

### 1. Clone & Install Dependencies

<details>

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system. If you are trying to run the ACI Dev agent and require an input, you can either create your agent which communicates on the coral server or run and register the [Interface Agent](https://github.com/Coral-Protocol/Coral-Interface-Agent) on the Coral Server.

```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Coral-AciDevMCP-Agent

# Navigate to the project directory:
cd Coral-AciDevMCP-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Configure Environment Variables

<details>

Get the API Key:
[OpenAI](https://platform.openai.com/api-keys) || 
[Github Token](https://github.com/settings/tokens)

```bash
# Create .env file in project root
cp -r .env_sample .env
```

Check if the .env file has correct URL for Coral Server and adjust the parameters accordingly.

</details>

### 3. Configure Logfire for Monitoring

<details>

This agent uses [Logfire](https://ai.pydantic.dev/logfire/#pydantic-logfire) for monitoring tool usage and agent behavior. Logfire provides detailed insights into how your agent interacts with tools and handles requests.

1. **Setup Logfire**
   ```python
   # These lines are already included in main.py
   import logfire
   
   logfire.configure()  
   logfire.instrument_pydantic_ai()
   ```

For more details about Logfire configuration and features, visit: [Pydantic-AI Logfire Documentation](https://ai.pydantic.dev/logfire/#pydantic-logfire)

</details>

### 4. Configure MCP with Required Apps

<details>

1. Go to the **"App Store"** on your ACI.dev Dashboard.  


2. **Search for "Gmail"** using the search bar, then click on the Gmail app from the results.  
<img width="1887" height="883" alt="Image" src="https://github.com/user-attachments/assets/687883b1-f5a6-45db-8cc9-4167916de69b" />

3. **Click "Configure App"** to begin setup.  
<img width="1886" height="879" alt="Image" src="https://github.com/user-attachments/assets/b3a477b8-0724-463b-b6fa-5eff0b787bc9" />

4. **Enable the toggle** for *"Use ACI.dev's OAuth2 App"* and confirm your choice.  
<img width="1237" height="600" alt="Image" src="https://github.com/user-attachments/assets/3151fb6f-dd84-49d4-9de0-b797a6a224ee" />

5. **Choose your agent** by selecting the *"Default Agent"* or any other preferred agent.  
<img width="1231" height="504" alt="Image" src="https://github.com/user-attachments/assets/f6e1459d-4b52-4c5e-be7d-5d0759a8b416" />

6. **Enter an Account Owner ID** of your choice, then click **"Start OAuth2 Flow"**.  
<img width="1231" height="423" alt="Image" src="https://github.com/user-attachments/assets/f293cdac-bcdc-405f-b1b9-06dea7dea12f" />

7. **Select the Gmail account** you wish to connect.  
<img width="1397" height="473" alt="Image" src="https://github.com/user-attachments/assets/3b4c7f3b-84fe-4847-af12-cd55117175ec" />

8. **Grant permission** to ACI.dev by checking the required box, then click **"Continue"** to complete the configuration.
<img width="1382" height="877" alt="Image" src="https://github.com/user-attachments/assets/3e4f3f80-8e7c-4d2d-8e58-855d215726bb" />

</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be seperately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
# PROJECT_DIR="/PATH/TO/YOUR/PROJECT"

applications:
  - id: "app"
    name: "Default Application"
    description: "Default application for testing"
    privacyKeys:
      - "default-key"
      - "public"
      - "priv"

registry:
  Aacidevmcp_agent:
    options:
      - name: "OPENAI_API_KEY"
        type: "string"
        description: "API key for the service"
      - name: "ACI_OWNER_ID"
        type: "string"
        description: "ACI OWNER ID for the service"
      - name: "ACI_API_KEY"
        type: "string"
        description: "ACI API KEY for the service"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/run_agent.sh main.py"]
      environment:
        - name: "OPENAI_API_KEY"
          from: "OPENAI_API_KEY"
        - name: "ACI_OWNER_ID"
          from: "ACI_OWNER_ID"
        - name: "ACI_API_KEY"
          from: "ACI_API_KEY"
        - name: "MODEL_NAME"
          value: "gpt-4.1"
        - name: "MODEL_PROVIDER"
          value: "openai"
        - name: "MODEL_TOKEN"
          value: "16000"
        - name: "MODEL_TEMPERATURE"
          value: "0.3"

```

For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run python main.py
```

You can view the agents running in Dev Mode using the [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio) by running it separately in a new terminal.

</details>


## Example

<details>

```bash
# Input:
can you ask aci dev to check my github- sd2879 and return me recent repository i made

#Output:
The GitHub repositories created by the user sd2879 are:

1. ai-taxi-stand - https://github.com/sd2879/ai-taxi-stand
2. archscan-mistral-ai - https://github.com/sd2879/archscan-mistral-ai
3. cad_pdf_extractror - https://github.com/sd2879/cad_pdf_extractror
4. docker-image-CI-CD - https://github.com/sd2879/docker-image-CI-CD
5. llama_scoutie_ai - https://github.com/sd2879/llama_scoutie_ai
6. mangalX - https://github.com/sd2879/mangalX
7. quant_track_crypto - https://github.com/sd2879/quant_track_crypto
8. rag_pipeline - https://github.com/sd2879/rag_pipeline
9. rooftop_solar_potential - https://github.com/sd2879/rooftop_solar_potential
10. rooftop_solar_potential_using_detectron2 - https://github.com/sd2879/rooftop_solar_potential_using_detectron2
11. sd2879 - https://github.com/sd2879/sd2879
12. test-repo - https://github.com/sd2879/test-repo

```

</details>

### Creator Details
- **Name**: Suman Deb
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)
