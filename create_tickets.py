"""
Ticket Creation Script
Creates GitHub Issues from actionable alerts
"""

import json
import os
from datetime import datetime
from ticket_generator import GitHubTicketGenerator, TicketTracker
from utils import Logger


def main():
    """Create tickets from actionable alerts"""
    
    logger = Logger()
    logger.info("=" * 60)
    logger.info("🎫 Creating GitHub Issues from Actionable Alerts")
    logger.info("=" * 60)
    
    # Load actionable alerts
    if not os.path.exists("actionable_alerts.json"):
        logger.warning("actionable_alerts.json not found. No tickets to create.")
        return
    
    with open("actionable_alerts.json", "r") as f:
        actionable_alerts = json.load(f)
    
    logger.info(f"📥 Loaded {len(actionable_alerts)} actionable alerts")
    
    # Initialize generator
    generator = GitHubTicketGenerator()
    tracker = TicketTracker()
    
    logger.info(f"\n🔧 Configuration:")
    logger.info(f"  ├─ GitHub Token: {'✓ Set' if not generator.dry_run else '✗ Not set (dry-run)'}")
    logger.info(f"  ├─ Repository: {generator.repo_owner}/{generator.repo_name}")
    logger.info(f"  └─ Dry Run: {'✓ Yes' if generator.dry_run else '✗ No'}")
    
    # Create tickets
    logger.info(f"\n▶️  Creating tickets...")
    logger.info("=" * 60)
    
    created_tickets = []
    for i, alert in enumerate(actionable_alerts, 1):
        ticket = generator.create_ticket(alert)
        if ticket:
            created_tickets.append(ticket)
            tracker.track_ticket(ticket)
            logger.info(f"  {i}. ✓ {alert['alert']['activity_name']} (Score: {alert['score']})")
    
    logger.info("=" * 60)
    logger.info(f"\n✅ Tickets Created: {len(created_tickets)}/{len(actionable_alerts)}")
    
    # Save summary
    summary = generator.get_created_tickets_summary()
    
    with open("ticket_summary.json", "w") as f:
        json.dump(summary, f, default=str, indent=2)
    
    logger.info(f"\n📊 Ticket Summary:")
    logger.info(f"  ├─ Total Created: {summary['total_created']}")
    logger.info(f"  ├─ Critical (>85): {summary['critical']}")
    logger.info(f"  ├─ High (70-85): {summary['high']}")
    logger.info(f"  ├─ Medium (<70): {summary['medium']}")
    logger.info(f"  ├─ Test Defects: {summary['test_defects']}")
    logger.info(f"  └─ Production: {summary['production']}")
    
    if created_tickets:
        logger.info(f"\n🔗 Created Issues:")
        for ticket in created_tickets[:5]:
            issue_num = ticket.get("issue_number", "dry-run")
            logger.info(f"  ├─ #{issue_num}: {ticket['activity']}")
        
        if len(created_tickets) > 5:
            logger.info(f"  └─ ... and {len(created_tickets) - 5} more")
    
    # Open issues
    open_tickets = tracker.get_open_tickets()
    logger.info(f"\n📋 Open Tickets: {len(open_tickets)}")
    
    logger.info(f"\n✅ Ticket creation completed at {datetime.now().isoformat()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
