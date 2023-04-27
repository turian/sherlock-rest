from django.http import JsonResponse
from rest_framework.decorators import api_view
from sherlock import run_sherlock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_sherlock_api(request):
    # Get the necessary arguments from the request
    arguments = []  # Populate this list with the required arguments

    # Call the run_sherlock function with the arguments
    results = run_sherlock(arguments)
    if request.method == 'POST':
        # Your view logic here
        return JsonResponse({"result": "success"})
    # Return the results as a JSON response
    return JsonResponse(results, safe=False)

    return JsonResponse({"detail": "Method not allowed."}, status=405)
