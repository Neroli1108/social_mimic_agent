# Social Mimic Agent System

A comprehensive simulation framework that leverages Large Language Models (LLMs) to create intelligent agents with diverse personalities for studying policy impacts and social dynamics in various scenarios.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Overview

The Social Mimic Agent System is a powerful research tool designed for social scientists, policy makers, and researchers to simulate and analyze human behavior under different policy scenarios. The system creates AI-driven agents with unique personalities that interact in customizable environments, providing insights into policy effectiveness and social dynamics.

### Key Capabilities

- **Multi-LLM Support**: OpenAI GPT, Google Gemini, and Hugging Face models
- **Dynamic Scenarios**: Predefined (workplace, town, school, neighborhood) and custom scenarios
- **Intelligent Agents**: Personality-driven agents with memory and adaptive behavior
- **Policy Analysis**: Comprehensive evaluation with customizable criteria
- **Real-time Monitoring**: Step-by-step or continuous simulation modes
- **Detailed Reporting**: Statistical analysis and strategic recommendations

## 🚀 Features

### 🤖 Intelligent Agent System

- **Personality-Driven Behavior**: Agents with unique traits and realistic responses
- **Memory Management**: Limited memory to simulate human cognitive constraints
- **Adaptive Stance**: Dynamic policy stance based on personality and scenario
- **Diverse Actions**: Non-repetitive, contextual actions throughout simulation

### 📊 Advanced Policy Evaluation

- **Customizable Criteria**: Default metrics plus user-defined evaluation rules
- **Support Analysis**: Detailed breakdown by personality types
- **Weighted Scoring**: Configurable importance for different criteria
- **Strategic Recommendations**: Actionable insights for policy implementation

### 🎭 Scenario Management

- **Predefined Scenarios**: Ready-to-use environments (workplace, community, education)
- **Custom Scenarios**: AI-enhanced scenario creation with intelligent suggestions
- **Context-Aware Personalities**: Scenario-appropriate agent personality generation
- **Dynamic Enhancement**: Automatic scenario and policy polishing

### 📈 Comprehensive Monitoring

- **Real-time Tracking**: Agent activities, interactions, and behavior patterns
- **Step-by-step Analysis**: Detailed insights at each simulation stage
- **Historical Data**: Complete logs for post-simulation analysis
- **Visual Reporting**: Progress bars, statistics, and formatted reports

## 🛠️ Installation

### Prerequisites

- **Python 3.7+**
- **API Key** for at least one LLM provider:
  - OpenAI API key
  - Google Gemini API key
  - Hugging Face API key (optional)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/social_mimic_agent_system.git
   cd social_mimic_agent_system
   ```

2. **Create virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys** (choose one method)

   **Method 1: Environment Variables**

   ```bash
   export OPENAI_API_KEY='your_openai_key_here'
   export GEMINI_API_KEY='your_gemini_key_here'
   export HUGGING_FACE_API_KEY='your_hf_key_here'
   ```

   **Method 2: Runtime Input**
   The system will prompt for API keys when needed.

5. **Run the simulation**
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### Basic Simulation

1. **Start the system**: `python main.py`
2. **Select LLM provider**: Choose from OpenAI, Gemini, or Hugging Face
3. **Configure policy**: Use predefined policies or create custom ones
4. **Set up scenario**: Select from predefined scenarios or create custom environments
5. **Configure agents**: Set number of agents and customize personalities
6. **Choose evaluation criteria**: Use defaults or create custom evaluation rules
7. **Run simulation**: Select step-by-step or continuous mode
8. **Analyze results**: Review detailed reports and recommendations

### Advanced Configuration

#### Custom Evaluation Criteria

```python
# The system supports custom evaluation criteria including:
- Agent sentiment analysis
- Behavioral change frequency
- Communication pattern analysis
- Custom keyword matching
- Manual scoring
```

#### Scenario Customization

```python
# Create custom scenarios with automatic enhancement:
- Detailed context analysis
- Personality suggestions
- Scenario polishing
- Implementation guidelines
```

#### Agent Personality Design

```python
# Design agents with specific traits:
- Personality-based policy stances
- Scenario-appropriate behaviors
- Dynamic interaction patterns
- Memory-influenced decisions
```

## 📁 Project Structure

```
social_mimic_agent_system/
├── agents/                 # Agent implementation and behavior logic
│   ├── __init__.py
│   └── agent.py           # Core agent class with LLM integration
├── policies/              # Policy management system
│   ├── __init__.py
│   └── policy.py          # Policy definition and updates
├── communication/         # Inter-agent communication system
│   ├── __init__.py
│   └── communication.py   # Broadcast and policy distribution
├── monitoring/            # Simulation monitoring and data collection
│   ├── __init__.py
│   └── monitor.py         # Real-time monitoring and reporting
├── logging_system/        # Activity logging and persistence
│   ├── __init__.py
│   └── logger.py          # Agent activity logging
├── utils/                 # Utility modules and helpers
│   ├── __init__.py
│   ├── llm_provider_selection.py      # Multi-LLM provider support
│   ├── scenario_generator.py          # Scenario creation and enhancement
│   ├── policy_evaluator.py            # Policy impact evaluation
│   └── evaluation_rules_manager.py    # Custom evaluation criteria
├── tests/                 # Unit tests for all components
├── logs/                  # Generated log files (created at runtime)
├── main.py               # Main simulation orchestrator
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration Options

### LLM Providers

- **OpenAI**: GPT-3.5/GPT-4 models for sophisticated reasoning
- **Google Gemini**: Gemini 1.5 Flash/Pro for fast and versatile performance
- **Hugging Face**: Custom models for specialized use cases

### Evaluation Criteria

- **Public Support Level** (25%): Community acceptance measurement
- **Implementation Feasibility** (20%): Practical implementation assessment
- **Economic Impact Perception** (20%): Economic effect evaluation
- **Social Cohesion** (20%): Community unity analysis
- **Adaptation Speed** (15%): Change adaptation rate

### Simulation Modes

- **Step-by-step**: Interactive mode with pause between steps
- **Continuous**: Automated execution with configurable timing
- **Hybrid**: Switch modes during simulation

## 📊 Example Use Cases

### 1. Workplace Policy Analysis

```python
# Analyze remote work policy impact
Policy: "Mandatory 3-day office attendance policy"
Scenario: Corporate workplace with diverse departments
Agents: 5 employees with varied personality types
Evaluation: Focus on productivity and satisfaction metrics
```

### 2. Community Policy Research

```python
# Study local government policy effects
Policy: "40% property tax increase for infrastructure"
Scenario: Small town community
Agents: 7 residents with different backgrounds
Evaluation: Economic impact and social cohesion focus
```

### 3. Educational Policy Testing

```python
# Evaluate new academic policies
Policy: "Mandatory digital device ban during classes"
Scenario: High school environment
Agents: 6 stakeholders (students, teachers, parents)
Evaluation: Custom criteria for academic performance
```

## 📈 Output and Analytics

### Simulation Reports

- **Overall Policy Effectiveness Score** (0-10 scale)
- **Support Analysis by Personality Type**
- **Individual Agent Behavioral Patterns**
- **Communication Network Analysis**
- **Strategic Implementation Recommendations**

### Generated Files

- **Agent Logs**: `logs/[agent_name].log` - Detailed activity records
- **Monitoring Data**: Real-time simulation state snapshots
- **Evaluation Reports**: Comprehensive policy impact analysis

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m unittest tests.test_agent
python -m unittest tests.test_policy
python -m unittest tests.test_communication
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow PEP 8** coding standards
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with detailed description

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run code formatting
black .

# Run linting
flake8 .

# Run tests
pytest
```

## ⚠️ Important Notes

### API Usage and Costs

- **Monitor API usage**: LLM providers charge per token/request
- **Rate limits**: Be aware of provider-specific rate limitations
- **Batch optimization**: Consider running multiple scenarios efficiently

### Research Ethics

- **Informed consent**: Ensure participants understand AI involvement in research
- **Data privacy**: Handle any real-world data integration responsibly
- **Bias awareness**: AI models may reflect training data biases

### Limitations

- **Simplified modeling**: AI agents don't capture full human complexity
- **Token limitations**: Long conversations may hit context limits
- **Model variations**: Different LLM providers may yield different results

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models and API access
- Google for Gemini AI capabilities
- Hugging Face for open-source model ecosystem
- Contributors and researchers using this tool for social good

---

**Built for researchers, by researchers.** This tool is designed to advance our understanding of social dynamics and policy impacts through ethical AI simulation.
