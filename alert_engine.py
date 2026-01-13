"""
Alert Engine Module
Processes raw alerts through assessment, correlation, filtering, and scoring
Determines actionability of alerts
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import re


class AlertNormalizer:
    """Convert different alert formats to standard format"""
    
    @staticmethod
    def normalize(alert_data: Dict, source: str = "selenium") -> Dict:
        """
        Normalize alert to standard format
        
        Args:
            alert_data: Raw alert data
            source: Source of alert (selenium, api, etc)
        
        Returns:
            Normalized alert dict
        """
        return {
            "alert_id": alert_data.get("alert_id", f"alert_{int(time.time() * 1000)}"),
            "timestamp": alert_data.get("timestamp", datetime.now().isoformat()),
            "execution_id": alert_data.get("execution_id", ""),
            "check_id": alert_data.get("check_id", 0),
            "activity_name": alert_data.get("activity_name", "Unknown"),
            "url": alert_data.get("url", ""),
            "status": alert_data.get("status", "unknown"),  # success, failure, error
            "response_code": alert_data.get("response_code"),
            "response_time": alert_data.get("response_time", 0),
            "error_message": alert_data.get("error_message", ""),
            "source": source,
            "is_simulated": alert_data.get("is_simulated", False),
            "previous_status": alert_data.get("previous_status", "unknown"),
            "severity": alert_data.get("severity", 5),  # 1-10
            "retry_count": alert_data.get("retry_count", 0)
        }


class AlertAssessor:
    """Assess if alert is actionable"""
    
    def __init__(self, history_file: str = "alert_history.json"):
        self.history_file = history_file
        self.known_false_positives = self._load_false_positives()
        self.alert_frequency = defaultdict(list)
    
    def assess(self, alert: Dict) -> Dict:
        """
        Comprehensive assessment of alert
        
        Returns:
            Assessment dict with various checks
        """
        
        assessment = {
            "is_false_positive": self._check_false_positive(alert),
            "is_known_issue": self._check_known_issue(alert),
            "frequency_check": self._check_frequency(alert),
            "has_historical_context": self._has_historical_context(alert),
            "severity_score": self._calculate_severity(alert),
            "threshold_exceeded": self._check_threshold(alert)
        }
        
        return assessment
    
    def _check_false_positive(self, alert: Dict) -> bool:
        """Check if alert is known false positive"""
        
        # Maintenance window false positive
        if alert.get("is_simulated") and "maintenance" in alert.get("error_message", "").lower():
            return True
        
        # Expected failures on certain times
        try:
            timestamp = datetime.fromisoformat(alert["timestamp"])
            day = timestamp.weekday()  # 0=Monday, 6=Sunday
            hour = timestamp.hour
            
            # Known window: Sunday 22:00-23:59
            if day == 6 and 22 <= hour < 24:
                return True
        except:
            pass
        
        return False
    
    def _check_known_issue(self, alert: Dict) -> bool:
        """Check if it's a known recurring issue"""
        
        activity = alert["activity_name"]
        return activity in self.known_false_positives
    
    def _check_frequency(self, alert: Dict) -> Dict:
        """Check alert frequency/storm"""
        
        activity = alert["activity_name"]
        now = datetime.now()
        five_min_ago = now - timedelta(minutes=5)
        
        # Get alerts for this activity in last 5 minutes
        recent_alerts = [
            a for a in self.alert_frequency.get(activity, [])
            if datetime.fromisoformat(a["timestamp"]) > five_min_ago
        ]
        
        self.alert_frequency[activity].append(alert)
        
        return {
            "count_5_min": len(recent_alerts),
            "exceeded": len(recent_alerts) > 10,  # Threshold: >10 in 5 min
            "is_storm": len(recent_alerts) > 50
        }
    
    def _has_historical_context(self, alert: Dict) -> bool:
        """Check if we have historical data for this activity"""
        
        activity = alert["activity_name"]
        # In real system, would query database
        # For now, return True (assume we have context after first run)
        return True
    
    def _calculate_severity(self, alert: Dict) -> float:
        """Calculate severity score 0-10"""
        
        base_score = 5
        
        if alert["status"] == "failure":
            base_score += 3
        
        if alert["response_code"] and alert["response_code"] >= 500:
            base_score += 2
        elif alert["response_code"] and alert["response_code"] >= 400:
            base_score += 1
        
        if alert["response_time"] > 10:
            base_score += 1
        
        return min(10, base_score)
    
    def _check_threshold(self, alert: Dict) -> bool:
        """Check if alert exceeds threshold"""
        
        # Response time threshold
        if alert["response_time"] > 5000:  # 5 seconds
            return True
        
        # Response code threshold
        if alert["response_code"] and alert["response_code"] >= 500:
            return True
        
        # Failed status
        if alert["status"] in ["failure", "error"]:
            return True
        
        return False
    
    def _load_false_positives(self) -> Dict:
        """Load known false positives from config"""
        
        return {
            "License Check": ["tuesday 14:30"],
            "Test Activity": ["always"],
            "Maintenance Task": ["sunday 22-23"]
        }


class EventCorrelator:
    """Correlate related alerts"""
    
    def __init__(self, time_window: int = 300):  # 5 minutes default
        self.time_window = time_window
        self.correlation_groups = []
    
    def correlate(self, alerts: List[Dict]) -> List[Dict]:
        """
        Correlate related alerts into groups
        
        Args:
            alerts: List of normalized alerts
        
        Returns:
            List of correlated alert groups
        """
        
        if not alerts:
            return []
        
        groups = []
        processed = set()
        
        for i, alert in enumerate(alerts):
            if i in processed:
                continue
            
            group = [alert]
            processed.add(i)
            
            # Find related alerts
            for j, other_alert in enumerate(alerts):
                if j <= i or j in processed:
                    continue
                
                if self._are_correlated(alert, other_alert):
                    group.append(other_alert)
                    processed.add(j)
            
            groups.append({
                "group_id": f"group_{i}",
                "alerts": group,
                "count": len(group),
                "root_cause": self._infer_root_cause(group),
                "timestamp": datetime.now().isoformat()
            })
        
        return groups
    
    def _are_correlated(self, alert1: Dict, alert2: Dict) -> bool:
        """Check if two alerts are correlated"""
        
        # Same service/URL
        if alert1["activity_name"] == alert2["activity_name"]:
            return True
        
        # Same time window
        try:
            t1 = datetime.fromisoformat(alert1["timestamp"])
            t2 = datetime.fromisoformat(alert2["timestamp"])
            if abs((t1 - t2).total_seconds()) < self.time_window:
                # Duplicate alert
                if alert1["error_message"] == alert2["error_message"]:
                    return True
        except:
            pass
        
        # Cascade failure pattern
        if "network" in alert1.get("error_message", "").lower():
            if any(keyword in alert2.get("error_message", "").lower() 
                   for keyword in ["timeout", "connection", "refused"]):
                return True
        
        return False
    
    def _infer_root_cause(self, alert_group: List[Dict]) -> str:
        """Infer root cause from alert group"""
        
        error_messages = [a.get("error_message", "") for a in alert_group]
        
        if any("timeout" in msg.lower() for msg in error_messages):
            return "Network timeout or high latency"
        
        if any("connection" in msg.lower() for msg in error_messages):
            return "Connection/Connectivity issue"
        
        if any("503" in str(a.get("response_code", "")) for a in alert_group):
            return "Service unavailable"
        
        if any("500" in str(a.get("response_code", "")) for a in alert_group):
            return "Server error"
        
        if len(alert_group) > 5:
            return "Multiple service failures - possible cascading issue"
        
        return "Unknown cause"


class RuleEngine:
    """Apply rules to filter and process alerts"""
    
    def __init__(self, rules_config: Dict = None):
        self.rules = rules_config or self._get_default_rules()
    
    def apply_rules(self, alert: Dict, assessment: Dict) -> Dict:
        """
        Apply filtering rules to alert
        
        Returns:
            Dict with action and reasoning
        """
        
        # Rule 1: Suppress false positives
        if assessment["is_false_positive"]:
            return {
                "action": "SUPPRESS",
                "reason": "Known false positive",
                "should_create_ticket": False
            }
        
        # Rule 2: Suppress during maintenance
        try:
            timestamp = datetime.fromisoformat(alert["timestamp"])
            if timestamp.weekday() == 6 and 22 <= timestamp.hour < 24:
                return {
                    "action": "SUPPRESS",
                    "reason": "Maintenance window",
                    "should_create_ticket": False
                }
        except:
            pass
        
        # Rule 3: Suppress if frequency exceeded (deduplication)
        if assessment["frequency_check"]["is_storm"]:
            return {
                "action": "DEDUPLICATE",
                "reason": "Alert storm detected",
                "should_create_ticket": False
            }
        
        # Rule 4: Suppress low severity
        if assessment["severity_score"] < 2 and not alert.get("is_simulated"):
            return {
                "action": "SUPPRESS",
                "reason": "Low severity",
                "should_create_ticket": False
            }
        
        # Rule 5: Create ticket for actionable alerts
        return {
            "action": "ESCALATE",
            "reason": "Actionable alert",
            "should_create_ticket": True
        }
    
    def _get_default_rules(self) -> Dict:
        """Get default rule set"""
        return {
            "false_positive_suppression": True,
            "maintenance_window_suppression": True,
            "storm_deduplication": True,
            "low_severity_threshold": 2,
            "frequency_threshold_5min": 10
        }


class ActionabilityScorer:
    """Score alert actionability 0-100"""
    
    def __init__(self):
        self.critical_services = ["account-server", "transaction-server", "loan-server"]
        self.score_weights = {
            "base_failure": 30,
            "not_false_positive": 25,
            "frequency": 20,
            "severity": 15,
            "threshold_exceeded": 10
        }
    
    def calculate_score(self, alert: Dict, assessment: Dict) -> int:
        """
        Calculate actionability score 0-100
        
        Threshold: >60 = create ticket
        """
        
        score = 0
        
        # Base: failure detection
        if alert["status"] in ["failure", "error"]:
            score += self.score_weights["base_failure"]
        
        # Not a false positive
        if not assessment["is_false_positive"]:
            score += self.score_weights["not_false_positive"]
        
        # Frequency check passed (not storm)
        if not assessment["frequency_check"]["is_storm"]:
            score += self.score_weights["frequency"]
        
        # Severity contribution
        severity_points = (assessment["severity_score"] / 10) * self.score_weights["severity"]
        score += severity_points
        
        # Threshold exceeded
        if assessment["threshold_exceeded"]:
            score += self.score_weights["threshold_exceeded"]
        
        # Critical service boost
        if any(service in alert["url"].lower() for service in self.critical_services):
            score += 15
        
        # Simulated defects score lower
        if alert.get("is_simulated"):
            score -= 10
        
        # Clamp to 0-100
        score = max(0, min(100, score))
        
        return int(score)


class AlertEngine:
    """Main alert engine coordinating all components"""
    
    def __init__(self, rules_config: Dict = None):
        self.normalizer = AlertNormalizer()
        self.assessor = AlertAssessor()
        self.correlator = EventCorrelator()
        self.rule_engine = RuleEngine(rules_config)
        self.scorer = ActionabilityScorer()
        self.processed_alerts = []
    
    def process_alerts(self, raw_alerts: List[Dict]) -> Dict:
        """
        Process raw alerts into actionable tickets
        
        Args:
            raw_alerts: List of raw alert dicts
        
        Returns:
            Dict with results
        """
        
        # Step 1: Normalize
        normalized = [self.normalizer.normalize(alert) for alert in raw_alerts]
        
        # Step 2: Assess
        assessments = [self.assessor.assess(alert) for alert in normalized]
        
        # Step 3: Correlate
        correlated_groups = self.correlator.correlate(normalized)
        
        # Step 4: Score & Filter
        results = {
            "actionable_alerts": [],
            "suppressed_alerts": [],
            "deduplicated_alerts": [],
            "correlated_groups": correlated_groups,
            "timestamp": datetime.now().isoformat()
        }
        
        for alert, assessment in zip(normalized, assessments):
            # Apply rules
            rule_result = self.rule_engine.apply_rules(alert, assessment)
            
            # Calculate score
            score = self.scorer.calculate_score(alert, assessment)
            
            processed = {
                "alert": alert,
                "assessment": assessment,
                "rule_result": rule_result,
                "score": score,
                "should_create_ticket": rule_result["should_create_ticket"] and score > 60
            }
            
            # Categorize
            if rule_result["action"] == "SUPPRESS":
                results["suppressed_alerts"].append(processed)
            elif rule_result["action"] == "DEDUPLICATE":
                results["deduplicated_alerts"].append(processed)
            else:
                results["actionable_alerts"].append(processed)
            
            self.processed_alerts.append(processed)
        
        # Summary
        results["summary"] = {
            "total_alerts": len(normalized),
            "actionable": len(results["actionable_alerts"]),
            "suppressed": len(results["suppressed_alerts"]),
            "deduplicated": len(results["deduplicated_alerts"]),
            "tickets_to_create": sum(1 for a in results["actionable_alerts"] if a["should_create_ticket"])
        }
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get processing statistics"""
        
        if not self.processed_alerts:
            return {"message": "No alerts processed"}
        
        scores = [alert["score"] for alert in self.processed_alerts]
        
        return {
            "total_processed": len(self.processed_alerts),
            "avg_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "high_priority": sum(1 for s in scores if s > 75),
            "medium_priority": sum(1 for s in scores if 60 <= s <= 75),
            "low_priority": sum(1 for s in scores if s < 60)
        }
