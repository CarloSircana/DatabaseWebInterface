# DatabaseWebInterface
python 3.9.6

Setup and use: 
1. clone. 
2. create a virtual env using requirements.txt. 
3. edit the database settings in settings.py. 
4. run on local server, do python manage.py runserver 

Target Create a website for the database of number fields, similar to www.lmfdb.orgNumberField or galoisdb.math.upb.de.

Steps already done First simple queries by degree,signature, discriminant, cm property.

TODO Set up raw queries and convert the code to use simple queries. Output polynomial, discriminant, signature, formatted as a table.

Sanity checks

degree = 1
signature (r, s) = r=0 , s = 0, r+2s = degree.
Create tables Something like the first table in httpswww.lmfdb.orgNumberFieldstats. Understand how to make columns and rows in html.

Queries with galois group 2 different fields for the html interface

Integer for transitive group id

Pair of integers for small group id (corresponding to group_order and small_group_id)

To perform the query in the galois_group table, you also need the degree. degree + transitive_group_id or degree + group_order + small_group_id uniquely identifies the group.

No nested queries We need to check that the required group is in the the table. First, we search for the group, meaning that we want the group_id (primary key in the galois_group table). If the group is missing, just return empty page. Otherwise, you perform the query in the field table searching for the fields with that group_id. You can assume that the order, degree and ids are all int.

UPDATE One single input field, called Galois group. The input can be of 2 forms

nTk n is the degree, k is the transitive group id. Example 4T2 means degree 4 and transitive group id 2
[n, k] n is the order of the group, k is the small group id. Example [3, 1].

Completeness data table The user asks for a group (nTk or [order, small_group_id]) and a signature (r, s). Retrieve the discriminant bound from the completeness table. You might get multiple answers, depending on the grh entry in the table. Print all of them (grh value and discriminant_bound), together with the group data given in input by the user.

Class group query Two possibilities for the user

class number (it is an integer = 1)
class group structure (list of integers = 1 with the property that each integer is a multiple of the previous entry in the list) (Example [2, 4] is allowed, [2] is allowed, [2, 3] is not allowed, because 3 is not a multiple of 2)
The class number corresponds to the entry group_order in the class group table. Careful it might overflow. It is not a primary key, so there might be multiple entries in the table satisfying this property. The class group structure corresponds to the entry structure in the class group table. It is a primary key, so only one possible entry. As for the galois group queries, perform either a nested query or a double query, retrieving the class_group_id.

Next steps Statistics page Completeness data queries. Source of data.

Note: class_group_id overflows, temporary solution limit 1, degree in galois_group and degree in field don't match

To Do: add error message for invalid input, back button keeps the input, add new clear inputs button in index page, check memory usage
