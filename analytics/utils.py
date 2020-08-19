
def get_client_ip(request):
    x_fowrarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_fowrarded_for:
        ip = x_fowrarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR",None)
    return ip
