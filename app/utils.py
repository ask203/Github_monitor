import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
import logging

logger = logging.getLogger()

# Fetches all the events of the repos from Github API
def get_events(owner, repo, token):
    url = f'https://api.github.com/repos/{owner}/{repo}/events'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}'
    }

    events = []
    page = 1
    while len(events) < 500:  # Limit to 500 events
        try:
            logger.debug(f"Obtaining data from {owner}/{repo} : page - {page}")
            response = requests.get(url, headers=headers, params={'page': page})
            response.raise_for_status()
            page_events = response.json()
            if not page_events:
                break
            events.extend(page_events)
            page += 1
        except requests.exceptions.HTTPError as e:
            if response.status_code == 422:
                logger.debug("Reached the end of available event pages.")
                break
            else:
                raise e

    return events

# Filters the first 500 events or the recent events from the last 7 days, whichever is less
def filter_events(events):

    logger.debug(f"Filtering events from {events}")
   
    df = pd.DataFrame(events)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[df['type'].isin(['WatchEvent', 'PullRequestEvent', 'IssuesEvent'])]
    df = df.sort_values(by='created_at', ascending=False)
    
    last_7_days = datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=7)
    recent_events = df[df['created_at'] > last_7_days]
    filtered_events = recent_events.head(500) if len(recent_events) > 500 else recent_events

    logger.debug(f"Filtering events completed")

    return filtered_events

# Calculates the average time between consecutive events, separately for each combination of event type and repository name.
def calculate_avg_time_between_events(df):
    result = {}
    logger.debug(f"Average time between events are calculated")

    for (repo, event_type), group in df.groupby(['repo', 'type']):
        group = group.sort_values(by='created_at')
        time_diffs = group['created_at'].diff().dropna()
        avg_time_diff = time_diffs.mean().total_seconds() 
        if repo not in result:
            result[repo] = {}
        result[repo][event_type] = round(avg_time_diff, 1)
    
    formatted_output = {"repo": []}

    for repo, events in result.items():
        formatted_output["repo"].append({
            "name": repo,
            "event": events
        })
    
    return formatted_output

