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

## Features

- **Agent Simulation**: Agents have unique personalities and limited memory to mimic human cognition.
- **Policy Integration**: Policies can be introduced to observe their effects on agents.
- **Communication System**: Agents can interact with each other and policymakers.
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
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key (for LLM capabilities)

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

4. **Set Up OpenAI API Key**

   Replace `'YOUR_API_KEY'` in `agents/agent.py` with your actual OpenAI API key:

   ```python
   openai.api_key = 'YOUR_API_KEY'
   ```

   Alternatively, you can set the `OPENAI_API_KEY` environment variable:

   ```bash
   export OPENAI_API_KEY='your_api_key'  # On Windows use `set`
   ```

## Usage

Run the main simulation script:

```bash
python main.py
```

This will start the simulation with predefined agents and policies.

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
   for _ in range(10):  # Increase steps from 5 to 10
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
- **API Usage**: Be mindful of OpenAI API call limits and costs.
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

**Note**: This project is intended for educational and research purposes. Ensure compliance with OpenAI's usage policies when using the OpenAI API.
