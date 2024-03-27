from rest_framework import response

def CustomErrorResponse(status_code, message, data=None):
    return response.Response({
        "status_code": status_code,
        "message": message,
        "status": "error",
        "data": data
    }, status=status_code)