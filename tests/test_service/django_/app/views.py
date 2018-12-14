import json
from django.http import HttpResponse

book_data = [{
    'id': 1,
    'name': 'A'
}, {
    'id': 2,
    'name': 'B'
}, {
    'id': 3,
    'name': 'C'
}]


def books(request):
    name = request.GET.get('name')
    data = book_data
    if name:
        data = [each for each in filter(lambda r: r['name'] == name, book_data)]

    return HttpResponse(json.dumps(data), content_type='application/json')


def book_detail(request, id):
    data = [each for each in filter(lambda r: r['id'] == id, book_data)]
    if data:
        response = HttpResponse(json.dumps(data[0]), content_type='application/json')
    else:
        response = HttpResponse(json.dumps({'msg': 'Not Found'}), content_type='application/json', status=404)

    return response
