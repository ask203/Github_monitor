import time
import threading
from .utils import get_events, filter_events, calculate_avg_time_between_events
from .config import github_token , interval, repos
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


REPOS = repos
GITHUB_TOKEN = github_token

COMPUTED_DATA = {
    'avg_time_between_events': {},
    'event_counts': {}
}

scheduler_running = False
# Acquires event data from repos
def update_data():
    if len(REPOS) > 5:
        raise ValueError("The number of repositories exceeds the limit of 5.")
    
    all_events = []
    for repo in REPOS:
        logger.debug(f"Updating data for repo: {repo}")
        owner, repo_name = repo.split('/')
        events = get_events(owner, repo_name, GITHUB_TOKEN)
        for event in events:
            event['repo'] = repo
        all_events.extend(events)

    df = filter_events(all_events)
    avg_time_between_events = calculate_avg_time_between_events(df)
    
    COMPUTED_DATA['avg_time_between_events'] = avg_time_between_events
    COMPUTED_DATA['events_df'] = df  
    logger.debug("finished updating data")

def run_scheduler(interval=interval):  
    while True:
        update_data()
        time.sleep(interval)

# Start the scheduler in a separate thread
def start_scheduler():
    global scheduler_running
    if scheduler_running:
        logger.debug("Scheduler already running. Skipping start.")
        return
    
    logger.debug("Starting scheduler")
    scheduler_thread = threading.Thread(target=run_scheduler, args=(interval,))
    scheduler_thread.daemon = True
    scheduler_thread.start()
    scheduler_running = True
