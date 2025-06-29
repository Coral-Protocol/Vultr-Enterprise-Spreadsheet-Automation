# Coral Raise Your Hack Guide

## About Raise Your Hack 💻
This is your chance to push boundaries, solve real-world challenges, and create impact at the official hackathon of the [RAISE Summit 2025](https://www.raisesummit.com/) at one of Paris's most iconic venues: Le Carrousel du Louvre. RAISE Summit 2025 is a premier event convening the brightest minds across industries to accelerate innovation and drive the future of entrepreneurship, AI, and technology.

## About Coral Protocol 🪸

The [Coral Protocol](https://www.coralprotocol.org/) is an initiative to create an open, standardized infrastructure for AI agent coordination. It builds on the MCP framework to enable multiple AI agents to work together collaboratively, addressing the limitation of isolated AI systems that lack mechanisms for interconnected workflows. The Coral Protocol focuses on:

- Agent Collaboration: Allowing AI agents to communicate, share tasks, and coordinate in a structured way.

- Messaging Layer: Providing a system for agents to exchange messages, similar to human messaging platforms, with features like threads and mentions.

- Scalability and Openness: Designing an extensible, open-source solution that can support a wide range of AI applications, from customer support to project management.

We released the [Coral Server](https://github.com/Coral-Protocol/coral-server) as an open-source MCP server to serve as the backbone for this vision. The server acts as a messaging hub where AI agents can register, communicate via threads, and coordinate tasks by mentioning each other. The protocol aims to foster a community-driven ecosystem, encouraging developers to experiment, contribute, and build collaborative AI systems.

## About the Tracks 🎯

Coral Protocol is encouraged for teams interested in multi-agent systems, allowing them to integrate open-source agents from any framework. With its thread-based agent architecture, Coral enables scalable and predictable multi-agent interactions, making it a powerful tool for innovative applications. Checkout how to build on the below track using Coral Protocol.

### Vultr Track

🧠 Agentic Workflows for the Future of Work

<details>

Build a Web-Based Enterprise Agent Deployed on Vultr

In this track, you'll design and develop a web-based AI agent purpose-built to support enterprise teams—from marketing to sales, operations, and beyond. Your mission: create a smart, agentic tool that simplifies, accelerates, or transforms workflows for today’s (and tomorrow’s) knowledge workers. The core app should be deployed on Vultr infrastructure and optimized for real-world business use cases.

🔍 What We’re Looking For:
• Enterprise-Ready: Your agent should address pain points or opportunities within marketing, sales, customer success, HR, or other enterprise functions.

• Agentic & Autonomous: Move beyond simple prompts. Build workflows where the agent can reason, plan, and act with minimal human input. Think multi-step tasks, decision trees, and feedback loops.

• Future-of-Work Focused: Help teams save time, make smarter decisions, or enhance collaboration—through the lens of what future employee experience could look like.

• Web-Based & Deployed on Vultr: The app must be a deployable web app running on Vultr. You can use any stack, language, or framework, but it should be cloud-hosted and publicly accessible (Vultr credits will be provided).

• Scalable Tooling: We encourage—but don’t require—use of technologies like vector databases, model context protocol (MCP), or other modular, scalable AI components.

🛠️ Tech Flexibility:
• Use any programming language or framework.
• Use open-source LLMs, retrieval-augmented generation. (Also available via Vultr Serverless Inference)

📦 Developer Expectations:
• Include a GitHub repo with setup instructions, agent capabilities, and a sample use case demo.
• Deploy on Vultr (we’ll provide credits and assistance).
• Show how your app solves a real problem in an enterprise context.

Each team leader of the Vultr Track will receive a coupon code to claim $250 in free credits on Vultr by signing up as a regular customer.

</details>

### Vultr Track: How to setup Coral on Vultr


#### 1. Set up Vultr

<details>

- Sign up on Vultr and know more by looking into the [product documentation](https://docs.vultr.com/products)

- Choose and host an instance as per your system requirements

![Vultr Instance](images/vultr-instance.png)

- SSH into the instance (check IP) and enter the password of your instance

```bash
ssh root@95.179.233.169
```

</details>

#### 2. Setup the Agents


<details>

- In this example, we are using the agent:[Coral Interface Agent](https://github.com/Coral-Protocol/Coral-Interface-Agent) and [Coral Pandas Agent](https://github.com/Coral-Protocol/Coral-Pandas-Agent). Please click and link and set up the agents by following the setup instructions in the repository.

</details>

#### 3. Run the Agents

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be seaprately running on each terminal without UI support.  

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
  interface:
    options:
      - name: "API_KEY"
        type: "string"
        description: "API key for the service"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/Coral-Interface-Agent/run_agent.sh main.py"]
      environment:
        - name: "API_KEY"
          from: "API_KEY"
        - name: "MODEL_NAME"
          value: "gpt-4.1"
        - name: "MODEL_PROVIDER"
          value: "openai"
        - name: "MODEL_TOKEN"
          value: "16000"
        - name: "MODEL_TEMPERATURE"
          value: "0.3"
          
  pandas:
    options:
      - name: "API_KEY"
        type: "string"
        description: "API key for the service"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/Coral-Pandas-Agent/run_agent.sh main.py"]
      environment:
        - name: "API_KEY"
          from: "API_KEY"
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

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below commands in separate terminals.

<details>

Run the Interface Agent

```bash
# cd to directory
cd Coral-Interface-Agent

# Run the agent using `uv`:
uv run python main.py
```

Run the Pandas Agent

```bash
# cd to directory
cd Coral-Pandas-Agent

# Run the agent using `uv`:
uv run python main.py
```

</details>

(NOTE: The examples above are just to demonstrate how to use Coral. For the hackathon you have to create you own use case by either selecting from the list of agents from our [awesome agent list](https://github.com/Coral-Protocol/awesome-agents-for-multi-agent-systems) or create your own agents compatible on Coral.)

