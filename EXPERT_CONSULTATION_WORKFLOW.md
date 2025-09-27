# Expert Consultation Workflow
*Structured escalation to human experts when automated research isn't sufficient*

## 🎯 Overview

This workflow defines when and how to escalate infrastructure issues to human experts, ensuring efficient use of expert time while providing comprehensive context for rapid resolution. The system balances automated research capabilities with human expertise access.

## 🔄 Escalation Decision Framework

### Automatic Escalation Triggers

#### **Critical (Immediate Escalation)**
```python
CRITICAL_ESCALATION_CRITERIA = {
    'production_down': {
        'keywords': ['outage', 'down', 'offline', 'unavailable', 'critical'],
        'business_impact': 'high',
        'escalation_time': 'immediate',
        'expert_level': 'senior'
    },

    'security_incident': {
        'keywords': ['breach', 'intrusion', 'malware', 'unauthorized', 'compromised'],
        'business_impact': 'critical',
        'escalation_time': 'immediate',
        'expert_level': 'security_specialist'
    },

    'data_loss': {
        'keywords': ['corruption', 'lost', 'deleted', 'recovery', 'backup_failed'],
        'business_impact': 'critical',
        'escalation_time': 'immediate',
        'expert_level': 'data_recovery_specialist'
    }
}
```

#### **High Priority (30-minute rule)**
- Multiple failed automated remediation attempts
- Performance degradation affecting >50% of users
- Configuration changes with unexpected results
- Vendor escalation recommended by automated research

#### **Standard Priority (4-hour rule)**
- Complex multi-vendor integration issues
- Automation research confidence < 60%
- Best practice guidance requests for major changes
- Compliance or regulatory questions

### Escalation Decision Algorithm

```python
class EscalationDecisionEngine:
    """
    Determines when and how to escalate to human experts
    """

    def __init__(self):
        self.escalation_rules = self._load_escalation_rules()
        self.expert_availability = self._load_expert_availability()

    def should_escalate(self, issue_context, research_results):
        """
        Determine if expert escalation is warranted

        Args:
            issue_context: Issue details and business impact
            research_results: Results from automated research

        Returns:
            Escalation decision with reasoning
        """

        escalation_factors = {
            'business_impact_score': self._calculate_business_impact(issue_context),
            'research_confidence': research_results.get('overall_confidence', 0.0),
            'time_invested': research_results.get('research_duration_minutes', 0),
            'failed_attempts': research_results.get('failed_remediation_attempts', 0),
            'complexity_indicators': self._assess_complexity(issue_context),
            'vendor_escalation_suggested': research_results.get('vendor_escalation_recommended', False)
        }

        # Apply escalation scoring algorithm
        escalation_score = self._calculate_escalation_score(escalation_factors)

        decision = {
            'should_escalate': escalation_score > 0.7,
            'escalation_urgency': self._determine_urgency(escalation_factors),
            'recommended_expert_type': self._select_expert_type(issue_context),
            'escalation_reason': self._generate_escalation_reasoning(escalation_factors),
            'estimated_expert_time_needed': self._estimate_expert_time(escalation_factors)
        }

        return decision

    def _calculate_business_impact(self, issue_context):
        """Calculate business impact score (0.0 to 1.0)"""

        impact_factors = {
            'users_affected': issue_context.get('users_affected', 0),
            'systems_affected': len(issue_context.get('affected_systems', [])),
            'revenue_impact': issue_context.get('estimated_revenue_impact', 0),
            'compliance_risk': issue_context.get('compliance_risk_level', 'low'),
            'data_sensitivity': issue_context.get('data_classification', 'internal')
        }

        # Weighted scoring algorithm
        weights = {
            'users_affected': 0.3,
            'systems_affected': 0.2,
            'revenue_impact': 0.2,
            'compliance_risk': 0.15,
            'data_sensitivity': 0.15
        }

        normalized_scores = {
            'users_affected': min(impact_factors['users_affected'] / 1000, 1.0),
            'systems_affected': min(impact_factors['systems_affected'] / 10, 1.0),
            'revenue_impact': min(impact_factors['revenue_impact'] / 100000, 1.0),
            'compliance_risk': {'low': 0.0, 'medium': 0.5, 'high': 1.0}.get(impact_factors['compliance_risk'], 0.0),
            'data_sensitivity': {'public': 0.0, 'internal': 0.3, 'confidential': 0.7, 'restricted': 1.0}.get(impact_factors['data_sensitivity'], 0.0)
        }

        business_impact_score = sum(
            normalized_scores[factor] * weights[factor]
            for factor in weights
        )

        return min(business_impact_score, 1.0)
```

## 👥 Expert Network Configuration

### Expert Categories and Specializations

```python
EXPERT_NETWORK = {
    'network_architecture': {
        'specializations': [
            'large_scale_routing',
            'datacenter_design',
            'wan_optimization',
            'network_security_design',
            'sdwan_implementation'
        ],
        'certifications_required': ['CCIE R&S', 'JNCIE-ENT', 'CISSP'],
        'availability': {
            'business_hours': '8x5',
            'after_hours': 'on_call_rotation',
            'response_sla': '30_minutes'
        },
        'escalation_methods': ['slack', 'phone', 'video_conference'],
        'expertise_level': 'senior'
    },

    'security_engineering': {
        'specializations': [
            'incident_response',
            'forensics',
            'vulnerability_management',
            'compliance_frameworks',
            'threat_hunting'
        ],
        'certifications_required': ['CISSP', 'CCIE Security', 'GCIH', 'GCFA'],
        'availability': {
            'business_hours': '24x7',
            'after_hours': '24x7',
            'response_sla': '15_minutes'
        },
        'escalation_methods': ['secure_chat', 'encrypted_phone', 'secure_video'],
        'expertise_level': 'expert'
    },

    'cloud_architecture': {
        'specializations': [
            'aws_architecture',
            'azure_architecture',
            'gcp_architecture',
            'multi_cloud_design',
            'cloud_migration',
            'cost_optimization'
        ],
        'certifications_required': [
            'AWS Solutions Architect Professional',
            'Azure Solutions Architect Expert',
            'Google Cloud Professional Architect'
        ],
        'availability': {
            'business_hours': '8x5',
            'after_hours': 'on_call_rotation',
            'response_sla': '45_minutes'
        },
        'escalation_methods': ['slack', 'email', 'video_conference'],
        'expertise_level': 'senior'
    },

    'virtualization': {
        'specializations': [
            'vsphere_troubleshooting',
            'performance_tuning',
            'disaster_recovery',
            'vsan_design',
            'nsx_implementation'
        ],
        'certifications_required': ['VCDX', 'VCP-DCV', 'VCAP-DCV'],
        'availability': {
            'business_hours': '8x5',
            'after_hours': 'emergency_only',
            'response_sla': '1_hour'
        },
        'escalation_methods': ['screen_share', 'remote_access', 'phone'],
        'expertise_level': 'senior'
    },

    'automation_engineering': {
        'specializations': [
            'infrastructure_as_code',
            'ci_cd_pipelines',
            'ansible_automation',
            'python_scripting',
            'api_integration'
        ],
        'certifications_required': ['Red Hat Certified Engineer', 'AWS DevOps Professional'],
        'availability': {
            'business_hours': '8x5',
            'after_hours': 'on_call_rotation',
            'response_sla': '1_hour'
        },
        'escalation_methods': ['slack', 'email', 'screen_share'],
        'expertise_level': 'senior'
    }
}
```

### Expert Selection Algorithm

```python
class ExpertSelectionEngine:
    """
    Selects optimal expert based on issue characteristics and availability
    """

    def select_optimal_expert(self, issue_context, urgency_level):
        """
        Select the best available expert for the given issue
        """

        # Analyze issue to determine required expertise
        required_expertise = self._analyze_expertise_requirements(issue_context)

        # Get available experts matching requirements
        available_experts = self._get_available_experts(
            expertise_requirements=required_expertise,
            urgency_level=urgency_level
        )

        # Score and rank experts
        expert_scores = []
        for expert in available_experts:
            score = self._score_expert_match(expert, issue_context, required_expertise)
            expert_scores.append((expert, score))

        # Sort by score (highest first)
        expert_scores.sort(key=lambda x: x[1]['total_score'], reverse=True)

        if expert_scores:
            best_expert, best_score = expert_scores[0]
            alternatives = [expert for expert, score in expert_scores[1:3]]  # Next 2 best

            return {
                'primary_expert': best_expert,
                'confidence': best_score['confidence'],
                'alternatives': alternatives,
                'selection_reasoning': best_score['reasoning'],
                'estimated_response_time': best_expert['response_sla'],
                'preferred_communication': best_expert['preferred_method']
            }
        else:
            return self._handle_no_available_experts(required_expertise, urgency_level)

    def _score_expert_match(self, expert, issue_context, requirements):
        """
        Score how well an expert matches the issue requirements
        """

        scoring_factors = {
            'specialization_match': self._score_specialization_match(expert, requirements),
            'experience_level': self._score_experience_level(expert, issue_context),
            'availability_score': self._score_availability(expert, requirements['urgency']),
            'past_performance': self._score_past_performance(expert, issue_context),
            'current_workload': self._score_current_workload(expert)
        }

        # Weighted total score
        weights = {
            'specialization_match': 0.4,
            'experience_level': 0.2,
            'availability_score': 0.2,
            'past_performance': 0.1,
            'current_workload': 0.1
        }

        total_score = sum(
            scoring_factors[factor] * weights[factor]
            for factor in weights
        )

        return {
            'total_score': total_score,
            'confidence': min(total_score, 1.0),
            'reasoning': self._generate_selection_reasoning(scoring_factors),
            'factors': scoring_factors
        }
```

## 📋 Escalation Package Preparation

### Comprehensive Context Assembly

```python
class EscalationPackageBuilder:
    """
    Builds comprehensive context package for expert consultation
    """

    def build_escalation_package(self, issue_context, research_results, escalation_decision):
        """
        Create comprehensive package for expert handoff
        """

        package = {
            'metadata': self._build_metadata(issue_context, escalation_decision),
            'executive_summary': self._build_executive_summary(issue_context),
            'technical_summary': self._build_technical_summary(issue_context, research_results),
            'business_impact': self._build_business_impact_summary(issue_context),
            'timeline': self._build_issue_timeline(issue_context),
            'research_summary': self._build_research_summary(research_results),
            'current_hypotheses': self._extract_hypotheses(research_results),
            'data_artifacts': self._collect_data_artifacts(issue_context),
            'environment_context': self._build_environment_context(issue_context),
            'constraints': self._identify_constraints(issue_context),
            'success_criteria': self._define_success_criteria(issue_context),
            'recommended_approach': self._suggest_expert_approach(research_results)
        }

        # Format for expert consumption
        formatted_package = self._format_for_expert_consumption(package)

        return formatted_package

    def _build_executive_summary(self, issue_context):
        """
        Create concise executive summary for rapid expert understanding
        """

        summary_template = {
            'issue_description': issue_context.get('description', 'Not provided'),
            'business_impact': {
                'severity': issue_context.get('severity', 'Unknown'),
                'affected_users': issue_context.get('users_affected', 0),
                'affected_systems': issue_context.get('affected_systems', []),
                'estimated_downtime': issue_context.get('estimated_downtime', 'Unknown'),
                'financial_impact': issue_context.get('financial_impact', 'To be determined')
            },
            'current_status': issue_context.get('current_status', 'Under investigation'),
            'urgency_justification': issue_context.get('urgency_reason', 'Standard escalation'),
            'key_stakeholders': issue_context.get('stakeholders', [])
        }

        return summary_template

    def _build_technical_summary(self, issue_context, research_results):
        """
        Create detailed technical summary with research findings
        """

        technical_summary = {
            'symptoms': issue_context.get('symptoms', []),
            'error_messages': issue_context.get('error_messages', []),
            'affected_infrastructure': {
                'devices': issue_context.get('affected_devices', []),
                'software_versions': issue_context.get('software_versions', {}),
                'configurations': issue_context.get('relevant_configs', []),
                'network_topology': issue_context.get('topology_info', {})
            },
            'research_findings': {
                'vendor_documentation': research_results.get('vendor_research', {}),
                'known_issues': research_results.get('known_bugs', []),
                'community_solutions': research_results.get('community_research', {}),
                'best_practices': research_results.get('best_practices', [])
            },
            'attempted_solutions': issue_context.get('attempted_solutions', []),
            'current_working_theory': research_results.get('primary_hypothesis', 'Under investigation')
        }

        return technical_summary
```

### Expert Communication Templates

```python
class ExpertCommunicationTemplates:
    """
    Standardized templates for expert communication
    """

    def generate_initial_contact(self, escalation_package, expert_info):
        """
        Generate initial expert contact message
        """

        template = f"""
Subject: {escalation_package['metadata']['urgency']} Infrastructure Issue - Expert Consultation Requested

{expert_info['name']},

We need your expertise on a {escalation_package['metadata']['urgency'].lower()} infrastructure issue:

EXECUTIVE SUMMARY:
{escalation_package['executive_summary']['issue_description']}

BUSINESS IMPACT:
- Affected Users: {escalation_package['business_impact']['affected_users']}
- Systems Down: {', '.join(escalation_package['business_impact']['affected_systems'])}
- Estimated Revenue Impact: {escalation_package['business_impact']['financial_impact']}

TECHNICAL SUMMARY:
{escalation_package['technical_summary']['current_working_theory']}

RESEARCH COMPLETED:
- Vendor documentation reviewed: {self._format_research_status(escalation_package['research_summary']['vendor_research'])}
- Community solutions explored: {self._format_research_status(escalation_package['research_summary']['community_research'])}
- Configuration analysis: {self._format_research_status(escalation_package['research_summary']['config_analysis'])}

IMMEDIATE NEED:
{escalation_package['recommended_approach']['immediate_actions']}

Full technical package attached. Available for {expert_info['preferred_communication']} at your earliest convenience.

Best regards,
Infrastructure Automation System
        """

        return template

    def generate_follow_up_template(self, expert_session_notes):
        """
        Generate follow-up communication after expert consultation
        """

        follow_up = f"""
Subject: Follow-up on Infrastructure Issue - Actions and Outcomes

CONSULTATION SUMMARY:
Expert: {expert_session_notes['expert_name']}
Duration: {expert_session_notes['session_duration']}
Date: {expert_session_notes['consultation_date']}

EXPERT RECOMMENDATIONS:
{self._format_recommendations(expert_session_notes['recommendations'])}

ACTIONS TAKEN:
{self._format_actions(expert_session_notes['actions_implemented'])}

CURRENT STATUS:
{expert_session_notes['current_status']}

NEXT STEPS:
{self._format_next_steps(expert_session_notes['next_steps'])}

LESSONS LEARNED:
{self._format_lessons_learned(expert_session_notes['lessons_learned'])}

Knowledge base updated with resolution steps for future reference.
        """

        return follow_up
```

## 🔄 Expert Session Management

### Session Workflow

```python
class ExpertSessionManager:
    """
    Manages expert consultation sessions from initiation to completion
    """

    def initiate_expert_session(self, escalation_package, expert_assignment):
        """
        Start expert consultation session
        """

        session = {
            'session_id': self._generate_session_id(),
            'expert_info': expert_assignment['primary_expert'],
            'issue_context': escalation_package,
            'start_time': datetime.now(),
            'communication_channel': expert_assignment['preferred_communication'],
            'session_status': 'initiated',
            'participants': [
                'expert',
                'requesting_engineer',
                'infrastructure_agent'
            ]
        }

        # Set up communication channel
        communication_setup = self._setup_communication_channel(
            channel_type=expert_assignment['preferred_communication'],
            participants=session['participants'],
            security_level=escalation_package['metadata']['security_classification']
        )

        session['communication_details'] = communication_setup

        # Send initial briefing to expert
        initial_briefing = self._send_initial_briefing(session)

        session['briefing_sent'] = initial_briefing

        return session

    def track_session_progress(self, session_id):
        """
        Track and update session progress
        """

        session = self._get_session(session_id)

        progress_update = {
            'session_id': session_id,
            'elapsed_time': datetime.now() - session['start_time'],
            'current_phase': self._determine_current_phase(session),
            'expert_engagement_level': self._assess_expert_engagement(session),
            'progress_indicators': self._collect_progress_indicators(session),
            'estimated_completion': self._estimate_completion_time(session)
        }

        return progress_update

    def capture_session_outcomes(self, session_id, session_notes):
        """
        Capture and document session outcomes
        """

        session = self._get_session(session_id)

        outcomes = {
            'resolution_achieved': session_notes['issue_resolved'],
            'expert_recommendations': session_notes['recommendations'],
            'actions_implemented': session_notes['actions_taken'],
            'knowledge_gained': session_notes['new_insights'],
            'process_improvements': session_notes['process_feedback'],
            'follow_up_required': session_notes['follow_up_needed'],
            'session_rating': session_notes['effectiveness_rating'],
            'time_to_resolution': datetime.now() - session['start_time']
        }

        # Update knowledge base
        self._update_knowledge_base(outcomes)

        # Generate session report
        session_report = self._generate_session_report(session, outcomes)

        return {
            'outcomes': outcomes,
            'report': session_report,
            'knowledge_base_updated': True
        }
```

## 📊 Expert Network Analytics

### Performance Tracking

```python
class ExpertNetworkAnalytics:
    """
    Track expert network performance and optimization opportunities
    """

    def analyze_expert_effectiveness(self, time_period='30_days'):
        """
        Analyze expert consultation effectiveness
        """

        analytics = {
            'escalation_metrics': self._calculate_escalation_metrics(time_period),
            'expert_performance': self._analyze_expert_performance(time_period),
            'resolution_outcomes': self._analyze_resolution_outcomes(time_period),
            'knowledge_transfer': self._measure_knowledge_transfer(time_period),
            'cost_effectiveness': self._calculate_cost_effectiveness(time_period)
        }

        return analytics

    def identify_optimization_opportunities(self, analytics_data):
        """
        Identify ways to optimize expert network utilization
        """

        opportunities = {
            'automation_candidates': self._find_automation_candidates(analytics_data),
            'training_needs': self._identify_training_gaps(analytics_data),
            'process_improvements': self._suggest_process_improvements(analytics_data),
            'expert_network_gaps': self._identify_expertise_gaps(analytics_data),
            'knowledge_base_enhancements': self._suggest_kb_improvements(analytics_data)
        }

        return opportunities

    def generate_expert_network_report(self, analytics_data, opportunities):
        """
        Generate comprehensive expert network performance report
        """

        report = f"""
        # Expert Network Performance Report

        ## Executive Summary
        - Total Escalations: {analytics_data['escalation_metrics']['total_escalations']}
        - Average Resolution Time: {analytics_data['resolution_outcomes']['avg_resolution_time']}
        - Success Rate: {analytics_data['resolution_outcomes']['success_rate']}%
        - Cost per Resolution: ${analytics_data['cost_effectiveness']['cost_per_resolution']}

        ## Key Insights
        {self._format_key_insights(analytics_data)}

        ## Optimization Opportunities
        {self._format_opportunities(opportunities)}

        ## Recommendations
        {self._generate_recommendations(analytics_data, opportunities)}
        """

        return report
```

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Create infrastructure researcher agent for deep technical expertise", "status": "completed", "activeForm": "Created researcher agent that can access technical documentation and best practices"}, {"content": "Identify knowledge sources for infrastructure troubleshooting", "status": "completed", "activeForm": "Mapped out comprehensive technical knowledge sources and expert systems"}, {"content": "Design agent patterns for accessing vendor documentation", "status": "completed", "activeForm": "Created structured patterns for accessing Cisco, VMware, AWS, Microsoft documentation"}, {"content": "Create expert consultation workflow", "status": "completed", "activeForm": "Designed comprehensive workflow for escalating to human experts when needed"}]