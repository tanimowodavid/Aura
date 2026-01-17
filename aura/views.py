import json
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_view(request):
    """Render the chat interface"""
    # Initialize chat history in session if it doesn't exist
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
    
    return render(request, 'aura/chat.html', {
        'chat_history': request.session.get('chat_history', [])
    })

@csrf_exempt
@require_http_methods(["POST"])
def chat_stream(request):
    """Handle chat messages and stream OpenAI responses"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return StreamingHttpResponse(
                iter(['data: {"error": "Message cannot be empty"}\n\n']),
                content_type='text/event-stream'
            )
        
        # Get chat history from session
        chat_history = request.session.get('chat_history', [])
        
        # Add user message to history
        chat_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful, friendly AI assistant named Aura. Be concise, warm, and supportive in your responses."}
        ]
        messages.extend(chat_history)
        
        def generate():
            try:
                assistant_message = ""
                
                # Stream response from OpenAI
                stream = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    stream=True,
                    temperature=0.7
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        assistant_message += content
                        yield f"data: {json.dumps({'content': content})}\n\n"
                
                # Add assistant message to history
                chat_history.append({
                    'role': 'assistant',
                    'content': assistant_message
                })
                
                # Save updated history to session
                request.session['chat_history'] = chat_history
                request.session.modified = True
                
                yield f"data: {json.dumps({'done': True})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'error': 'I apologize, but I encountered an issue. Please try again in a moment.'})}\n\n"
        
        return StreamingHttpResponse(
            generate(),
            content_type='text/event-stream'
        )
        
    except Exception as e:
        return StreamingHttpResponse(
            iter([f'data: {json.dumps({"error": "Something went wrong. Please refresh and try again."})}\n\n']),
            content_type='text/event-stream'
        )

@csrf_exempt
@require_http_methods(["POST"])
def clear_chat(request):
    """Clear chat history"""
    request.session['chat_history'] = []
    request.session.modified = True
    return StreamingHttpResponse(
        iter([json.dumps({'success': True})]),
        content_type='application/json'
    )