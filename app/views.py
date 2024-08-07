from flask import Blueprint, jsonify, request, url_for
from datetime import datetime, timedelta
import pytz
from .scheduler import COMPUTED_DATA as cd
from collections import defaultdict
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    statistics_url = url_for('main.statistics', _external=True)
    event_count_url = url_for('main.event_count', _external=True)
    return jsonify({
        'statistics': statistics_url,
        'event_count': event_count_url
    })


@main.route('/statistics', methods=['GET'])
def statistics():
    return jsonify(cd['avg_time_between_events'])

@main.route('/event_count', methods=['GET'])
def event_count():
    offset_minutes = int(request.args.get('offset', 100))
    offset_time = datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(minutes=offset_minutes)
    
    # Access the DataFrame from computed_data
    df = cd.get('events_df')
    
    if df is None:
        return jsonify({"error": "No data available"}), 500
    
    # Filter the required offset from the data
    df['created_at'] = pd.to_datetime(df['created_at'])
    filtered_events = df[df['created_at'] > offset_time]
    aggregated_counts = filtered_events.groupby(['repo', 'type']).size().reset_index(name='count')
    
    all_repos = df['repo'].unique()
    all_event_types = df['type'].unique()
    
    repo_event_counts = {}
    
    # Initialize all repos and event types with 0 count
    for repo in all_repos:
        repo_event_counts[repo] = {"name": repo, "events": {event_type: 0 for event_type in all_event_types}}
    
    # Populate counts from aggregated data
    for _, row in aggregated_counts.iterrows():
        repo = row['repo']
        event_type = row['type']
        count = row['count']
        repo_event_counts[repo]['events'][event_type] = count
    
    # Final output
    filtered_event_counts = {
        "repo": [
            {
                "name": repo_data["name"],
                "event": repo_data["events"]
            } for repo_data in repo_event_counts.values()
        ]
    }
    
    return jsonify(filtered_event_counts)