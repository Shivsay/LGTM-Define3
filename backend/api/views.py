from django.shortcuts import render
from django.http import HttpResponse

def example_view(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def aircraft_post_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            name = data.get('name')
            email = data.get('email')

            # Process the data (e.g., save to the database, etc.)
            # For example, you could create a User instance here

            # Return a success response
            return JsonResponse({'message': 'Data received', 'name': name, 'email': email}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

