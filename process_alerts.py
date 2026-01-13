"""
Alert Processing Script
Processes raw alerts through the alert engine
"""

import json
import os
from datetime import datetime
from alert_engine import AlertEngine
from database import AlertDatabase
from utils import Logger, DataProcessor


def main():
    """Process alerts from the health check"""
    
    logger = Logger()
    logger.info("=" * 60)
    logger.info("🔄 Starting Alert Engine Processing")
    logger.info("=" * 60)
    
    # Load raw alerts
    if not os.path.exists("raw_alerts.json"):
        logger.error("raw_alerts.json not found. Run health check first.")
        return
    
    with open("raw_alerts.json", "r") as f:
        raw_alerts = json.load(f)
    
    logger.info(f"📥 Loaded {len(raw_alerts)} raw alerts")
    
    # Initialize engine
    engine = AlertEngine()
    db = AlertDatabase()
    
    # Process alerts
    logger.info("⚙️  Processing alerts through engine...")
    results = engine.process_alerts(raw_alerts)
    
    # Log results
    logger.info(f"✓ Alert Engine Results:")
    logger.info(f"  ├─ Total Alerts: {results['summary']['total_alerts']}")
    logger.info(f"  ├─ Actionable: {results['summary']['actionable']}")
    logger.info(f"  ├─ Suppressed: {results['summary']['suppressed']}")
    logger.info(f"  ├─ Deduplicated: {results['summary']['deduplicated']}")
    logger.info(f"  └─ Tickets to Create: {results['summary']['tickets_to_create']}")
    
    # Log correlated groups
    if results['correlated_groups']:
        logger.info(f"🔗 Correlated Alert Groups:")
        for group in results['correlated_groups']:
            logger.info(f"  ├─ Group {group['group_id']}: {group['count']} alerts")
            logger.info(f"  │   └─ Root Cause: {group['root_cause']}")
    
    # Categorize and display alerts
    logger.info(f"\n📊 Actionable Alerts ({len(results['actionable_alerts'])}):")
    for alert in results['actionable_alerts'][:5]:  # Show first 5
        activity = alert['alert']['activity_name']
        score = alert['score']
        status = alert['alert']['status']
        logger.info(f"  ├─ {activity}: {status.upper()} (Score: {score})")
    
    if len(results['actionable_alerts']) > 5:
        logger.info(f"  └─ ... and {len(results['actionable_alerts']) - 5} more")
    
    # Save processed results
    logger.info(f"\n💾 Saving processed results...")
    
    with open("alert_engine_results.json", "w") as f:
        # Serialize for JSON (remove datetime objects if any)
        json_safe_results = json.dumps(results, default=str, indent=2)
        f.write(json_safe_results)
    
    logger.info(f"  ├─ Alert engine results: ✓")
    
    # Save actionable alerts for ticket creation
    actionable_alerts = [
        alert for alert in results['actionable_alerts']
        if alert['should_create_ticket']
    ]
    
    with open("actionable_alerts.json", "w") as f:
        json.dump(actionable_alerts, f, default=str, indent=2)
    
    logger.info(f"  ├─ Actionable alerts: ✓ ({len(actionable_alerts)} tickets to create)")
    
    # Statistics
    logger.info(f"\n📈 Engine Statistics:")
    stats = engine.get_statistics()
    logger.info(f"  ├─ Average Score: {stats['avg_score']:.1f}/100")
    logger.info(f"  ├─ High Priority (>75): {stats['high_priority']}")
    logger.info(f"  ├─ Medium Priority (60-75): {stats['medium_priority']}")
    logger.info(f"  └─ Low Priority (<60): {stats['low_priority']}")
    
    # Data insights
    logger.info(f"\n🔍 Alert Insights:")
    insights = DataProcessor.extract_insights(raw_alerts)
    logger.info(f"  ├─ Most Common Error: {insights.get('most_common_error', 'N/A')[:50]}")
    logger.info(f"  ├─ Most Affected Activity: {insights.get('most_affected_activity', 'N/A')}")
    logger.info(f"  ├─ Failure Rate: {insights['failure_rate']:.1f}%")
    logger.info(f"  └─ Pattern: {insights['pattern']}")
    
    logger.info(f"\n✅ Alert processing completed at {datetime.now().isoformat()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
