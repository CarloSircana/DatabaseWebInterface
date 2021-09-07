from .models import Field
from django.db import connection

class Helper():

    def __init__(self) -> None:
        pass
    def format_polynomials(self,polys):
        ## generate list_of_x for polynomial
        #input_degree = int(input_degree)
        superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        list_of_x = []
        for i in range(len(polys[0])):
            if i >= 2:
                list_of_x.append(f'x{i}'.translate(superscript))
            elif i ==1 or i == -1:
                list_of_x.append('x')
            else:
                list_of_x.append('')
        list_of_x = list_of_x[::-1]
        
        ## put the coeffs(polys) and list_of_x together to form output string
        output_list = []
        #for i in range(len(polys)):
        poly_order = polys[0]
        #print(poly_order)
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
        #print(output_list)
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
                    polys = Field.objects.values_list('polynomial', flat=True).filter(degree = i, real_embeddings = input_rm)
                formatted_poly = self.format_polynomials(polys)
                output_list = output_list + formatted_poly

        else:
            #input_degree = int(input_degree)
            if input_rm  == None:
                polys = Field.objects.values_list('polynomial', flat=True).filter(degree = input_degree)
            else:
                polys = Field.objects.values_list('polynomial', flat=True).filter(degree = input_degree).filter(real_embeddings = input_rm)
            output_list = self.format_polynomials(polys)

        print(len(polys[0]))
        return output_list
    
    def disc_(self, input_disc):
        if ',' in input_disc:
            input_disc_range = input_disc.split(',')
           
            output_list = []
            #for i in disc_range:
            polys = Field.objects.values_list('polynomial', flat=True).filter(discriminant__range = (input_disc_range[0], input_disc_range[1]))

            for i in range(len(polys)):
                output_list.append(self.format_polynomials(polys[i]))
            
            
            return output_list

        else:
            
            polys = Field.objects.values_list('polynomial', flat=True).filter(discriminant = input_disc)
            
            output_list = self.format_polynomials(polys)

        return output_list

    def degree_disc_(self, input_disc,input_degree):
        if ',' in input_disc and ',' not in input_degree:
            input_disc_range = input_disc.split(',')
            #input_disc_range = list(map(int, input_disc_range))

            polys = Field.objects.values_list('polynomial',flat=True).filter(degree = input_degree, discriminant__range = (input_disc_range[0], input_disc_range[1]))
            output_list = self.format_polynomials(polys)
            
            return output_list

        elif ',' not in input_disc and ',' in input_degree:
            degree_range = input_degree.split(',')
            #input_degree_range = list(map(int, input_degree_range))

            #degree_range = list(range(input_degree_range[0], input_degree_range[1]+1))
            #output_list = []
            #for i in degree_range:
            polys = Field.objects.values_list('polynomial', flat=True).filter(degree__range = (degree_range[0], degree_range[1]), discriminant = input_disc)
            output_list = self.format_polynomials(polys)
            #output_list = output_list + formatted_poly

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
            polys = Field.objects.values_list('polynomial',flat=True).filter(degree = input_degree, discriminant = input_disc)
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

    
    
    def raw_query(self, input_degree = None, input_disc =None, input_cm=None, r =None):

        query_data = {}
        query_data['degree'] = input_degree
        query_data['discriminant'] = input_disc
        query_data['cm'] = input_cm
        query_data["real embeddings"] = r


        query = "SELECT polynomial, discriminant FROM field "
        query += "WHERE"
        first = True
        for k, v in query_data.items():
            if k == "degree":
                data = v
                print(data)
                if data is not None and data != '':
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    if ',' not in data:
                        query += " degree = " + str(data)
                    else:
                        degree_range = data.split(',')
                        # print(degree_range)
                        query += " degree BETWEEN " + degree_range[0] + ' AND ' + degree_range[1] 
            elif k == "discriminant":
                data = v
                print(data)
                if data is not None and data != '':
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    if ',' not in data:
                        query += " discriminant =" + data
                    else:
                        disc_range = data.split(',')
                        print(disc_range)
                        query += " discriminant BETWEEN " + disc_range[0] + ' AND ' + disc_range[1] 
            elif k == "cm":
                data = v
                if  data is not None and data != '':
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    if data == 't':
                        query += " cm = TRUE " 
                    else:
                        query += " cm = FALSE "
            elif k == "real embeddings":
                data = v
                if data is not None and data != '':
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    query += " real_embeddings = " + str(data)

        print(query)

        cursor = connection.cursor()
        cursor.execute(query + 'ORDER BY degree')
        polys = cursor.fetchall()
        #print(polys)

        output_polys = []
        output_discs = []
        for i in range(len(polys)):
            output_polys = output_polys + self.format_polynomials(polys[i])
            output_discs.append(str(polys[i][1]))

        return output_polys

    
    def format_signature(self, input_sig):
        sig = input_sig.split(',')
        r = int(sig[0])
        s = int(sig[1])

        return r,s