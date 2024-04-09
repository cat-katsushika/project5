from django.shortcuts import render


def terms_of_service(request):
    return render(request, 'terms_and_conditions/terms_of_service.html')

def privacy_policy(request):
    return render(request, "terms_and_conditions/privacy_policy.html")

def specified_commercial_transaction_act(request):
    return render(request, "terms_and_conditions/specified_commercial_transaction_act.html")