from .models import Field, GaloisGroup, ClassGroup, Completeness
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

    def query_galois_group(self, galois_group):
        query = ''
        if 'T' in galois_group:
            g_g = galois_group.split('T')
            degree = g_g[0]
            transitive_group_id = g_g[1]
            query += " (SELECT group_id FROM galois_group WHERE degree =" + str(degree) + " AND transitive_group_id =" + str(transitive_group_id) + ")"

        elif 't' in galois_group:
            g_g = galois_group.split('t')
            degree = g_g[0]
            transitive_group_id = g_g[1]
            query += " (SELECT group_id FROM galois_group WHERE degree =" + str(degree) + " AND transitive_group_id =" + str(transitive_group_id) + ")"

        elif ',' in galois_group:
            g_g = galois_group.split(',')
            group_order = g_g[0]
            small_group_id = g_g[1]
            query += "(SELECT group_id FROM galois_group WHERE group_order=" + str(group_order) + " AND small_group_id = " + str(small_group_id) + ")"

        return query        
    
    
    def poly_query(self, input_degree = None, input_disc =None, input_cm=None, r =None, galois_group = None, class_group = None):

        query_data = {}
        query_data['degree'] = input_degree
        query_data['discriminant'] = input_disc
        query_data['cm'] = input_cm
        query_data["real embeddings"] = r
        query_data["galois_group"] = galois_group
        query_data["class_group"] = class_group


        query = "SELECT polynomial, discriminant FROM field "
        query += "WHERE"
        first = True
        for k, v in query_data.items():
            if k == "degree":
                data = v
                if data:
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
                if data:
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
                if  data:
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    if data == 't' or data == 'T':
                        query += " cm = TRUE "
                    elif data == 'f' or data == 'F': 
                        query += " cm = FALSE "
                    
            elif k == "real embeddings":
                data = v
                if data:
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    query += " real_embeddings = " + str(data)

            elif k == "galois_group":
                data = v
                if data:
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    query += " group_id =" + self.query_galois_group(data)
            
            elif k == "class_group":
                data = v
                if data:
                    if not first:
                        query += " AND"
                    else:
                        first = False
                    if ',' not in data:
                        query += " class_group_id = (SELECT class_group_id from class_group WHERE group_order =" + str(data) + " LIMIT 1)"
                    else:
                        query += " class_group_id = (SELECT class_group_id from class_group WHERE structure = '{" + str(data) + "}')"
                    

        print(query)

        cursor = connection.cursor()
        cursor.execute(query)
        polys = cursor.fetchall()

        output_polys = []
        output_discs = []
        for i in range(len(polys)):
            output_polys = output_polys + self.format_polynomials(polys[i])
            output_discs.append(str(polys[i][1]))


        return output_polys, output_discs

    
    def format_signature(self, input_sig):
        sig = input_sig.split(',')
        try:
            r = int(sig[0])
            s = int(sig[1])
        except ValueError:
            r= -1
            s = -1

        return r,s

    def completeness_query(self, r, galois_group):
        
        query_data = {}
        query_data["real embeddings"] = r
        query_data["galois_group"] = galois_group

        query = "SELECT grh, discriminant_bound FROM completeness "
        query += "WHERE real_embeddings = " + str(r) +" AND group_id =" + self.query_galois_group(galois_group)

        print(query)
        
        cursor = connection.cursor()
        cursor.execute(query)
        output = cursor.fetchall()

        output_grh = []
        output_discs = []
        for i in range(len(output)):
            output_grh.append(str(output[i][0]))
            output_discs.append(str(output[i][1]))


        return output_grh, output_discs

    def degree_check(self, input_degree):
        if ',' not in input_degree:
            try: 
                if int(input_degree) < 1:   
                    return False
            except ValueError:
                 return False
                
        else:
            try:
                degree_range = input_degree.split(',')
                if int(degree_range[0]) < 1 or int(degree_range[1]) < 1:
                    return False
            except ValueError:
                 return False
        
        return True

    def sig_check(self, input_sig, input_degree=None):
        r,s = self.format_signature(input_sig)
        if r < 0 or s < 0:
            return False

        if input_degree == '' or input_degree == None:
            input_degree = r+(2*s)
            input_degree = str(input_degree)
            return input_degree

        elif r+(2*s) != int(input_degree):      
            return False
        elif ',' in input_degree:
            return False

        return True

    def disc_check(self, input_disc):
        if ',' not in input_disc:
            try: 
                int(input_disc)
            except ValueError:
                 return False        
        else:
            try:
                disc_range = input_disc.split(',')
                int(disc_range[0]) 
                int(disc_range[1])               
            except ValueError:
                 return False
        
        return True

    def cm_check(self,input_cm):
        valid_values = ['t', 'T', 'f', 'F']
        
        if input_cm in valid_values:
            return True
        else:
            return False