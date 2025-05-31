from .evaluation_rules_manager import EvaluationRulesManager

class PolicyEvaluator:
    def __init__(self):
        self.rules_manager = EvaluationRulesManager()
        self.evaluation_criteria = []

    def configure_evaluation_rules(self):
        """Configure evaluation rules with user input"""
        print(f"\n📊 POLICY EVALUATION SETUP")
        print("="*50)
        
        # Display default rules first
        self.rules_manager.display_default_rules()
        
        # Get user preferences
        self.active_criteria = self.rules_manager.get_evaluation_preferences()
        self.evaluation_criteria = list(self.active_criteria.keys())
        
        print(f"\n✅ Evaluation configuration complete!")
        return self.active_criteria

    def evaluate_policy_impact(self, agents, monitor_data, policy_text):
        """Evaluate the impact of the policy on agents using configured rules"""
        evaluation = {
            "policy_text": policy_text,
            "evaluation_criteria": self.active_criteria,
            "overall_score": 0,
            "criteria_scores": {},
            "agent_analysis": {},
            "support_analysis": {},
            "recommendations": []
        }
        
        # Analyze each agent's response
        for agent in agents:
            agent_analysis = self._analyze_agent_response(agent, monitor_data)
            evaluation["agent_analysis"][agent.name] = agent_analysis
        
        # Analyze support patterns
        evaluation["support_analysis"] = self._analyze_support_patterns(agents, policy_text)
        
        # Calculate scores using configured criteria
        evaluation["criteria_scores"] = self._calculate_criteria_scores_with_rules(
            agents, monitor_data, policy_text, self.active_criteria
        )
        
        # Calculate weighted overall score
        total_weight = sum(criteria["weight"] for criteria in self.active_criteria.values())
        weighted_score = sum(
            score * self.active_criteria[criterion]["weight"] 
            for criterion, score in evaluation["criteria_scores"].items()
        )
        evaluation["overall_score"] = weighted_score / total_weight if total_weight > 0 else 0
        
        # Generate recommendations
        evaluation["recommendations"] = self._generate_recommendations(evaluation)
        
        return evaluation

    def _calculate_criteria_scores_with_rules(self, agents, monitor_data, policy_text, criteria_config):
        """Calculate scores using configured evaluation rules"""
        scores = {}
        
        for criterion_name, criterion_details in criteria_config.items():
            if criterion_details.get("custom", False):
                # Custom criterion
                score = self.rules_manager.calculate_custom_criterion_score(
                    criterion_name, criterion_details, agents, monitor_data
                )
            else:
                # Default criterion
                score = self._calculate_default_criterion_score(
                    criterion_name, agents, monitor_data, policy_text
                )
            
            scores[criterion_name] = score
        
        return scores

    def _calculate_default_criterion_score(self, criterion_name, agents, monitor_data, policy_text):
        """Calculate score for default criteria"""
        if criterion_name == "Public Support Level":
            supporters = sum(1 for agent in agents if getattr(agent, 'stance_on_policy', '').lower().find('supportive') != -1)
            support_ratio = supporters / len(agents)
            return support_ratio * 10
            
        elif criterion_name == "Implementation Feasibility":
            opponents = sum(1 for agent in agents if any(word in getattr(agent, 'stance_on_policy', '').lower() 
                           for word in ['skeptical', 'concerned', 'opposed']))
            feasibility = max(0, 10 - (opponents / len(agents)) * 10)
            return feasibility
            
        elif criterion_name == "Economic Impact Perception":
            if "tariff" in policy_text.lower():
                return 4.0  # Tariffs generally perceived negatively
            elif "work-from-home" in policy_text.lower():
                return 7.5
            else:
                return 6.0
                
        elif criterion_name == "Social Cohesion":
            avg_interactions = sum(len(agent.memory) for agent in agents) / len(agents)
            return min(avg_interactions * 2, 10)
            
        elif criterion_name == "Adaptation Speed":
            adapted_agents = sum(1 for agent in agents if agent.policy_knowledge)
            return (adapted_agents / len(agents)) * 10
            
        else:
            return 5.0  # Default neutral score

    def _analyze_support_patterns(self, agents, policy_text):
        """Analyze which personality types support or oppose the policy"""
        support_patterns = {
            "supporters": [],
            "opponents": [],
            "neutral": [],
            "support_percentage": 0,
            "opposition_percentage": 0,
            "key_supporting_traits": [],
            "key_opposing_traits": []
        }
        
        for agent in agents:
            stance = getattr(agent, 'stance_on_policy', 'neutral')
            if any(word in stance.lower() for word in ['supportive', 'positive', 'beneficial', 'good']):
                support_patterns["supporters"].append({
                    "name": agent.name,
                    "personality": agent.personality_traits,
                    "stance": stance
                })
            elif any(word in stance.lower() for word in ['opposed', 'against', 'skeptical', 'concerned', 'worried']):
                support_patterns["opponents"].append({
                    "name": agent.name,
                    "personality": agent.personality_traits,
                    "stance": stance
                })
            else:
                support_patterns["neutral"].append({
                    "name": agent.name,
                    "personality": agent.personality_traits,
                    "stance": stance
                })
        
        total_agents = len(agents)
        support_patterns["support_percentage"] = (len(support_patterns["supporters"]) / total_agents) * 100
        support_patterns["opposition_percentage"] = (len(support_patterns["opponents"]) / total_agents) * 100
        support_patterns["neutral_percentage"] = (len(support_patterns["neutral"]) / total_agents) * 100
        
        # Identify key traits
        support_patterns["key_supporting_traits"] = self._extract_common_traits(support_patterns["supporters"])
        support_patterns["key_opposing_traits"] = self._extract_common_traits(support_patterns["opponents"])
        
        return support_patterns

    def _extract_common_traits(self, agent_group):
        """Extract common personality traits from a group of agents"""
        if not agent_group:
            return []
        
        trait_words = []
        for agent in agent_group:
            personality = agent["personality"].lower()
            words = [word.strip() for word in personality.replace(" and ", " ").split()]
            trait_words.extend(words)
        
        # Count frequency and return most common
        trait_counts = {}
        for trait in trait_words:
            trait_counts[trait] = trait_counts.get(trait, 0) + 1
        
        # Return traits that appear in more than one agent
        common_traits = [trait for trait, count in trait_counts.items() if count > 1 or len(agent_group) == 1]
        return common_traits[:3]  # Top 3 most common traits

    def _analyze_agent_response(self, agent, monitor_data):
        """Analyze individual agent's response to the policy"""
        analysis = {
            "personality": agent.personality_traits,
            "total_actions": len(agent.log),
            "memory_utilization": len(agent.memory) / agent.memory.maxlen,
            "policy_engagement": "High" if agent.policy_knowledge else "Low",
            "behavioral_pattern": self._classify_behavior(agent),
            "stance": getattr(agent, 'stance_on_policy', 'Unknown'),
            "action_diversity": self._calculate_action_diversity(agent)
        }
        return analysis

    def _calculate_action_diversity(self, agent):
        """Calculate how diverse the agent's actions are"""
        if len(agent.log) < 2:
            return "Insufficient data"
        
        # Simple diversity check - look for repeated keywords
        actions = [entry for entry in agent.log if entry.startswith("Acted:")]
        if len(actions) < 2:
            return "Limited actions"
        
        # Check for repeated phrases
        action_texts = [action.replace("Acted: ", "") for action in actions]
        unique_words = set()
        total_words = 0
        
        for action in action_texts:
            words = action.lower().split()
            unique_words.update(words)
            total_words += len(words)
        
        diversity_ratio = len(unique_words) / max(total_words, 1)
        
        if diversity_ratio > 0.7:
            return "High diversity"
        elif diversity_ratio > 0.5:
            return "Moderate diversity"
        else:
            return "Low diversity (repetitive)"

    def _classify_behavior(self, agent):
        """Classify agent behavior based on their actions and personality"""
        if not agent.log:
            return "Inactive"
        
        stance = getattr(agent, 'stance_on_policy', '')
        personality_lower = agent.personality_traits.lower()
        
        if "supportive" in stance.lower():
            return "Policy Advocate"
        elif "skeptical" in stance.lower() or "concerned" in stance.lower():
            return "Policy Critic"
        elif "neutral" in stance.lower():
            return "Information Seeker"
        elif "outgoing" in personality_lower or "social" in personality_lower:
            return "Community Mobilizer"
        else:
            return "Cautious Observer"

    def _generate_recommendations(self, evaluation):
        """Generate recommendations based on evaluation results"""
        recommendations = []
        support_analysis = evaluation["support_analysis"]
        overall_score = evaluation["overall_score"]
        policy_text = evaluation["policy_text"]
        
        # Overall assessment
        if overall_score >= 7:
            recommendations.append("✅ Policy has strong community acceptance")
            recommendations.append("🎯 Proceed with implementation while maintaining communication")
        elif overall_score >= 5:
            recommendations.append("⚠️ Policy has moderate acceptance with concerns")
            recommendations.append("🛠️ Address specific concerns before full implementation")
        else:
            recommendations.append("❌ Policy faces significant community resistance")
            recommendations.append("🔄 Consider revising policy or improving communication strategy")
        
        # Support-specific recommendations
        support_pct = support_analysis["support_percentage"]
        if support_pct < 30:
            recommendations.append("📢 Launch comprehensive public education campaign")
        elif support_pct < 60:
            recommendations.append("🤝 Engage with neutral parties to build broader support")
        
        # Personality-based recommendations
        if support_analysis["key_supporting_traits"]:
            traits_str = ", ".join(support_analysis["key_supporting_traits"])
            recommendations.append(f"💡 Leverage {traits_str} personalities as policy champions")
        
        if support_analysis["key_opposing_traits"]:
            traits_str = ", ".join(support_analysis["key_opposing_traits"])
            recommendations.append(f"🎯 Develop targeted messaging for {traits_str} personalities")
        
        # Custom criteria recommendations
        criteria_config = evaluation["evaluation_criteria"]
        for criterion_name, criterion_details in criteria_config.items():
            if criterion_details.get("custom", False):
                score = evaluation["criteria_scores"].get(criterion_name, 0)
                if score < 5:
                    recommendations.append(f"⚠️ Address concerns in '{criterion_name}' (Score: {score:.1f}/10)")
        
        return recommendations

    def print_evaluation_report(self, evaluation):
        """Print a detailed evaluation report with custom criteria"""
        print(f"\n{'🔍 POLICY IMPACT EVALUATION REPORT':^60}")
        print(f"{'='*60}")
        print(f"Policy: {evaluation['policy_text']}")
        
        # Show evaluation configuration
        print(f"\n📊 EVALUATION CONFIGURATION:")
        print(f"{'-'*40}")
        criteria_config = evaluation["evaluation_criteria"]
        for criterion_name, criterion_details in criteria_config.items():
            weight_pct = criterion_details["weight"] * 100
            custom_marker = " (CUSTOM)" if criterion_details.get("custom", False) else ""
            print(f"  {criterion_name}{custom_marker}: {weight_pct:.0f}% weight")
        
        # Overall Score
        overall_score = evaluation["overall_score"]
        print(f"\n📊 OVERALL POLICY EFFECTIVENESS: {overall_score:.1f}/10")
        
        if overall_score >= 7:
            print("🟢 EXCELLENT - Policy has strong community support")
        elif overall_score >= 5:
            print("🟡 MODERATE - Policy has mixed reception with room for improvement")
        elif overall_score >= 3:
            print("🟠 CHALLENGING - Policy faces significant concerns")
        else:
            print("🔴 DIFFICULT - Policy has low acceptance and high resistance")
        
        # Support Analysis
        support_analysis = evaluation["support_analysis"]
        print(f"\n📈 PUBLIC SUPPORT ANALYSIS:")
        print(f"{'-'*40}")
        print(f"Support Level: {support_analysis['support_percentage']:.1f}%")
        print(f"Opposition Level: {support_analysis['opposition_percentage']:.1f}%")
        print(f"Neutral/Undecided: {support_analysis['neutral_percentage']:.1f}%")
        
        # Criteria Breakdown
        print(f"\n📈 DETAILED CRITERIA ANALYSIS:")
        print(f"{'-'*40}")
        for criterion, score in evaluation["criteria_scores"].items():
            weight = criteria_config[criterion]["weight"] * 100
            bar = "█" * int(score) + "░" * (10 - int(score))
            custom_marker = " (CUSTOM)" if criteria_config[criterion].get("custom", False) else ""
            print(f"{criterion}{custom_marker:<5} {score:>4.1f}/10 (Weight: {weight:.0f}%) [{bar}]")
        
        # Support breakdown
        print(f"\n👥 SUPPORT BY PERSONALITY TYPE:")
        if support_analysis["supporters"]:
            print("🟢 SUPPORTERS:")
            for supporter in support_analysis["supporters"]:
                print(f"   • {supporter['name']} ({supporter['personality']}): {supporter['stance']}")
        
        if support_analysis["opponents"]:
            print("🔴 OPPOSITION:")
            for opponent in support_analysis["opponents"]:
                print(f"   • {opponent['name']} ({opponent['personality']}): {opponent['stance']}")
        
        if support_analysis["neutral"]:
            print("🟡 NEUTRAL:")
            for neutral in support_analysis["neutral"]:
                print(f"   • {neutral['name']} ({neutral['personality']}): {neutral['stance']}")
        
        # Individual Agent Analysis
        print(f"\n👥 INDIVIDUAL AGENT ANALYSIS:")
        print(f"{'-'*40}")
        for agent_name, analysis in evaluation["agent_analysis"].items():
            print(f"\n🤖 {agent_name}:")
            print(f"   Personality: {analysis['personality']}")
            print(f"   Policy Stance: {analysis['stance']}")
            print(f"   Behavior Pattern: {analysis['behavioral_pattern']}")
            print(f"   Action Diversity: {analysis['action_diversity']}")
            print(f"   Activity Level: {analysis['total_actions']} actions")
            print(f"   Policy Engagement: {analysis['policy_engagement']}")
        
        # Recommendations
        print(f"\n💡 STRATEGIC RECOMMENDATIONS:")
        print(f"{'-'*40}")
        for i, recommendation in enumerate(evaluation["recommendations"], 1):
            print(f"{i}. {recommendation}")
        
        print(f"\n{'='*60}")