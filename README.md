# Database Web Interface


Target: Create a website for the database of number fields, similar to https://www.lmfdb.org/NumberField/ or http://galoisdb.math.upb.de/.

Steps already done:
First simple queries by degree,signature, discriminant, cm property.

TODO:
Set up raw queries and convert the code to use simple queries.
Output: polynomial, discriminant, signature
Sanity checks:
- degree >= 1
- signature (r, s) => r>=0 , s >= 0, r+2*s = degree.




Create tables:
Something like the first table in https://www.lmfdb.org/NumberField/stats. Understand how to make columns and rows in html.



Queries with galois group:
2 different fields for the html interface: - Integer for transitive group id
                                          - Pair of integers for small group id (corresponding to group_order and small_group_id)
                                          
To perform the query in the galois_group table, you also need the degree.
degree + transitive_group_id or degree + group_order + small_group_id uniquely identify the group.

No nested queries: We need to check that the required group is in the the table.
First, we search for the group, meaning that we want the group_id (primary key in the galois_group table). If the group is missing, just return empty page.
Otherwise, you perform the query in the field table searching for the fields with that group_id.
You can assume that the order, degree and ids are all int.

Completeness data table:
The user asks for a group (degree + transitive_group_id or degree + order + small_group_id) and a signature (r, s). (Sanity check: degree = r+2s, transitive_group_id > 0, order >0, small_group_id > 0). Retrieve the discriminant bound from the completeness table.
You might get 2 answers, depending on the grh entry in the table.
Print them both (grh value and discriminant_bound), together with the group data given in input by the user. 



Next steps:
Add class group, galois group queries.
Statistics page
Completeness data queries.
Source of data.
