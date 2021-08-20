
def format_polynomials(input_degree, polys):
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
        poly_str = []
        for j in range(len(list_of_x )):
            if polys[i][j] != 0:
                if polys[i][j] >= 2 and j != 0:
                    poly_str.append("+" + str(polys[i][j])+list_of_x[j])
                elif polys[i][j] >= 2 and j == 0:
                    poly_str.append(str(polys[i][j])+list_of_x[j])
                elif polys[i][j] == 1 and list_of_x[j] != '' and j != 0:
                    poly_str.append("+" +list_of_x[j])
                elif polys[i][j] == 1 and list_of_x[j] != '' and j == 0:
                    poly_str.append(list_of_x[j])
                elif list_of_x[j] == '':
                    poly_str.append("+" +str(polys[i][j]))
                elif polys[i][j] == -1 and list_of_x[j] != '':
                    poly_str.append("-" +list_of_x[j])
                elif list_of_x[j] == '':
                    poly_str.append(str(polys[i][j]))
                else:
                    poly_str.append(str(polys[i][j])+list_of_x[j])
        output_list.append(''.join(poly_str))
    
    return output_list 