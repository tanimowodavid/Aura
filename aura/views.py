import json
from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from finance.models import FinancialProfile, CheckIn, FinanceHistory
from aura.service.prompts import ONBOARDING_FUNCTIONS, CHECKIN_FUNCTIONS, onboarding_system_prompt, checkin_system_prompt
from openai import OpenAI


client = OpenAI()



@login_required
def onboarding_view(request):
    """Onboarding chat interface"""
    if 'onboarding_chat_history' not in request.session:
        request.session['onboarding_chat_history'] = []
    
    return render(request, 'aura/onboarding.html', {
        'chat_history': request.session.get('onboarding_chat_history', [])
    })


@login_required
def checkin_view(request):
    """Check-in chat interface"""
    if 'checkin_chat_history' not in request.session:
        request.session['checkin_chat_history'] = []
    
    try:
        profile = request.user.financial_profile
        last_checkin = request.user.checkins.first()
        
        return render(request, 'aura/checkin.html', {
            'chat_history': request.session.get('checkin_chat_history', []),
            'profile': profile,
            'last_checkin': last_checkin
        })
    except FinancialProfile.DoesNotExist:
        return redirect('aura:onboarding')


def calculate_next_checkin(user):
    """Calculate next check-in date based on frequency"""
    frequency_map = {
        'daily': 1,
        'twice_weekly': 3,
        'weekly': 7,
        'biweekly': 14,
        'monthly': 30
    }
    days = frequency_map.get(user.check_in_frequency, 7)
    return timezone.now() + timedelta(days=days)






@csrf_exempt
@require_http_methods(["POST"])
@login_required
def onboarding_stream(request):
    """Handle onboarding chat with function calling"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return StreamingHttpResponse(
                iter(['data: {"error": "Message cannot be empty"}\n\n'.encode()]),
                content_type='text/event-stream'
            )
        
        chat_history = request.session.get('onboarding_chat_history', [])
        chat_history.append({'role': 'user', 'content': user_message})
        
        system_prompt = onboarding_system_prompt(request.user)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(chat_history)
        
        def generate():
            try:
                assistant_message = ""
                function_call_data = None
                
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    functions=ONBOARDING_FUNCTIONS,
                    function_call="auto",
                    stream=True,
                    temperature=0.7,
                )
                
                
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    
                    # Handle function call
                    if delta.function_call:
                        if not function_call_data:
                            function_call_data = {'name': '', 'arguments': ''}
                        if delta.function_call.name:
                            function_call_data['name'] = delta.function_call.name
                        if delta.function_call.arguments:
                            function_call_data['arguments'] += delta.function_call.arguments
                    
                    # Handle regular content
                    if delta.content:
                        assistant_message += delta.content
                        yield f"data: {json.dumps({'content': delta.content})}\n\n".encode()
                
                # Process function call if present
                if function_call_data and function_call_data['name'] == 'complete_onboarding':
                    args = json.loads(function_call_data['arguments'])
                    
                    # Create financial profile
                    profile, created = FinancialProfile.objects.get_or_create(
                        user=request.user,
                        defaults={
                            'estimated_balance': Decimal(str(args['estimated_balance'])),
                            'primary_goal': args['primary_goal'],
                            'financial_context': args.get('financial_context', {})
                        }
                    )
                    
                    if not created:
                        profile.estimated_balance = Decimal(str(args['estimated_balance']))
                        profile.primary_goal = args['primary_goal']
                        profile.financial_context.update(args.get('financial_context', {}))
                        profile.save()
                    
                    # Create initial history entry
                    FinanceHistory.objects.create(
                        profile=profile,
                        estimated_total=Decimal(str(args['estimated_balance']))
                    )
                    
                    # Update user
                    request.user.next_check_in_at = calculate_next_checkin(request.user)
                    request.user.is_onboarded = True
                    request.user.save()
                    
                    # Clear session
                    request.session['onboarding_chat_history'] = []
                    request.session.modified = True
                    
                    yield f"data: {json.dumps({'onboarding_complete': True})}\n\n".encode()
                else:
                    # Save chat history
                    chat_history.append({'role': 'assistant', 'content': assistant_message})
                    request.session['onboarding_chat_history'] = chat_history
                    request.session.modified = True
                
                yield f"data: {json.dumps({'done': True})}\n\n".encode()
                
            except Exception as e:
                yield f"data: {json.dumps({'error': 'I apologize, but I encountered an issue. Please try again.'})}\n\n".encode()
        
        return StreamingHttpResponse(generate(), content_type='text/event-stream')
        
    except Exception as e:
        return StreamingHttpResponse(
            iter([f'data: {json.dumps({"error": "Something went wrong. Please refresh and try again."})}\n\n'.encode()]),
            content_type='text/event-stream'
        )


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def checkin_stream(request):
    """Handle check-in chat with function calling"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return StreamingHttpResponse(
                iter(['data: {"error": "Message cannot be empty"}\n\n'.encode()]),
                content_type='text/event-stream'
            )
        
        profile = request.user.financial_profile
        last_checkin = request.user.checkins.first()
        
        chat_history = request.session.get('checkin_chat_history', [])
        chat_history.append({'role': 'user', 'content': user_message})
        
        system_prompt = checkin_system_prompt(request.user)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(chat_history)
        
        def generate():
            try:
                assistant_message = ""
                function_call_data = None
                
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    functions=CHECKIN_FUNCTIONS,
                    function_call="auto",
                    stream=True,
                    temperature=0.7
                )
                
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    
                    if delta.function_call:
                        if not function_call_data:
                            function_call_data = {'name': '', 'arguments': ''}
                        if delta.function_call.name:
                            function_call_data['name'] = delta.function_call.name
                        if delta.function_call.arguments:
                            function_call_data['arguments'] += delta.function_call.arguments
                    
                    if delta.content:
                        assistant_message += delta.content
                        yield f"data: {json.dumps({'content': delta.content})}\n\n".encode()
                
                if function_call_data and function_call_data['name'] == 'save_checkin':
                    args = json.loads(function_call_data['arguments'])
                    
                    # Create check-in record
                    CheckIn.objects.create(
                        user=request.user,
                        estimated_balance=Decimal(str(args['estimated_balance'])),
                        user_update=args.get('user_update', {}),
                        summary=args['summary'],
                        advice=args['advice'],
                        focus_until_next=args['focus_until_next'],
                        confidence_score=args.get('confidence_score', 80)
                    )
                    
                    # Update profile
                    profile.estimated_balance = Decimal(str(args['estimated_balance']))
                    if args.get('financial_context_updates'):
                        profile.financial_context.update(args['financial_context_updates'])
                    profile.save()
                    
                    # Add to history
                    FinanceHistory.objects.create(
                        profile=profile,
                        estimated_total=Decimal(str(args['estimated_balance']))
                    )
                    
                    # Update next check-in
                    request.user.next_check_in_at = calculate_next_checkin(request.user)
                    request.user.save()
                    
                    # Clear session
                    request.session['checkin_chat_history'] = []
                    request.session.modified = True
                    
                    yield f"data: {json.dumps({'checkin_complete': True})}\n\n".encode()
                else:
                    chat_history.append({'role': 'assistant', 'content': assistant_message})
                    request.session['checkin_chat_history'] = chat_history
                    request.session.modified = True
                
                yield f"data: {json.dumps({'done': True})}\n\n".encode()
                
            except Exception as e:
                yield f"data: {json.dumps({'error': 'I apologize, but I encountered an issue. Please try again.'})}\n\n".encode()
        
        return StreamingHttpResponse(generate(), content_type='text/event-stream')
        
    except Exception as e:
        return StreamingHttpResponse(
            iter([f'data: {json.dumps({"error": "Something went wrong. Please refresh and try again."})}\n\n'.encode()]),
            content_type='text/event-stream'
        )