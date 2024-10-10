# Social Mimic Agent System

A simulation framework that uses Large Language Models (LLMs) to create agents with diverse personalities interacting under various policies. This system is designed for social research to study the impacts of new policies on individuals and their interactions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Logging and Monitoring](#logging-and-monitoring)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Social Mimic Agent System simulates real-life social interactions by:

- Creating agents with distinct personalities.
- Implementing policies that affect agent behavior.
- Enabling communication between agents and policymakers.
- Logging agent activities for analysis.
- Monitoring agent states and interactions.

This tool is valuable for researchers studying social dynamics, policy impacts, and human behavior modeling.

### LLM Providers

The system allows users to select between multiple LLM providers, including:

- **OpenAI** (e.g., GPT-4)
- **Hugging Face** (Custom models)
- **Google Gemini** (e.g., Gemini 1.5 Flash)

Users can choose the LLM provider and model before running the simulation.

## Features

- **Agent Simulation**: Agents have unique personalities and limited memory to mimic human cognition.
- **Policy Integration**: Policies can be introduced to observe their effects on agents.
- **Communication System**: Agents can interact with each other and policymakers.
- **LLM Integration**: Supports OpenAI, Hugging Face, and Google Gemini models.
- **Logging System**: Records all agent activities for detailed analysis.
- **Monitoring System**: Collects data from agents to provide insights into the simulation.

## Project Structure

```
social_mimic_agent_system/
├── agents/
│   ├── __init__.py
│   └── agent.py
├── policies/
│   ├── __init__.py
│   └── policy.py
├── communication/
│   ├── __init__.py
│   └── communication.py
├── logging_system/
│   ├── __init__.py
│   └── logger.py
├── monitoring/
│   ├── __init__.py
│   └── monitor.py
├── utils/
│   ├── __init__.py
│   └── llm_provider_selection.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- API keys for OpenAI, Hugging Face, or Google Gemini.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/social_mimic_agent_system.git
   cd social_mimic_agent_system
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Keys**

   Replace `'YOUR_API_KEY'` in `agents/agent.py` with your actual API keys for the LLM provider (OpenAI, Hugging Face, or Gemini), or set the environment variables:

   ```bash
   export OPENAI_API_KEY='your_openai_key'
   export HUGGING_FACE_API_KEY='your_hugging_face_key'
   export GEMINI_API_KEY='your_gemini_key'
   ```

## Usage

Run the main simulation script:

```bash
python main.py
```

This will start the simulation and prompt you to select an LLM provider and model.

## Configuration

### Adding Agents

To add more agents, modify the `main.py` file:

```python
from agents.agent import Agent

# Initialize agents
agent1 = Agent(name="Alice", personality_traits="optimistic and outgoing")
agent2 = Agent(name="Bob", personality_traits="pessimistic and introverted")
agent3 = Agent(name="Charlie", personality_traits="analytical and curious")  # New agent
agents = [agent1, agent2, agent3]
```

### Updating Policies

Modify the `Policy` instance in `main.py`:

```python
from policies.policy import Policy

# Initialize policy
policy = Policy("A new environmental regulation is implemented.")
```

### Adjusting Memory Limit

Set the `memory_limit` parameter when creating an agent:

```python
agent = Agent(name="Dana", personality_traits="ambitious", memory_limit=10)
```

## Examples

### Basic Simulation

The default simulation includes two agents, Alice and Bob, interacting under a new work-from-home policy.

### Custom Simulation

1. **Define Agents with Unique Personalities**

   ```python
   agent1 = Agent(name="Eve", personality_traits="friendly and talkative")
   agent2 = Agent(name="Frank", personality_traits="reserved and thoughtful")
   ```

2. **Introduce a New Policy**

   ```python
   policy = Policy("A mandatory digital detox weekend is announced.")
   ```

3. **Run Simulation Steps**

   Adjust the number of simulation steps in `main.py`:

   ```python
   for _ in range 10:  # Increase steps from 5 to 10
       # Simulation code...
   ```

## Logging and Monitoring

### Logs

Agent activities are logged in the `logs/` directory. Each agent has a separate log file:

- `logs/Alice.log`
- `logs/Bob.log`

### Monitoring Data

The monitoring system collects data at each simulation step and prints a summary report at the end. Modify the `Monitor` class in `monitoring/monitor.py` to customize data collection and reporting.

## Limitations

- **Simplified Model**: This is a basic simulation and may not capture all complexities of human behavior.
- **API Usage**: Be mindful of OpenAI, Hugging Face, and Gemini API call limits and costs.
- **Error Handling**: Limited exception handling is implemented; enhancements may be necessary for robustness.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your_feature`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/your_feature`.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note**: This project is intended for educational and research purposes. Ensure compliance with OpenAI, Hugging Face, and Gemini's usage policies when using their APIs.
