from celery import shared_task
from .views import my_function_view

@shared_task
def run_my_function_view():
    # Your additional code, if needed
    response = my_function_view(None)
    # Do something with the response if needed