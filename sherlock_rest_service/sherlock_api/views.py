from django.http import JsonResponse
from rest_framework.decorators import api_view
from sherlock import run_sherlock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from sherlock import run_sherlock

# TODO: Check for extra args?
@csrf_exempt
def run_sherlock_api(request):
    if request.method == 'POST':
        # Parse JSON data received from the client
        data = json.loads(request.body)
        
        # Extract necessary arguments from the data
        usernames = data.get('usernames', [])
        csv = data.get('csv', False)

        # Prepare a list of arguments to pass to the run_sherlock function
        arguments = []
        
        # Add --csv flag if necessary
        if csv:
            arguments.append('--csv')

        # Add usernames to the arguments list
        arguments.extend(usernames)

        # Extract site_list from the data
        site_list = data.get('site_list', ["reddit", "twitter"])

        # Add site_list to the arguments list
        for site in site_list:
            arguments.extend(["--site", site])
        
        # Call the run_sherlock function with the prepared arguments
        final_results = run_sherlock(arguments)

        # Return the JsonResponse with the results
        return JsonResponse({"result": final_results})

    return JsonResponse({"detail": "Method not allowed."}, status=405)