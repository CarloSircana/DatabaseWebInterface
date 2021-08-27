from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .helper import Helper
from .models import Field

def index(request):
    #degree = polys.get_degree()
    #output = '\n'.join([str(q.degree) for q in degree])

    return render(request, 'poly/index.html')
    #return HttpResponse('adsasdkfjbsdhf')

def output(request):
    input_degree = request.GET.get('degree')
    input_disc = request.GET.get('discriminant')
    input_cm = request.GET.get('cm')
    input_sig = request.GET.get('signature')

    #print(request.GET)
    if input_degree == '' or input_degree == None:
        if input_disc == '' or input_disc == None:
            if input_cm == '' or input_cm == None:
                if input_sig == '' or input_sig == None:
                    return render(request, 'poly/index.html')
    
    sig = input_sig.split(',')

    poly = Helper()

    if input_degree != '' and input_disc == '':
        output_list = poly.degree_(input_degree)
    elif input_degree == '' and input_disc != '':
        output_list = poly.disc_(input_disc)
    elif input_degree != '' and input_disc != '':
        output_list = poly.degree_disc_(input_disc,input_degree)
    else:
        output_list = poly.signature_(sig[0],sig[1])
    

    #print(output_list)
    context = {'degree': input_degree, 'discriminant':input_disc, 'queryset': output_list}
    #print((polys[0]))
    #return HttpResponse(output)
    return render(request, 'poly/output.html',context)

