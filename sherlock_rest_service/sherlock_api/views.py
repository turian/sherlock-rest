from django.http import JsonResponse
from rest_framework.decorators import api_view
from sherlock import run_sherlock

@api_view(['GET'])
def sherlock_api(request):
    # Get the necessary arguments from the request
    arguments = []  # Populate this list with the required arguments

    # Call the run_sherlock function with the arguments
    results = run_sherlock(arguments)

    # Return the results as a JSON response
    return JsonResponse(results, safe=False)
