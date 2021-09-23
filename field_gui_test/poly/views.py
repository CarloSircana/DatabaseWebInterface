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
    # input_degree = None
    # input_disc = None
    # input_cm = None
    r = ''
    
    input_degree = request.GET.get('degree')
    input_disc = request.GET.get('discriminant')
    input_cm = request.GET.get('cm')
    input_sig = request.GET.get('signature')
    galois_group = request.GET.get('galois_group')
    class_group = request.GET.get('class_group')

    if not input_degree and not input_disc and not input_cm and not input_sig and not galois_group and not class_group:
        return render(request, 'poly/index.html')

    poly = Helper()
    
    ## signature check
    if input_sig: 
        r,s = poly.format_signature(input_sig)
        if r < 0 or s < 0:
            return render(request, 'poly/index.html')

        if input_degree == '' or input_degree == None:
            input_degree = r+(2*s)
            input_degree = str(input_degree)

        elif r+(2*s) != int(input_degree):      
            return render(request, 'poly/index.html')
        elif ',' in input_degree:
            return render(request, 'poly/index.html')

    

    ## degree check
    if input_degree: #!= '' and input_degree is not None:
        if ',' not in input_degree:
            if int(input_degree) < 1:   
                return render(request, 'poly/index.html')
        else:
            degree_range = input_degree.split(',')
            if int(degree_range[0]) < 1 or int(degree_range[1]) < 1:
                return render(request, 'poly/index.html')


    # if input_degree != '' and input_disc == '':
    #     output_list = poly.degree_(input_degree)
    # elif input_degree == '' and input_disc != '':
    #     output_list = poly.disc_(input_disc)
    # elif input_degree != '' and input_disc != '':
    #     output_list = poly.degree_disc_(input_disc,input_degree)
    # else:
    #     output_list = poly.signature_(sig[0],sig[1])

    if 'poly' in request.GET:
        output_polys, output_discs = poly.poly_query(input_degree,input_disc, input_cm,r, galois_group, class_group)

        output_list = zip(output_polys[:10], output_discs[:10])

        #for polys,discs in output_list:
            #print(polys,discs)

        
        input_list = ['degree: ' + str(input_degree),'discriminant: ' + str(input_disc), 'cm: '+ str(input_cm), 'signature: ' + str(input_sig), 'galois_group: ' + str(galois_group)]
        
        if class_group:
            if ',' in class_group:
                input_list.append('class group structure: {' + str(class_group) + "}")
            else:
                input_list.append('class group id: ' + str(class_group))
        context = {'input_list': input_list, 'queryset': output_list }
        #print((polys[0]))
        #return HttpResponse(output)
        return render(request, 'poly/output.html',context)

    elif 'completeness' in request.GET:
        output_grh, output_discs = poly.completeness_query(r, galois_group)

        output_list = zip(output_grh[:10], output_discs[:10])

        #for polys,discs in output_list:
            #print(polys,discs)

        
        input_list = ['signature: ' + str(input_sig), 'galois_group: ' + str(galois_group)]
        
        context = {'input_list': input_list, 'queryset': output_list }
        #print((polys[0]))
        #return HttpResponse(output)
        return render(request, 'poly/completeness.html',context)
