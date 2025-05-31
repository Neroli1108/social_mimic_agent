import random
import re

class ScenarioGenerator:
    def __init__(self):
        self.predefined_scenarios = {
            "workplace": {
                "description": "A corporate office environment with employees from different departments",
                "context": "Professional setting with hierarchies, deadlines, and team collaboration",
                "sample_personalities": [
                    "ambitious and competitive",
                    "collaborative and supportive", 
                    "detail-oriented and methodical",
                    "creative and innovative",
                    "experienced and mentor-like",
                    "analytical and data-driven"
                ]
            },
            "town": {
                "description": "A small town community with diverse residents",
                "context": "Community setting with local businesses, families, and civic activities",
                "sample_personalities": [
                    "friendly and community-minded",
                    "traditional and conservative",
                    "progressive and change-oriented",
                    "quiet and observant",
                    "outgoing and social",
                    "practical and down-to-earth"
                ]
            },
            "school": {
                "description": "An educational institution with students, teachers, and staff",
                "context": "Academic environment focused on learning, growth, and development",
                "sample_personalities": [
                    "studious and goal-oriented",
                    "creative and artistic",
                    "athletic and competitive",
                    "social and popular",
                    "introverted and bookish",
                    "rebellious and questioning"
                ]
            },
            "neighborhood": {
                "description": "A residential area with families and individuals of various backgrounds",
                "context": "Community living with shared spaces, local concerns, and neighborly interactions",
                "sample_personalities": [
                    "helpful and neighborly",
                    "privacy-focused and reserved",
                    "active and community-involved",
                    "elderly and wise",
                    "young and energetic",
                    "busy and career-focused"
                ]
            }
        }

    def polish_custom_scenario(self, raw_scenario):
        """Polish and enhance a user's custom scenario input"""
        # Clean and enhance the scenario description
        polished = self._clean_text(raw_scenario)
        
        # Add context and structure
        enhanced_scenario = self._enhance_scenario_description(polished)
        
        # Suggest improvements
        suggestions = self._generate_scenario_suggestions(polished)
        
        return {
            "original": raw_scenario,
            "polished": enhanced_scenario,
            "suggestions": suggestions
        }

    def polish_custom_policy(self, raw_policy):
        """Polish and enhance a user's custom policy input"""
        polished = self._clean_text(raw_policy)
        
        # Enhance policy language
        enhanced_policy = self._enhance_policy_language(polished)
        
        # Generate policy analysis
        analysis = self._analyze_policy_type(enhanced_policy)
        
        return {
            "original": raw_policy,
            "polished": enhanced_policy,
            "analysis": analysis,
            "suggestions": self._generate_policy_suggestions(enhanced_policy)
        }

    def _clean_text(self, text):
        """Clean and normalize text input"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Ensure proper capitalization
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        # Ensure proper ending punctuation
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text

    def _enhance_scenario_description(self, scenario):
        """Enhance scenario description with more context"""
        scenario_lower = scenario.lower()
        
        # Add contextual enhancements based on keywords
        enhancements = []
        
        if any(word in scenario_lower for word in ['hospital', 'clinic', 'medical']):
            enhancements.append("involving healthcare professionals, patients, and administrative staff")
        elif any(word in scenario_lower for word in ['restaurant', 'cafe', 'food']):
            enhancements.append("including staff, customers, and management with diverse dining preferences")
        elif any(word in scenario_lower for word in ['factory', 'manufacturing', 'production']):
            enhancements.append("with workers, supervisors, and quality control personnel")
        elif any(word in scenario_lower for word in ['retail', 'store', 'shop']):
            enhancements.append("featuring employees, customers, and managers with varied shopping experiences")
        elif any(word in scenario_lower for word in ['government', 'city hall', 'municipal']):
            enhancements.append("including civil servants, elected officials, and citizens")
        
        if enhancements:
            enhanced = f"{scenario} This environment includes {enhancements[0]}."
        else:
            enhanced = f"{scenario} This setting involves people with diverse backgrounds, roles, and perspectives."
        
        return enhanced

    def _enhance_policy_language(self, policy):
        """Enhance policy language for clarity and impact"""
        policy_lower = policy.lower()
        
        # Add specificity based on policy type
        if "tariff" in policy_lower and "%" not in policy_lower:
            # If tariff mentioned but no percentage, suggest adding specifics
            if "increase" in policy_lower:
                enhanced = policy.replace(".", " by 25%.")
            else:
                enhanced = policy
        elif "work from home" in policy_lower or "remote work" in policy_lower:
            if "policy" not in policy_lower:
                enhanced = policy.replace(".", " policy.")
            else:
                enhanced = policy
        elif "tax" in policy_lower and "%" not in policy_lower:
            enhanced = policy.replace(".", " of 5%.")
        else:
            enhanced = policy
        
        # Ensure formal policy language
        if not any(word in enhanced.lower() for word in ['policy', 'regulation', 'law', 'mandate', 'initiative']):
            enhanced = enhanced.replace(".", " policy.")
        
        return enhanced

    def _analyze_policy_type(self, policy):
        """Analyze the type and characteristics of a policy"""
        policy_lower = policy.lower()
        
        analysis = {
            "type": "General Policy",
            "scope": "Local",
            "impact_areas": [],
            "stakeholders": [],
            "complexity": "Medium"
        }
        
        # Determine policy type
        if "tariff" in policy_lower:
            analysis["type"] = "Trade/Economic Policy"
            analysis["scope"] = "National/International"
            analysis["impact_areas"] = ["Economy", "Consumer Prices", "Local Business"]
            analysis["stakeholders"] = ["Consumers", "Local Businesses", "Importers", "Government"]
            analysis["complexity"] = "High"
        elif any(word in policy_lower for word in ["work from home", "remote work"]):
            analysis["type"] = "Workplace Policy"
            analysis["scope"] = "Organizational"
            analysis["impact_areas"] = ["Work-Life Balance", "Productivity", "Office Operations"]
            analysis["stakeholders"] = ["Employees", "Managers", "HR", "Facilities"]
            analysis["complexity"] = "Medium"
        elif "tax" in policy_lower:
            analysis["type"] = "Fiscal Policy"
            analysis["scope"] = "Local/Regional"
            analysis["impact_areas"] = ["Public Revenue", "Individual Finances", "Public Services"]
            analysis["stakeholders"] = ["Taxpayers", "Government", "Public Service Users"]
            analysis["complexity"] = "High"
        elif any(word in policy_lower for word in ["environment", "recycling", "sustainability"]):
            analysis["type"] = "Environmental Policy"
            analysis["scope"] = "Community"
            analysis["impact_areas"] = ["Environment", "Lifestyle Changes", "Costs"]
            analysis["stakeholders"] = ["Residents", "Businesses", "Environmental Groups"]
            analysis["complexity"] = "Medium"
        
        return analysis

    def _generate_scenario_suggestions(self, scenario):
        """Generate suggestions for improving the scenario"""
        suggestions = []
        scenario_lower = scenario.lower()
        
        if len(scenario) < 50:
            suggestions.append("Consider adding more details about the setting and context")
        
        if not any(word in scenario_lower for word in ['people', 'person', 'individual', 'resident', 'employee', 'student']):
            suggestions.append("Specify what types of people are involved in this scenario")
        
        if not any(word in scenario_lower for word in ['interact', 'work', 'live', 'study', 'meet']):
            suggestions.append("Describe how people interact or what they do in this environment")
        
        suggestions.append("Consider the diversity of roles, ages, and backgrounds in this scenario")
        
        return suggestions

    def _generate_policy_suggestions(self, policy):
        """Generate suggestions for improving the policy"""
        suggestions = []
        policy_lower = policy.lower()
        
        if not any(word in policy_lower for word in ['effective', 'implement', 'start', 'begin']):
            suggestions.append("Consider adding when this policy takes effect")
        
        if "%" not in policy and any(word in policy_lower for word in ['increase', 'decrease', 'change']):
            suggestions.append("Consider specifying the percentage or amount of change")
        
        if not any(word in policy_lower for word in ['all', 'every', 'citizen', 'employee', 'resident']):
            suggestions.append("Clarify who this policy affects")
        
        suggestions.append("Consider the short-term and long-term implications of this policy")
        
        return suggestions

    def get_scenario_options(self):
        return list(self.predefined_scenarios.keys())

    def get_scenario_info(self, scenario):
        return self.predefined_scenarios.get(scenario, None)

    def analyze_custom_scenario(self, scenario_description):
        """Analyze a custom scenario and suggest appropriate personalities"""
        scenario_lower = scenario_description.lower()
        
        # Enhanced keyword-based analysis with more sophisticated matching
        suggested_personalities = []
        
        # Business/workplace keywords
        if any(word in scenario_lower for word in ['office', 'company', 'business', 'corporate', 'work', 'employee', 'manager']):
            suggested_personalities.extend([
                "ambitious and results-driven",
                "collaborative and team-oriented",
                "analytical and detail-focused",
                "creative and innovative",
                "cautious and procedure-oriented",
                "leadership-focused and decisive"
            ])
        
        # Community/social keywords  
        if any(word in scenario_lower for word in ['community', 'neighborhood', 'town', 'village', 'residents', 'citizens']):
            suggested_personalities.extend([
                "community-minded and helpful",
                "traditional and conservative",
                "progressive and open-minded",
                "quiet and observant",
                "social and outgoing",
                "practical and resourceful"
            ])
        
        # Educational keywords
        if any(word in scenario_lower for word in ['school', 'university', 'student', 'teacher', 'education', 'learning']):
            suggested_personalities.extend([
                "studious and dedicated",
                "curious and questioning",
                "social and outgoing",
                "focused and disciplined",
                "creative and expressive",
                "analytical and logical"
            ])
        
        # Healthcare keywords
        if any(word in scenario_lower for word in ['hospital', 'clinic', 'medical', 'doctor', 'nurse', 'patient']):
            suggested_personalities.extend([
                "caring and empathetic",
                "professional and efficient",
                "calm under pressure",
                "detail-oriented and precise",
                "compassionate and patient",
                "organized and systematic"
            ])
        
        # Technology keywords
        if any(word in scenario_lower for word in ['tech', 'software', 'digital', 'innovation', 'startup']):
            suggested_personalities.extend([
                "innovative and tech-savvy",
                "logical and problem-solving",
                "adaptable and flexible",
                "ambitious and driven",
                "creative and experimental",
                "analytical and systematic"
            ])
        
        # Service industry keywords
        if any(word in scenario_lower for word in ['restaurant', 'retail', 'customer', 'service', 'hospitality']):
            suggested_personalities.extend([
                "friendly and customer-focused",
                "energetic and fast-paced",
                "patient and service-oriented",
                "detail-oriented and organized",
                "stress-tolerant and adaptable",
                "team-oriented and collaborative"
            ])
        
        # Government/civic keywords
        if any(word in scenario_lower for word in ['government', 'civic', 'public', 'municipal', 'policy']):
            suggested_personalities.extend([
                "public-service oriented",
                "diplomatic and measured",
                "detail-oriented and systematic",
                "ethical and principled",
                "communicative and transparent",
                "balanced and fair-minded"
            ])
        
        # If no specific keywords found, provide balanced general personalities
        if not suggested_personalities:
            suggested_personalities = [
                "optimistic and outgoing",
                "cautious and analytical",
                "creative and expressive",
                "practical and realistic",
                "empathetic and caring",
                "confident and assertive",
                "collaborative and supportive",
                "independent and self-reliant"
            ]
        
        # Remove duplicates and return up to 10 suggestions
        unique_personalities = list(dict.fromkeys(suggested_personalities))  # Preserves order
        return unique_personalities[:10]

    def generate_agent_names(self, count, scenario_type="general"):
        """Generate appropriate names based on scenario"""
        name_pools = {
            "workplace": ["Alex", "Jordan", "Morgan", "Casey", "Taylor", "Riley", "Avery", "Quinn", "Blake", "Sage"],
            "town": ["Emma", "Liam", "Grace", "Noah", "Sophia", "Mason", "Isabella", "Lucas", "Ava", "Oliver"],
            "school": ["Zoe", "Ethan", "Maya", "Caleb", "Luna", "Tyler", "Aria", "Connor", "Ivy", "Dylan"],
            "neighborhood": ["Sarah", "Michael", "Rachel", "David", "Lisa", "James", "Maria", "Robert", "Anna", "John"],
            "custom": ["Sam", "Chris", "Pat", "Jamie", "Drew", "Casey", "Robin", "Skyler", "Reese", "Cameron"]
        }
        
        names = name_pools.get(scenario_type, name_pools["custom"])
        return random.sample(names, min(count, len(names)))