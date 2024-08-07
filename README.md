
# GitHub Monitoring Application

## Overview

This application monitors activities happening on specified GitHub repositories and provides statistics via a REST API. The statistics are based on a rolling window of either 7 days or 500 events, whichever is less. 

### Features

- Monitors up to five configurable GitHub repositories.
- Provides statistics on the average time between consecutive events for each combination of event type and repository name.
- Returns the total number of events grouped by event type and repository name for a given time offset.
- Updates data every 5 minutes(configurable) in the background to ensure quick response times for API requests.

## Assumptions

- The application will monitor a fixed list of up to five repositories.
- GitHub's API rate limits are respected, and a GitHub token with sufficient permissions is provided.
- The system's time zone is UTC.

## Requirements

- Python 3.6+
- Virtual environment tool (e.g., `venv`)
- GitHub personal access token with `repo` scope. For token generating details click [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)


## Run Locally

#### 1 - Clone the project

```bash
  git clone https://github.com/ask203/github_monitor.git
```
#### 2 - Create a Virtual Environment
```bash
  python3 -m venv venv
  source venv/bin/activate
```
####  3 - Go to the project directory

```bash
  cd github_monitor
```

#### 4 - Install dependencies

```bash
  pip install -r requirements.txt
```

#### 5 - Set Up Environment Variables

Create a .env file in the root directory and add your GitHub token

```bash
  GITHUB_TOKEN=your_github_token
```
#### 6 - Configure Repositories and Interval

Edit the config.py file to specify the repositories and the interval for updating data
You can list the repositories(max 5) you want to track by adding them to the `repos` list in the format `'owner/repository_name'`. For example:

```python

repos = [
    'owner_1/name_1',
    'owner_2/name_2',
    'owner_3/name_3',
    'owner_4/name_4',
    'owner_5/name_5'
]

interval = 300
```

7 - Run the Application

```bash
  python run.py
```



## API Reference

### Endpoints

#### 1 - '/statistics'
- Method: GET

- Description: Fetches the average time between consecutive events for each combination of event type and repository name.

- Response: JSON object containing average time in seconds.

Example Request:

```sh
  curl http://127.0.0.1:5000/statistics
```
Example Response:

```json
{
    "repo": [
        {
            "event": {
                "IssuesEvent": 1032.4,
                "PullRequestEvent": 1764.4,
                "WatchEvent": 1431.3
            },
            "name": "microsoft/vscode"
        },
        {
            "event": {
                "IssuesEvent": 17613,
                "PullRequestEvent": 650.9,
                "WatchEvent": 2231.2
            },
            "name": "tensorflow/tensorflow"
        }
    ]
}
```

#### 2 - '/event_count'

- Method: GET

- Description: Fetches the total number of events grouped by the event type and repository name for a given offset.

- Query Parameters:

| Parameter | Type     | Description                                        |
| :-------- | :------- | :------------------------------------------------- |
| `offset`  |   `int`  | Number of minutes to look back for counting events |

Example Request:

```sh
curl http://127.0.0.1:5000/event_count?offset=1000
``` 
or without offset, which sets it to 100

```sh
curl http://127.0.0.1:5000/event_count
```
Example Response:

```json
{
    "repo": [
        {
            "event": {
                "IssuesEvent": 37,
                "PullRequestEvent": 23,
                "WatchEvent": 26
            },
            "name": "microsoft/vscode"
        },
        {
            "event": {
                "IssuesEvent": 2,
                "PullRequestEvent": 42,
                "WatchEvent": 12
            },
            "name": "tensorflow/tensorflow"
        }
    ]
}
```
