import google
import google.auth.transport.requests
import gradio as gr
import os
import requests

settings = {
    'PROJECT_ID': os.environ['PROJECT_ID'],
    'REGION': os.environ.get('REGION', 'us-central1'),
}

settings.update(
    {
        'API_ENDPOINT': '{region}-aiplatform.googleapis.com'.format(
            region=settings['REGION']
        ),
        'MODEL_ID': 'gemini-2.0-flash-exp',
        'GENERATE_CONTENT_API': 'generateContent',
    }
)

def greet(name, intensity):
    output_ = generate_content(name)    
    return output_

def generate_content(prompt: str):
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
        , "systemInstruction" :{
            "parts": [
                {
                    "text": "なるだけ短く簡潔に回答してください。日本語でいうと100文字程度が目安です。"
                }
            ]
        }
        , "generationConfig": {
            "responseModalities": ["TEXT"]
            ,"temperature": 1
            ,"maxOutputTokens": 8192
            ,"topP": 0.95
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "OFF"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "OFF"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "OFF"
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "OFF"
            },
        ]
    }

    url = 'https://{api_endpoint}/v1/projects/{project_id}/locations/{region}/publishers/google/models/{model_id}:{generate_content_api}'.format(
        api_endpoint=settings['API_ENDPOINT'],
        project_id=settings['PROJECT_ID'],
        region=settings['REGION'],
        model_id=settings['MODEL_ID'],
        generate_content_api=settings['GENERATE_CONTENT_API']
    )

    token = _retreive_token()
    headers = {
        "Authorization": "Bearer {token}".format(token=token),
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
    )
    dict_ = response.json()
    return dict_['candidates'][0]['content']['parts'][0]['text']


def _retreive_token():
    credentials, project_id = google.auth.default()
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token



demo = gr.ChatInterface(
    fn=greet,
    type="messages",
     css="footer {visibility: hidden}"
)

demo.launch()