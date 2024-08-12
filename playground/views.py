import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Deal, User, DealParticipant
import json

@csrf_exempt
def create_deal(request):
    print('create_deal endpoint hit')
    if request.method == 'POST':
        try:
            print('POST request received')
            user, created = User.objects.get_or_create(telegram_id=1)  # Упрощенное создание пользователя для тестирования
            deal = Deal.objects.create(creator=user, code=str(uuid.uuid4()))
            print(f'Deal created with ID: {deal.id}, Code: {deal.code}')
            return JsonResponse({'deal_id': deal.id, 'code': deal.code})
        except Exception as e:
            print(f'Error creating deal: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    print('Invalid request method')
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def join_deal(request):
    print('join_deal endpoint hit')
    if request.method == 'POST':
        try:
            print('POST request received')
            data = json.loads(request.body)
            code = data.get('code')
            user_id = data.get('user_id')

            try:
                deal = Deal.objects.get(code=code)
            except Deal.DoesNotExist:
                return JsonResponse({'error': 'Deal not found'}, status=404)

            user, created = User.objects.get_or_create(telegram_id=user_id)
            DealParticipant.objects.create(deal=deal, user=user, role='participant')
            print(f'User {user.id} joined deal {deal.id}')
            return JsonResponse({'deal_id': deal.id})
        except Exception as e:
            print(f'Error joining deal: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    print('Invalid request method')
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_user_deals(request):
    print('get_user_deals endpoint hit')
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            user = User.objects.get(telegram_id=user_id)

            # Получение сделок, где пользователь является создателем или участником
            deals = Deal.objects.filter(
                Q(creator=user) | Q(participants__user=user),
                status='created'
            ).distinct()

            deals_data = [{'id': deal.id, 'code': deal.code, 'status': deal.status} for deal in deals]

            return JsonResponse({'deals': deals_data})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            print(f'Error getting user deals: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    print('Invalid request method')
    return JsonResponse({'error': 'Invalid request method'}, status=400)
