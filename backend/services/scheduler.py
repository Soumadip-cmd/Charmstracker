"""
Background Task Scheduler for CharmTracker
Automatically updates charm data on schedule
"""

import asyncio
import logging
from datetime import datetime, time
from typing import Optional
import os

from services.data_aggregator import DataAggregator

logger = logging.getLogger(__name__)


class BackgroundScheduler:
    """Manages scheduled background tasks"""
    
    def __init__(self, db):
        self.db = db
        self.aggregator = DataAggregator(db)
        self.running = False
        self.task = None
        
        # Configuration
        self.update_interval_hours = int(os.getenv('UPDATE_INTERVAL_HOURS', '6'))
        self.update_time = os.getenv('UPDATE_TIME', '02:00')  # Default 2 AM
        self.batch_size = int(os.getenv('UPDATE_BATCH_SIZE', '10'))
    
    async def start(self):
        """Start the background scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._run_scheduler())
        logger.info("Background scheduler started")
    
    async def stop(self):
        """Stop the background scheduler"""
        if not self.running:
            return
        
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        logger.info("Background scheduler stopped")
    
    async def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                await self._update_cycle()
                
                # Wait for next update interval
                await asyncio.sleep(self.update_interval_hours * 3600)
                
            except asyncio.CancelledError:
                logger.info("Scheduler task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                # Wait before retrying
                await asyncio.sleep(300)  # 5 minutes
    
    async def _update_cycle(self):
        """Run a complete update cycle"""
        try:
            logger.info("Starting scheduled update cycle")
            start_time = datetime.utcnow()
            
            # Get charms that need updating (oldest first)
            charms = await self.db.charms.find().sort("last_updated", 1).to_list(1000)
            
            total_charms = len(charms)
            logger.info(f"Found {total_charms} charms to update")
            
            # Update in batches
            success_count = 0
            fail_count = 0
            
            for i in range(0, total_charms, self.batch_size):
                batch = charms[i:i + self.batch_size]
                
                logger.info(f"Processing batch {i//self.batch_size + 1}")
                
                # Update batch in parallel
                tasks = [
                    self.aggregator.update_charm_data(charm['id'])
                    for charm in batch
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, Exception):
                        fail_count += 1
                    elif result:
                        success_count += 1
                    else:
                        fail_count += 1
                
                # Rate limiting between batches
                if i + self.batch_size < total_charms:
                    await asyncio.sleep(10)  # 10 seconds between batches
            
            # Log results
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(
                f"Update cycle complete: {success_count} success, "
                f"{fail_count} failed in {duration:.1f}s"
            )
            
            # Store update statistics
            await self.db.update_stats.insert_one({
                "started_at": start_time,
                "completed_at": datetime.utcnow(),
                "duration_seconds": duration,
                "total_charms": total_charms,
                "success_count": success_count,
                "fail_count": fail_count
            })
            
        except Exception as e:
            logger.error(f"Error in update cycle: {str(e)}")
    
    async def trigger_immediate_update(self, charm_id: Optional[str] = None):
        """Trigger an immediate update outside the schedule"""
        try:
            if charm_id:
                logger.info(f"Triggering immediate update for charm {charm_id}")
                success = await self.aggregator.update_charm_data(charm_id)
                return {"success": success, "charm_id": charm_id}
            else:
                logger.info("Triggering immediate update for all charms")
                stats = await self.aggregator.update_all_charms()
                return stats
                
        except Exception as e:
            logger.error(f"Error in immediate update: {str(e)}")
            return {"success": False, "error": str(e)}


# Global scheduler instance
_scheduler_instance: Optional[BackgroundScheduler] = None


def get_scheduler(db) -> BackgroundScheduler:
    """Get or create scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = BackgroundScheduler(db)
    return _scheduler_instance


async def start_scheduler(db):
    """Start the global scheduler"""
    scheduler = get_scheduler(db)
    await scheduler.start()


async def stop_scheduler():
    """Stop the global scheduler"""
    if _scheduler_instance:
        await _scheduler_instance.stop()