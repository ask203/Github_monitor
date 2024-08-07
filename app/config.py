from dotenv import load_dotenv
import os

load_dotenv()

#List up to 5 repositories in the format '{owner}/{repo}'
repos = [
    'tensorflow/tensorflow',
    'microsoft/vscode',
    'facebook/react',
    'torvalds/linux',
    'apple/swift',
]

github_token = os.getenv('GITHUB_TOKEN')

#Specify interval for updating data  in seconds
interval = 300 