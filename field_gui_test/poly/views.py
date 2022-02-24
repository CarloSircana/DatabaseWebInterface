from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View

from .helper import Helper
from .models import Field
from .forms import InputForm

from django.core.exceptions import ValidationError
import django.core.validators as val
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.views.decorators.cache import cache_control



# @cache_control(no_cache=True, no_store=True, max_age=0)
def index(request):
    #degree = polys.get_degree()
    #output = '\n'.join([str(q.degree) for q in degree])
    
    cache.clear()
    form = InputForm(request.GET)


    context = {'form': form}
    return render(request, 'poly/index.html', context)
    #return HttpResponse('adsasdkfjbsdhf')

class OutputView(View):

    cache.clear()
    form = InputForm
    
    input_degree = ''
    input_disc = ''
    input_cm = ''
    input_sig = ''
    galois_group = ''
    class_group = ''

    def input_format(self,input_list):
        input_values = []
        for i in input_list:
            val = i.split(': ')
            input_values.append(val[1])
        
        return input_values
        

    def output(self, request): 

        # form_context = {'form': self.form(request)}
        # print(form_context)
        
        self.r = ''
        
        self.input_degree = request.GET.get('degree')
        self.input_disc = request.GET.get('discriminant')
        self.input_cm = request.GET.get('cm')
        self.input_sig = request.GET.get('signature')
        self.galois_group = request.GET.get('galois_group')
        self.class_group = request.GET.get('class_group')
        
        if not self.input_degree and not self.input_disc and not self.input_cm and not self.input_sig and not self.galois_group and not self.class_group:
            return index(request) #render(request, 'poly/index.html', form_context)

        poly = Helper()
        
        
        # degree check
        if self.input_degree: 
            if poly.degree_check(self.input_degree) == False:
                return index(request) #render(request, 'poly/index.html', form_context)

        ## disc check
        if self.input_disc:
            if poly.disc_check(self.input_disc) == False:
                return index(request) #render(request, 'poly/index.html', form_context)

        ## signature check
        if self.input_sig: 
            if self.input_degree: 
                if poly.sig_check(self.input_sig, self.input_degree) == False:
                    return index(request) #render(request, 'poly/index.html', form_context)
            else:
                if poly.sig_check(self.input_sig) == False:
                    return index(request) #render(request, 'poly/index.html', form_context)
                else:
                    self.input_degree = poly.sig_check(self.input_sig)

        
        ## cm check
        if self.input_cm:
            if poly.cm_check(self.input_cm) == False:
                return index(request)# return render(request, 'poly/index.html', form_context)

        ## galois_group check
        if self.galois_group:
            if poly.galois_check(self.galois_group) == False:
                return index(request) #return render(request, 'poly/index.html', form_context)

        ## class_group_check
        if self.class_group:
            if poly.class_group_check(self.class_group) == False:
                return index(request) #return render(request, 'poly/index.html', form_context)
        

        if 'poly' in request.GET:
            
            if self.input_sig:
                self.r = self.input_sig[0]
                # print(self.r)
            output_polys, output_discs = poly.poly_query(self.input_degree,self.input_disc, self.input_cm,self.r, self.galois_group, self.class_group)

            formatted_polys = []

            for i in output_polys:
                formatted_polys = formatted_polys + poly.format_polynomials(i)

            output_list = zip(formatted_polys, output_discs)

            #for polys,discs in output_list:
                #print(polys,discs)

            
            input_list = ['degree: ' + str(self.input_degree),'discriminant: ' + str(self.input_disc), 'cm: '+ str(self.input_cm), 'signature: ' + str(self.input_sig), 'galois_group: ' + str(self.galois_group)]

            
            if self.class_group:
                if ',' in self.class_group:
                    input_list.append('class group structure: {' + str(self.class_group) + "}")
                else:
                    input_list.append('class group id: ' + str(self.class_group))


            # set cache for download files
            cache.set("inputs", input_list)

            context = {'input_list': input_list, 'queryset': output_list }
            #print((polys[0]))
            #return HttpResponse(output)
            return render(request, 'poly/output.html',context)
            

        elif 'completeness' in request.GET:
            
            if not self.galois_group or not self.input_sig:
                return index(request) #render(request, 'poly/index.html', self.form_context)
                
            r = self.input_sig[0]
            output_grh, output_discs = poly.completeness_query(r, self.galois_group)

            output_list = zip(output_grh, output_discs)

            #for polys,discs in output_list:
                #print(polys,discs)

            
            input_list = ['signature: ' + str(self.input_sig), 'galois_group: ' + str(self.galois_group)]
            
            context = {'input_list': input_list, 'queryset': output_list }
            #print((polys[0]))
            #return HttpResponse(output)
            return render(request, 'poly/completeness.html',context)
            

    # elif 'reset' in request.GET:
        # form = InputForm(request.GET)

        # form_context = {'form': form}
        # return render(request, 'poly/index.html', form_context)
    def get(self, request):
        return self.output(request)

class DownloadPyView(OutputView, View):

    def download_py(self,request):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=py_readable_polys_discs.txt'

        helper = Helper()    

        input_list = cache.get('inputs')
        
        query_values = OutputView.input_format(self, input_list)


        # print(query_values)
        r = ''
        input_degree = query_values[0] #OutputView.input_degree #request.GET.get('degree')
        input_disc = query_values[1] #OutputView.input_disc #request.GET.get('discriminant')
        input_cm = query_values[2] #OutputView.input_cm #request.GET.get('cm')
        input_sig = query_values[3] #OutputView.input_sig #request.GET.get('signature')
        galois_group = query_values[4] #OutputView.galois_group #request.GET.get('galois_group')
        
        class_group = ''
        if len(query_values) > 5:
            class_group = query_values[5] #OutputView.class_group #request.GET.get('class_group')

        

        if input_sig:
            r = input_sig[0]
            # print(r)

        output_polys, output_discs = helper.poly_query(input_degree,input_disc, input_cm,r, galois_group, class_group)

        formatted_polys = []

        for i in output_polys:
            formatted_polys = formatted_polys + helper.format_download_py(i)

        output_list = zip(formatted_polys, output_discs)

        response.writelines(output_list)
        
        return response
    def get(self, request):
        return self.download_py(request)

class DownloadJlView(OutputView, View):

    def download_jl(self,request):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=jl_readable_polys_discs.txt'

        helper = Helper()    

        input_list = cache.get('inputs')
        
        query_values = OutputView.input_format(self, input_list)


        # print(query_values)
        r = ''
        input_degree = query_values[0] #OutputView.input_degree #request.GET.get('degree')
        input_disc = query_values[1] #OutputView.input_disc #request.GET.get('discriminant')
        input_cm = query_values[2] #OutputView.input_cm #request.GET.get('cm')
        input_sig = query_values[3] #OutputView.input_sig #request.GET.get('signature')
        galois_group = query_values[4] #OutputView.galois_group #request.GET.get('galois_group')
        
        class_group = ''
        if len(query_values) > 5:
            class_group = query_values[5] #OutputView.class_group #request.GET.get('class_group')

        if input_sig:
            r = input_sig[0]
            # print(r)

        output_polys, output_discs = helper.poly_query(input_degree,input_disc, input_cm,r, galois_group, class_group)

        formatted_polys = []

        for i in output_polys:
            formatted_polys = formatted_polys + helper.format_download_jl(i)

        output_list = zip(formatted_polys, output_discs)

        response.writelines(output_list)
        
        return response
    def get(self, request):
        return self.download_jl(request)

class DownloadCoeffView(OutputView, View):

    def download_coeff(self,request):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=poly_coeff_and_disc.txt'

        helper = Helper()    

        input_list = cache.get('inputs')
        
        query_values = OutputView.input_format(self, input_list)


        # print(query_values)
        r = ''
        input_degree = query_values[0] #OutputView.input_degree #request.GET.get('degree')
        input_disc = query_values[1] #OutputView.input_disc #request.GET.get('discriminant')
        input_cm = query_values[2] #OutputView.input_cm #request.GET.get('cm')
        input_sig = query_values[3] #OutputView.input_sig #request.GET.get('signature')
        galois_group = query_values[4] #OutputView.galois_group #request.GET.get('galois_group')
        
        class_group = ''
        if len(query_values) > 5:
            class_group = query_values[5] #OutputView.class_group #request.GET.get('class_group')

        if input_sig:
            r = input_sig[0]
            # print(r)

        output_polys, output_discs = helper.poly_query(input_degree,input_disc, input_cm,r, galois_group, class_group)

        # formatted_polys = []

        # for i in output_polys:
        #     formatted_polys = formatted_polys + helper.format_download_coeff(i)

        # print(formatted_polys)

        output_list = zip(output_polys, output_discs)

        response.writelines(output_list)
        
        return response
    def get(self, request):
        return self.download_coeff(request)