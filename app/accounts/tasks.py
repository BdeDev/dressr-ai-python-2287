from celery import shared_task
from .models import User

@shared_task
def generate_avatar_task(user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile  # Assuming OneToOne Profile model
    #profile.avatar_url = geterate_avatar(user.id)
    profile.save()
    return f"Avatar generated for user {user.full_name}"