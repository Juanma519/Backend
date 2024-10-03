from universidades_handler import *
from alumnos_handler import *
from users_handler import *
from cursos_handler import *
from clases_handler import *


if __name__ == "__main__":
    
    #print(create_usuario("SuperAdmin", "Perez", "12345", 0, "superadmin@gmail.com", "Universidad de Montevideo"))
    #print(create_usuario("Admin", "Perez", "12345", 1, "admin@gmail.com", "Universidad de Montevideo"))
    #print(create_usuario("Profe", "Perez", "12345", 2, "profe@gmail.com", "Universidad de Montevideo"))

# UNIVERSIDADES
# create
    #print(create_universidad("Universidad de Chile"))
# update
    #print(update_nombre_universidad("Universidad de Chile", "Universidad de Chile2"))
# delete
    #print(delete_universidad("Universidad de Chile2"))
# get
    #print(get_universidad("Universidad de Montevideo"))
    #print(get_universidades())
    
# SALONES
# create
    #print(create_salon("Salon 1", "Universidad de Montevideo"))
# update
    #print(update_nombre_salon("Salon 1", "L205", "Universidad de Montevideo"))
# delete
    #print(delete_salon("L205", "Universidad de Montevideo"))
# get
    #print(get_salones("Universidad de Montevideo"))

# ALUMNOS
# create
    #print(create_alumno("Juan", "Perez", "foto", "Universidad de Montevideo", 123456))
# update
    #print(update_alumno(123456, "Universidad de Montevideo", {"nombre": "Juan2"}))
# get
    #print(get_alumno(123456, "Universidad de Montevideo"))
# delete
    #print(delete_alumno(123456, "Universidad de Montevideo"))
    

# USUARIOS
# create
    #print(create_usuario("Matias", "Perez", "12345", 1, "mail2@gmail.com", "Universidad de Montevideo"))
# update
    #print(update_usuario("mail@gmail.com", "Universidad de Montevideo", {"nombre": "Juan2"}))
# login
    #print(login("mail2@gmail.com","12345"))
# get
    #print(get_usuario("mail@gmail.com", "Universidad de Montevideo"))
    print(get_usuarios_universidad("Universidad de Montevideo"))
# delete
    #print(delete_usuario("mail@gmail.com", "Universidad de Montevideo"))

# CURSOS
# create
    #print(create_curso("Curso 1", "Universidad de Montevideo", "2021-10-10", "2021-11-11", ["L205"], ["10:00"],["12:00"], ["Lunes"]))
# update
    #print(update_curso("Curso 1", "Universidad de Montevideo", {"nombre": "Curso 2"}))
# get
    #print(get_curso("Curso 2", "Universidad de Montevideo"))
# add
    #print(add_alumno("Curso 2", "Universidad de Montevideo", 123456))
    #print(add_profesor("Curso 2", "Universidad de Montevideo", "profe@gmail.com"))
    #print(add_horario("Curso 2", "Universidad de Montevideo", ["L205", "L104"], ["10:00", "11:00"], ["12:00", "13:00"], ["Martes", "Viernes"]))
# delete
    #print(delete_curso("Curso 2", "Universidad de Montevideo"))
    #print(remove_alumno("Curso 2", "Universidad de Montevideo", 123456))
    #print(remove_profesor("Curso 2", "Universidad de Montevideo", "mail@gmail.com"))
    #print(remove_horario("Curso 2", "Universidad de Montevideo", ["L205"], ["10:00"], ["12:00"], ["Martes"]))

    #print(get_cursos_profesor("profe@gmail.com"))    

# CLASES
# create
    #print(create_clase("2021-10-10-10-00", "Curso 2", "Universidad de Montevideo"))
# update
    #print(update_clase("2021-10-10-10-00", "Curso 2", "Universidad de Montevideo", {"fecha": "2021-10-10-11-00"}))
# delete
    #print(delete_clase("2021-10-10-11-00", "Curso 2", "Universidad de Montevideo"))
# get
    #print(get_clase("2021-10-10-11-00", "Curso 2", "Universidad de Montevideo"))
    #print(get_clases("Curso 2", "Universidad de Montevideo"))
    #print(get_clases_curso("Curso 2", "Universidad de Montevideo"))
    
    
    
    pass