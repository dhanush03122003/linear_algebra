from django.shortcuts import render, redirect
from django.http import HttpResponse
from openpyxl import Workbook
from sample_app.models import Details
import numpy as np####
from sympy import Matrix#####

def HOME(request):
    if request.method == "POST":
        Details.objects.create(name=request.POST['name'], profile=request.POST['pf'])
        return redirect('/hi/')
       # return render(request, 'margins.html')
    return render(request, 'margins.html')

def display_det(request):
    all_details = Details.objects.all()
    return render(request, 'display_all.html', {'det': all_details})

def generate_excel(request):
    all_details = Details.objects.all()

    # Create a workbook and add details to it
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Name'
    sheet['B1'] = 'Profile'

    for index, detail in enumerate(all_details, start=2):
        sheet[f'A{index}'] = detail.name
        sheet[f'B{index}'] = detail.profile

    # Save the workbook to a BytesIO buffer
    from io import BytesIO
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Create a response with the Excel content
    response = HttpResponse(buffer.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=details.xlsx'

    return response

def linear_alg(request):
    if(request.method == "POST"):
        print("kkk")
        rows = int(request.POST.get('rows', 0))
        cols = int(request.POST.get('cols', 0))

        # Initialize a 2D array
        matrix = [[0] * cols for _ in range(rows)]

        # Populate the matrix with form data
        for i in range(rows):
            for j in range(cols):
                input_name = f'matrix[{i}][{j}]'
                matrix[i][j] = int(request.POST.get(input_name, 0))

        # You can print or use the matrix as needed
        print(matrix)
        A = np.array(matrix)
        A_sympy = Matrix(A)

        RREF, _ = A_sympy.rref()

        non_zero_rows = np.array(RREF)[~np.all(np.array(RREF) == 0, axis=1)]
        print("row space : ")
        print(non_zero_rows)
        print('row space dimension : ',len(non_zero_rows))

            
        col_space_matrix = A[:, :np.linalg.matrix_rank(A)]
        print("Column space matrix:")
        col_space_matrix = col_space_matrix.T
        print(col_space_matrix)
        print('col space dimension : ',len(col_space_matrix))

        X1 = Matrix(A)
        X = np.array(X1.nullspace())
        null_space = [[elem[0] for elem in row] for row in X]
        print("null space : ",null_space)
        print('null space dimension : ',len(null_space))

        X1 = Matrix(A.T)
        X = np.array(X1.nullspace())
        l_null_space = [[elem[0] for elem in row] for row in X]
        print("left null space : ",l_null_space)
        print('left null space dimension : ',len(l_null_space))
        data = {}
        data['rows'] = request.POST['rows']
        data['cols'] = request.POST['cols']

        if (data['rows'] == data['cols']):
            eigenvalues_and_vectors = A_sympy.eigenvects()
            print("Eigenvalues and Eigenvectors:")
            l = []
            for eigenvector_info in eigenvalues_and_vectors:
                eigenvalue = eigenvector_info[0]
                multiplicity = eigenvector_info[1]
                eigenvectors = eigenvector_info[2]
                l.append(eigenvalue)
                print(f"Eigenvalue: {eigenvalue}, Multiplicity: {multiplicity}")
                print(f"Eigenvectors:")
                for eigenvector in eigenvectors:
                    print(list(eigenvector))
            data['eigenvalues_and_vectors'] = eigenvalues_and_vectors
            data['no_eigen_vals'] = len(l)
            data['eigen_vals'] = l
            

        data['RREF'] = np.array(RREF)
        data['MATRIX'] = A

        data['row_space_valid'] = len(non_zero_rows)!= 0
        data['row_space'] = non_zero_rows
        data['row_space_dim'] = len(non_zero_rows)

        data['col_space_valid'] = len(col_space_matrix)!= 0
        data['col_space'] = col_space_matrix
        data['col_space_dim'] = len(col_space_matrix)

        data['null_space_valid'] = len(null_space)!= 0
        data['null_space'] = null_space
        data['null_space_dim'] = len(null_space)

        data['l_null_space_valid'] = len(l_null_space)!= 0
        data['l_null_space'] = l_null_space
        data['l_null_space_dim'] = len(l_null_space)

        return render(request,'lin_alg.html',{'data':data})

    return render(request,'lin_alg.html')





