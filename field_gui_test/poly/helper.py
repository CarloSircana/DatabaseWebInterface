from .models import Field

class Helper():

    def __init__(self) -> None:
        pass
    def format_polynomials(self, input_degree, polys):
        ## generate list_of_x for polynomial
        input_degree = int(input_degree)
        superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        list_of_x = []
        for i in range(input_degree+1):
            if i >= 2:
                list_of_x.append(f'x{i}'.translate(superscript))
            elif i ==1 or i == -1:
                list_of_x.append('x')
            else:
                list_of_x.append('')
        list_of_x = list_of_x[::-1]
        
        ## put the coeffs(polys) and list_of_x together to form output string
        output_list = []
        for i in range(len(polys)):
            poly_order = list(polys[i])
            poly_order = poly_order[::-1]
            #print(poly_order)
            poly_str = []
            for j in range(len(list_of_x )):
                if poly_order[j] != 0:
                    if poly_order[j] >= 2 and j != 0:
                        poly_str.append("+" + str(poly_order[j])+list_of_x[j])
                    elif poly_order[j] >= 2 and j == 0:
                        poly_str.append(str(poly_order[j])+list_of_x[j])
                    elif poly_order[j] == 1 and list_of_x[j] != '' and j != 0:
                        poly_str.append("+" +list_of_x[j])
                    elif poly_order[j] == 1 and list_of_x[j] != '' and j == 0:
                        poly_str.append(list_of_x[j])
                    elif list_of_x[j] == '' and poly_order[j] > 0:
                        poly_str.append("+" +str(poly_order[j]))
                    elif poly_order[j] == -1 and list_of_x[j] != '':
                        poly_str.append("-" +list_of_x[j])
                    elif list_of_x[j] == '':
                        poly_str.append(str(poly_order[j]))
                    else:
                        poly_str.append(str(poly_order[j])+list_of_x[j])
            output_list.append(''.join(poly_str))
        
        #output_list = output_list[::-1]
        return output_list 


    def degree_(self, input_degree, input_rm = None):
        if ',' in input_degree:
            input_degree_range = input_degree.split(',')
            input_degree_range = list(map(int, input_degree_range))

            degree_range = list(range(input_degree_range[0], input_degree_range[1]+1))
            output_list = []
            for i in degree_range:
                if input_rm  == None:
                    polys = Field.objects.values_list('polynomial', flat=True).filter(degree = i)
                else:
                    polys = Field.objects.values_list('polynomial', flat=True).filter(degree = i).filter(real_embeddings = input_rm)
                formatted_poly = self.format_polynomials(i,polys)
                output_list = output_list + formatted_poly

        else:
            #input_degree = int(input_degree)
            if input_rm  == None:
                polys = Field.objects.values_list('polynomial', flat=True).filter(degree = input_degree)
            else:
                polys = Field.objects.values_list('polynomial', flat=True).filter(degree = input_degree).filter(real_embeddings = input_rm)
            output_list = self.format_polynomials(input_degree,polys)

        return output_list
    
    def disc_(self, input_disc):
        if ',' in input_disc:
            input_disc_range = input_disc.split(',')
            #input_disc_range = list(map(int, input_disc_range))

            #disc_range = list(range(input_disc_range[0], input_disc_range[1]+1))
            #print(disc_range)
            output_list = []
            #for i in disc_range:
            polys = Field.objects.values_list('polynomial','degree').filter(discriminant__range = (input_disc_range[0], input_disc_range[1]))
            for i in range(len(polys)):
                formatted_poly = self.format_polynomials(polys[i][-1],polys[i][:-1])
                output_list = output_list + formatted_poly
            
            return output_list

        else:
            #input_degree = int(input_degree)
            output_list = []
            polys = Field.objects.values_list('polynomial','degree').filter(discriminant = input_disc)
            for i in range(len(polys)):
                formatted_poly = self.format_polynomials(polys[i][-1],polys[i][:-1])
                output_list = output_list + formatted_poly
            #output_list = self.format_polynomials(input_degree,polys)

        return output_list

    def degree_disc_(self, input_disc,input_degree):
        if ',' in input_disc and ',' not in input_degree:
            input_disc_range = input_disc.split(',')
            #input_disc_range = list(map(int, input_disc_range))

            polys = Field.objects.values_list('polynomial',flat=True).filter(degree = input_degree)
            polys = polys.filter(discriminant__range = (input_disc_range[0], input_disc_range[1]))
            
            output_list = self.format_polynomials(input_degree, polys)
            
            return output_list

        elif ',' not in input_disc and ',' in input_degree:
            input_degree_range = input_degree.split(',')
            input_degree_range = list(map(int, input_degree_range))

            degree_range = list(range(input_degree_range[0], input_degree_range[1]+1))
            output_list = []
            for i in degree_range:
                polys = Field.objects.values_list('polynomial', flat=True).filter(degree = i).filter(discriminant = input_disc)
                formatted_poly = self.format_polynomials(i,polys)
                output_list = output_list + formatted_poly

            return output_list

        elif ',' in input_disc and ',' in input_degree:
            input_degree_range = input_degree.split(',')
            input_degree_range = list(map(int, input_degree_range))
            input_disc_range = input_disc.split(',')

            degree_range = list(range(input_degree_range[0], input_degree_range[1]+1))
            output_list = []
            for i in degree_range:
                polys = Field.objects.values_list('polynomial', flat=True).filter(degree = i)
                polys = polys.filter(discriminant__range = (input_disc_range[0], input_disc_range[1]))
                formatted_poly = self.format_polynomials(i,polys)
                output_list = output_list + formatted_poly

            return output_list
        elif ',' not in input_degree and ',' not in input_disc:
            polys = Field.objects.values_list('polynomial',flat=True).filter(degree = input_degree)
            polys = polys.filter(discriminant = input_disc)
            output_list = self.format_polynomials(input_degree, polys)
            
            return output_list

    def cm_(self,input_cm):
        polys = Field.objects.values_list('polynomial','degree').filter(cm = input_cm)
        output_list = []
        for i in range(len(polys)):
                formatted_poly = self.format_polynomials(polys[i][-1],polys[i][:-1])
                output_list = output_list + formatted_poly
            
        return output_list


    def signature_(self,input_rm,input_s):
        deg = int(input_rm) + 2*int(input_s)

        polys = Field.objects.values_list('polynomial', flat=True).filter(degree = deg).filter(real_embeddings = input_rm)

        output_list = self.format_polynomials(deg,polys)

        return output_list