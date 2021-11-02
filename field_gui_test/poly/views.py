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
    

    ## degree check
    if input_degree: 
        if poly.degree_check(input_degree) == False:
            return render(request, 'poly/index.html')

    ## disc check
    if input_disc:
        if poly.disc_check(input_disc) == False:
            return render(request, 'poly/index.html')

    ## signature check
    if input_sig: 
        if input_degree: 
            if poly.sig_check(input_sig, input_degree) == False:
                return render(request, 'poly/index.html')
        else:
            if poly.sig_check(input_sig) == False:
                return render(request, 'poly/index.html')
            else:
                input_degree = poly.sig_check(input_sig)

    
    ## cm check
    if input_cm:
        if poly.cm_check(input_cm) == False:
            return render(request, 'poly/index.html')

    ## galois_group check
    if galois_group:
        if poly.galois_check(galois_group) == False:
            return render(request, 'poly/index.html')

    ## class_group_check
    if class_group:
        if poly.class_group_check(class_group) == False:
            return render(request, 'poly/index.html')
    

    

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
        if not galois_group or not input_sig:
            return render(request, 'poly/index.html')
            
        r = input_sig[0]
        output_grh, output_discs = poly.completeness_query(r, galois_group)

        output_list = zip(output_grh[:10], output_discs[:10])

        #for polys,discs in output_list:
            #print(polys,discs)

        
        input_list = ['signature: ' + str(input_sig), 'galois_group: ' + str(galois_group)]
        
        context = {'input_list': input_list, 'queryset': output_list }
        #print((polys[0]))
        #return HttpResponse(output)
        return render(request, 'poly/completeness.html',context)
