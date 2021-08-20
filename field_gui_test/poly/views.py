from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .helper import format_polynomials
from .models import Field

def index(request):
    #degree = polys.get_degree()
    #output = '\n'.join([str(q.degree) for q in degree])

    return render(request, 'poly/index.html')
    #return HttpResponse('adsasdkfjbsdhf')

def output(request):
    input_degree = request.GET.get('degree')
    if input_degree == '' or input_degree == None:
        return render(request, 'poly/index.html')

    if ',' in input_degree:
        input_degree_range = input_degree.split(',')
        input_degree_range = list(map(int, input_degree_range))

        degree_range = list(range(input_degree_range[0], input_degree_range[1]+1))
        output_list = []
        for i in degree_range:
            polys = Field.objects.values_list('polynomial', flat=True).filter(degree = i)
            formatted_poly = format_polynomials(i,polys)
            output_list = output_list + formatted_poly

    else:
        #input_degree = int(input_degree)
        polys = Field.objects.values_list('polynomial', flat=True).filter(degree = input_degree)
        output_list = format_polynomials(input_degree,polys)

    #print(output_list)
    context = {'degree': input_degree, 'queryset': output_list}
    #print((polys[0]))
    #return HttpResponse(output)
    return render(request, 'poly/output.html',context)

