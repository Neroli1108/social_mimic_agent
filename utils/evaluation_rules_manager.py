class EvaluationRulesManager:
    def __init__(self):
        self.default_criteria = {
            "Public Support Level": {
                "weight": 0.25,
                "description": "Measures the percentage of agents supporting the policy",
                "calculation": "Based on agent stance analysis and personality alignment"
            },
            "Implementation Feasibility": {
                "weight": 0.20,
                "description": "Assesses how easily the policy can be implemented",
                "calculation": "Inverse of resistance level and opposition strength"
            },
            "Economic Impact Perception": {
                "weight": 0.20,
                "description": "Evaluates perceived economic effects on stakeholders",
                "calculation": "Policy-specific analysis based on type and scope"
            },
            "Social Cohesion": {
                "weight": 0.20,
                "description": "Measures community unity and interaction patterns",
                "calculation": "Based on communication frequency and collaboration"
            },
            "Adaptation Speed": {
                "weight": 0.15,
                "description": "How quickly agents adapt to policy changes",
                "calculation": "Rate of policy knowledge integration and behavior change"
            }
        }
        
        self.custom_criteria = {}
        self.active_criteria = self.default_criteria.copy()

    def display_default_rules(self):
        """Display the default evaluation criteria and rules"""
        print(f"\n📊 DEFAULT POLICY EVALUATION CRITERIA")
        print("="*60)
        
        total_weight = sum(criteria["weight"] for criteria in self.default_criteria.values())
        
        for i, (criterion, details) in enumerate(self.default_criteria.items(), 1):
            percentage = (details["weight"] / total_weight) * 100
            print(f"\n{i}. {criterion} (Weight: {percentage:.0f}%)")
            print(f"   Description: {details['description']}")
            print(f"   Calculation: {details['calculation']}")
        
        print(f"\n📋 SCORING SYSTEM:")
        print(f"   • Each criterion is scored from 0-10")
        print(f"   • Final score is weighted average of all criteria")
        print(f"   • 8-10: Excellent policy acceptance")
        print(f"   • 6-8:  Good policy with minor concerns")
        print(f"   • 4-6:  Moderate policy requiring improvements")
        print(f"   • 0-4:  Poor policy needing major revision")

    def get_evaluation_preferences(self):
        """Get user preferences for evaluation criteria"""
        print(f"\n🎯 POLICY EVALUATION CONFIGURATION")
        print("="*60)
        print("1. Use default evaluation criteria")
        print("2. Customize weights for existing criteria")
        print("3. Add custom evaluation criteria")
        print("4. View detailed explanation of default criteria")
        
        choice = input("\nSelect option (1-4, default=1): ").strip()
        
        if choice == "2":
            return self.customize_weights()
        elif choice == "3":
            return self.add_custom_criteria()
        elif choice == "4":
            self.display_detailed_explanation()
            return self.get_evaluation_preferences()
        else:
            print("\n✓ Using default evaluation criteria")
            return self.default_criteria

    def display_detailed_explanation(self):
        """Display detailed explanation of how each criterion works"""
        self.display_default_rules()
        
        print(f"\n📚 DETAILED CRITERION EXPLANATIONS:")
        print("="*60)
        
        explanations = {
            "Public Support Level": [
                "• Analyzes agent stance keywords (supportive, opposed, neutral)",
                "• Considers personality alignment with policy type",
                "• Counts explicit support vs opposition statements",
                "• Weighs influential personality types more heavily"
            ],
            "Implementation Feasibility": [
                "• Measures resistance intensity from agent responses",
                "• Evaluates practical barriers mentioned by agents",
                "• Considers resource requirements vs available capacity",
                "• Assesses coordination complexity between stakeholders"
            ],
            "Economic Impact Perception": [
                "• Policy-specific impact analysis (tariffs = negative, remote work = positive)",
                "• Agent concern frequency about economic effects",
                "• Business vs consumer perspective balance",
                "• Short-term vs long-term economic considerations"
            ],
            "Social Cohesion": [
                "• Communication frequency between agents",
                "• Collaboration vs conflict patterns",
                "• Community engagement levels",
                "• Polarization vs consensus indicators"
            ],
            "Adaptation Speed": [
                "• Time to policy knowledge integration",
                "• Behavioral change indicators",
                "• Learning curve steepness",
                "• Resistance duration and intensity"
            ]
        }
        
        for criterion, details in explanations.items():
            print(f"\n🔍 {criterion}:")
            for detail in details:
                print(f"   {detail}")
        
        input("\nPress Enter to continue...")

    def customize_weights(self):
        """Allow user to customize weights for existing criteria"""
        print(f"\n⚖️ CUSTOMIZE EVALUATION WEIGHTS")
        print("-" * 40)
        print("Current weights (must sum to 1.0):")
        
        # Display current weights
        for criterion, details in self.default_criteria.items():
            percentage = details["weight"] * 100
            print(f"  {criterion}: {percentage:.0f}%")
        
        print(f"\n💡 Tips:")
        print(f"   • Higher weights = more influence on final score")
        print(f"   • Weights must sum to 100%")
        print(f"   • Press Enter to keep current weight")
        
        new_criteria = {}
        total_weight = 0
        
        for criterion, details in self.default_criteria.items():
            current_percentage = details["weight"] * 100
            
            while True:
                try:
                    user_input = input(f"\n{criterion} weight (current: {current_percentage:.0f}%): ").strip()
                    
                    if not user_input:
                        # Keep current weight
                        weight_percentage = current_percentage
                        break
                    else:
                        weight_percentage = float(user_input)
                        if 0 <= weight_percentage <= 100:
                            break
                        else:
                            print("Please enter a percentage between 0 and 100")
                except ValueError:
                    print("Please enter a valid number")
            
            new_weight = weight_percentage / 100
            new_criteria[criterion] = {
                "weight": new_weight,
                "description": details["description"],
                "calculation": details["calculation"]
            }
            total_weight += new_weight
        
        # Normalize weights to sum to 1.0
        if total_weight != 1.0:
            print(f"\n⚠️ Weights sum to {total_weight*100:.1f}%. Normalizing to 100%...")
            for criterion in new_criteria:
                new_criteria[criterion]["weight"] /= total_weight
        
        # Display final weights
        print(f"\n✓ FINAL EVALUATION WEIGHTS:")
        for criterion, details in new_criteria.items():
            percentage = details["weight"] * 100
            print(f"   {criterion}: {percentage:.0f}%")
        
        confirm = input("\nConfirm these weights? (y/n, default=y): ").strip().lower()
        if confirm != 'n':
            self.active_criteria = new_criteria
            return new_criteria
        else:
            return self.get_evaluation_preferences()

    def add_custom_criteria(self):
        """Allow user to add custom evaluation criteria"""
        print(f"\n➕ ADD CUSTOM EVALUATION CRITERIA")
        print("-" * 40)
        
        # Start with default criteria
        new_criteria = self.default_criteria.copy()
        
        while True:
            print(f"\nCurrent criteria:")
            for i, criterion in enumerate(new_criteria.keys(), 1):
                print(f"  {i}. {criterion}")
            
            add_more = input(f"\nAdd a custom criterion? (y/n): ").strip().lower()
            if add_more != 'y':
                break
            
            # Get custom criterion details
            criterion_name = input("Enter criterion name: ").strip()
            if not criterion_name:
                print("Criterion name cannot be empty")
                continue
                
            if criterion_name in new_criteria:
                print("This criterion already exists")
                continue
            
            description = input("Enter criterion description: ").strip()
            if not description:
                description = "Custom evaluation criterion"
            
            print(f"\nHow should this criterion be calculated?")
            print(f"1. Agent sentiment analysis (positive/negative responses)")
            print(f"2. Behavioral change frequency (action diversity)")
            print(f"3. Communication pattern analysis (interaction levels)")
            print(f"4. Custom keyword matching")
            print(f"5. Manual scoring (user-defined)")
            
            calc_choice = input("Select calculation method (1-5, default=1): ").strip()
            
            calculation_methods = {
                "1": "Sentiment analysis of agent responses and stance",
                "2": "Behavioral change frequency and action diversity",
                "3": "Communication patterns and interaction analysis",
                "4": "Custom keyword matching in agent responses",
                "5": "Manual scoring based on user observation"
            }
            
            calculation = calculation_methods.get(calc_choice, calculation_methods["1"])
            
            # Get weight
            while True:
                try:
                    weight_input = input(f"Enter weight percentage (0-100, default=10): ").strip()
                    weight_percentage = float(weight_input) if weight_input else 10.0
                    
                    if 0 <= weight_percentage <= 100:
                        break
                    else:
                        print("Please enter a percentage between 0 and 100")
                except ValueError:
                    print("Please enter a valid number")
            
            new_criteria[criterion_name] = {
                "weight": weight_percentage / 100,
                "description": description,
                "calculation": calculation,
                "custom": True
            }
            
            print(f"✓ Added: {criterion_name}")
        
        # Normalize all weights
        total_weight = sum(details["weight"] for details in new_criteria.values())
        if total_weight > 0:
            for criterion in new_criteria:
                new_criteria[criterion]["weight"] /= total_weight
        
        # Display final configuration
        print(f"\n✓ FINAL EVALUATION CONFIGURATION:")
        for criterion, details in new_criteria.items():
            percentage = details["weight"] * 100
            custom_marker = " (CUSTOM)" if details.get("custom", False) else ""
            print(f"   {criterion}{custom_marker}: {percentage:.1f}%")
        
        confirm = input("\nConfirm this configuration? (y/n, default=y): ").strip().lower()
        if confirm != 'n':
            self.active_criteria = new_criteria
            return new_criteria
        else:
            return self.get_evaluation_preferences()

    def get_active_criteria(self):
        """Get the currently active evaluation criteria"""
        return self.active_criteria

    def calculate_custom_criterion_score(self, criterion_name, criterion_details, agents, monitor_data):
        """Calculate score for custom criteria"""
        calculation_method = criterion_details["calculation"]
        
        if "sentiment analysis" in calculation_method.lower():
            return self._calculate_sentiment_score(agents)
        elif "behavioral change" in calculation_method.lower():
            return self._calculate_behavior_change_score(agents)
        elif "communication pattern" in calculation_method.lower():
            return self._calculate_communication_score(agents)
        elif "keyword matching" in calculation_method.lower():
            return self._calculate_keyword_score(agents, criterion_name)
        else:  # Manual scoring
            return self._get_manual_score(criterion_name)

    def _calculate_sentiment_score(self, agents):
        """Calculate sentiment-based score"""
        positive_count = 0
        total_responses = 0
        
        for agent in agents:
            stance = getattr(agent, 'stance_on_policy', '')
            if stance:
                total_responses += 1
                if any(word in stance.lower() for word in ['supportive', 'positive', 'beneficial', 'good', 'excellent']):
                    positive_count += 1
        
        return (positive_count / max(total_responses, 1)) * 10

    def _calculate_behavior_change_score(self, agents):
        """Calculate behavioral change score"""
        total_diversity = 0
        for agent in agents:
            actions = [entry for entry in agent.log if entry.startswith("Acted:")]
            if len(actions) > 1:
                unique_words = set()
                total_words = 0
                for action in actions:
                    words = action.lower().split()
                    unique_words.update(words)
                    total_words += len(words)
                diversity = len(unique_words) / max(total_words, 1)
                total_diversity += diversity
        
        avg_diversity = total_diversity / max(len(agents), 1)
        return min(avg_diversity * 15, 10)  # Scale to 0-10

    def _calculate_communication_score(self, agents):
        """Calculate communication pattern score"""
        total_interactions = sum(len(agent.memory) for agent in agents)
        avg_interactions = total_interactions / len(agents)
        return min(avg_interactions * 2, 10)  # Scale to 0-10

    def _calculate_keyword_score(self, agents, criterion_name):
        """Calculate keyword-based score"""
        # Simple keyword matching - can be enhanced
        positive_keywords = ['good', 'excellent', 'beneficial', 'positive', 'support']
        negative_keywords = ['bad', 'terrible', 'harmful', 'negative', 'oppose']
        
        positive_count = 0
        negative_count = 0
        
        for agent in agents:
            for log_entry in agent.log:
                entry_lower = log_entry.lower()
                positive_count += sum(1 for word in positive_keywords if word in entry_lower)
                negative_count += sum(1 for word in negative_keywords if word in entry_lower)
        
        total_sentiment = positive_count + negative_count
        if total_sentiment == 0:
            return 5.0  # Neutral
        
        sentiment_ratio = positive_count / total_sentiment
        return sentiment_ratio * 10

    def _get_manual_score(self, criterion_name):
        """Get manual score from user"""
        while True:
            try:
                score = input(f"Enter manual score for '{criterion_name}' (0-10): ").strip()
                score_value = float(score)
                if 0 <= score_value <= 10:
                    return score_value
                else:
                    print("Please enter a score between 0 and 10")
            except ValueError:
                print("Please enter a valid number")