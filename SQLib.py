import psycopg2

#Registring using SQL database
def registration_sql(stu_id, name, dep, course_id, credit, hours, cursor, conn):
    """Insert Student Registration Information into PostgreSQL"""
    try:
        cursor.execute(
            "INSERT INTO students (student_id, name, department, course_id) VALUES (%s, %s, %s, %s)",
            (stu_id, name, dep, course_id)
        )
        cursor.execute(
            "INSERT INTO course (course_id, credits, hours, student_id) VALUES (%s, %s, %s, %s)",
            (course_id, credit, hours, stu_id)
        )
        conn.commit()
        print("Student registered successfully in PostgreSQL!")

    except Exception as e:
        print(f"Error during SQL insertion: {str(e)}")

#Printing information from SQL database
def printStudentInfo_sql(cursor):
    combStudent = []
    combCourse = []
    combined_data = []
    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        
        cursor.execute("SELECT * FROM course")
        rows1 = cursor.fetchall()
        
        print("\nPostgreSQL Students Table")
        for row in rows:
            print(row[0], '\t',row[1], '\t',row[2], '\t',row[3], '\t')
            combStudent.append([row[0], row[1], row[2]])

        print("\nPostgreSQL Course Table")
        for row in rows1:
            print(row[0], '\t',row[1], '\t',row[2], '\t',row[3], '\t')
            combCourse.append([row[0], row[1], row[2]])
        
        for student, course in zip(combStudent, combCourse):
            combined_data.append(student + course)    
        return combined_data
    
    except Exception as e:
        print(f"Error retrieving data: {e}")

#Deleting information from SQL database
def delete_personal_info_sql(cursor, conn, stu_id):
        try:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (stu_id,))
            cursor.execute("DELETE FROM course WHERE student_id = %s", (stu_id,))
            conn.commit()
            print("Student information deleted successfully from PostgreSQL!")
            
        except Exception as e: 
            print(f"An error occurred while deleting student information: {e}")

#Updating information to SQL database
def update_personal_info_sql(cursor, conn, stu_id, credits, hours):
    try:
        cursor.execute("SELECT course_id FROM students WHERE student_id = %s", (stu_id,))
        result = cursor.fetchone()
        cursor.execute("UPDATE course SET credits = %s WHERE course_id = %s", (credits, result))
        cursor.execute("UPDATE course SET hours = %s WHERE course_id = %s", (hours, result))

        conn.commit()
        print("Student information updated successfully from PostgreSQL!")

    except Exception as e: 
            print(f"An error occurred while updating course information: {e}")

