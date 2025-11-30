from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Triggers post_delete signal
        return JsonResponse({"message": "User deleted successfully."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=400)
