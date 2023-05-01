import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sherlock import run_sherlock
from sherlock.result import QueryResult


def prepare_arguments(data, args_with_defaults):
    arguments = []
    for arg, default in args_with_defaults.items():
        value = data.get(arg, default)

        if isinstance(value, list):
            for item in value:
                if arg != "usernames":
                    arguments.extend([f"--{arg}", item])
                else:
                    arguments.append(item)
        elif isinstance(value, bool) and value:
            arguments.append(f"--{arg}")
        else:
            arguments.extend([f"--{arg}", value])
    return arguments


@csrf_exempt
def run_sherlock_api(request):
    if request.method == "POST":
        # Parse JSON data received from the client
        data = json.loads(request.body)

        # Prepare a list of arguments to pass to the run_sherlock function
        args_with_defaults = {
            "site": ["reddit", "twitter"],
            "usernames": [],
        }
        arguments = prepare_arguments(data, args_with_defaults)

        # Find any args not in args_with_defaults
        args_not_supported = set(data.keys()) - set(args_with_defaults.keys())
        if args_not_supported:
            return JsonResponse(
                {"detail": f"Arguments not supported: {', '.join(args_not_supported)}"},
                status=400,
            )

        # Call the run_sherlock function with the prepared arguments
        final_results = run_sherlock(arguments)
        final_results_serializable = []
        for result in final_results:
            assert set(result.keys()) == set(["username", "results"])
            for site, values in result["results"].items():
                new_values = {}
                for key, value in values.items():
                    if isinstance(value, QueryResult):
                        new_values[key] = str(value)
                    elif key == "response_text":
                        pass
                    else:
                        new_values[key] = value
                result["results"][site] = new_values
            final_results_serializable.append(result)
        return JsonResponse({"result": final_results_serializable})

    return JsonResponse({"detail": "Method not allowed."}, status=405)
