import json
import requests
import os

def lambda_handler(event, context):
    try:
        # Assuming the payload is in the 'body' of the input event
        payload = json.loads(event['body'])
        issue_url = payload.get('issue', {}).get('html_url', '')
        
        print(f'Issue URL: {issue_url}')  # Log the issue URL

        # Send message to Slack
        slack_url = os.environ.get('SLACK_URL', '')
        if slack_url:
            slack_payload = {'text': f'Issue Created: {issue_url}'}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(slack_url, data=json.dumps(slack_payload), headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            
            print(f'Slack Response: {response.text}')  # Log the Slack response
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('SLACK_URL environment variable not set')
            }
        
        # Return issue URL in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'issue_url': issue_url, 'message': 'Slack notification sent!'})
        }
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {str(e)}')  # Log JSON decoding error
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error decoding JSON: {str(e)}')
        }
    except requests.RequestException as e:
        print(f'Request to Slack failed: {str(e)}')  # Log Slack request error
        return {
            'statusCode': 500,
            'body': json.dumps(f'Request to Slack failed: {str(e)}')
        }
    except Exception as e:
        print(f'Unexpected error: {str(e)}')  # Log unexpected error
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal Server Error: {str(e)}')
        }
