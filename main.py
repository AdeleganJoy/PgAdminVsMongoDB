import pymongo
import psycopg2
import noSQLib as noSQL
import SQLib as SQL

def delete_personal_info():
    while True:
        stu_id = input("Enter student ID (e.g., 12345): ")
        if len(stu_id) == 5 and stu_id.isdigit():
            # Check if the student exists in both databases
            nosqlCheck = students.find_one({'student_id': stu_id}) is not None
            cursor.execute("SELECT EXISTS (SELECT 1 FROM students WHERE student_id = %s)", (stu_id,))
            sqlCheck = cursor.fetchone()[0]  # True if exists

            if nosqlCheck or sqlCheck:
                # Student exists, proceed to delete
                noSQL.delete_personal_info_noSQL(stu_id, students)
                SQL.delete_personal_info_sql(cursor, conn, stu_id)
                print(f"Student ID {stu_id} successfully deleted.")
                break
            else:
                print("Student ID does not exist in the database. Please enter a valid ID.")
        else:
            print("Student ID must be a 5-digit number (e.g., 12345).")

def update_personal_info():
    while True:
        stu_id = input("Enter student ID (e.g., 12345): ")
        if len(stu_id) == 5 and stu_id.isdigit():
            # Check if the student exists in both databases
            nosqlCheck = students.find_one({'student_id': stu_id}) is not None
            cursor.execute("SELECT EXISTS (SELECT 1 FROM students WHERE student_id = %s)", (stu_id,))
            sqlCheck = cursor.fetchone()[0]  # True if exists

            if nosqlCheck or sqlCheck:
                # Student exists, proceed to update
                while True:  
                    credit = input(f"Update credit number: ")
                    if credit.isdigit() and 1 <= int(credit) <= 5:
                        break
                    else:  
                        print("Credit must be a number between 1 and 5.")

                while True:
                    hours = input(f"Update hours required: ")
                    if hours.isdigit():  
                        break
                    else:  
                        print("Hours must be a number.")

                SQL.update_personal_info_sql(cursor, conn, stu_id, credit, hours)
                noSQL.update_personal_info_noSql(students, stu_id, credit, hours)
                print(f"Student ID {stu_id} successfully updated.")
                break
            else:
                print("Student ID does not exist in the database. Please enter a valid ID.")
        else:
            print("Student ID must be a 5-digit number (e.g., 12345).")

def print_both_tables():
    try:
        noSqlInfo = noSQL.printStudentInfo_noSql(students)
        sqlInfo = SQL.printStudentInfo_sql(cursor)

        combined = noSqlInfo + sqlInfo

        unique = {item[0]: item for item in combined}
        
        print("\nCombined Tables")
        for k,v in unique.items():
            print(v[0], v[1], v[2],v[3],v[4],v[5])
        
    except Exception as e:
        print(f"Error during print of both tables: {e}")


def main_menu():
    print("\nWelcome to LUT info Page")
    print("Please select one of the following:")
    print("(1)\t Print the tables")
    print("(2)\t Insert student information")
    print("(3)\t Delete student information")
    print("(4)\t Update Course information")
    print("(0)\t Exit the program")
    choice = input("Choice: ")
    return choice

def get_personal_info():
    while True:   
        stu_id = input("Enter student ID (e.g., 12345): ")
        if len(stu_id) == 5 and stu_id.isdigit():  
            # Check if the student ID exists in both databases
            nosqlCheck = students.find_one({'student_id': stu_id}) is None
            cursor.execute("SELECT EXISTS (SELECT 1 FROM students WHERE student_id = %s)", (stu_id,))
            sqlCheck = not cursor.fetchone()[0]         

            if nosqlCheck and sqlCheck:
                break
            else:
                print("Student ID already exists in the database. Please enter a new ID.")
        else:  
            print("Student ID must be a 5-digit number (e.g., 12345).") 

    name = input("Enter name: ")
    dep = input("Enter department: ")

    while True:  
        course_id = input("Enter course identifier (e.g., 606): ")  
        if len(course_id) == 3 and course_id.isdigit():  
            break
        else:  
            print("Course ID must be a 3-digit number (e.g., 606).") 

    while True:  
        credit = input("Enter credit number for Course " + course_id + ": ")
        if credit.isdigit() and 1 <= int(credit) <= 5:  
            break
        else:  
            print("Credit must be a number between 1 and 5.")  

    while True:
        hours = input("Enter number of hours required for Course " + course_id + ": ")  
        if hours.isdigit():  
            break
        else:  
            print("Hours must be a number.") 

    return stu_id, name, dep, course_id, credit, hours



if __name__ == "__main__":  
    #NoSQL instantiation
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = myclient["LUT"]  
        students = db['lut'] 
    except Exception as e:
        print("Error connecting to MongoDB: " + str(e))

    #SQL instantiation
    try:
        conn = psycopg2.connect(database="LUT",
                                host = "localhost",
                                user = "postgres",
                                password = "*****",
                                port="5432")
        cursor = conn.cursor()

    except Exception as e:  
        print("Error connecting to the database:" +  str(e))  

    try:
        while True:
            choice = main_menu()

            if choice == "1":
                print_both_tables()

            elif choice == "2":
                #get student information
                stu_id, name, dep, course_id, credit, hours = get_personal_info()

                # Insert into NoSQL
                noSQL.registration_noSql(stu_id, name, dep, course_id, int(credit), int(hours), students)

                # Insert into SQL
                if cursor and conn:
                    SQL.registration_sql(stu_id, name, dep, course_id, int(credit), int(hours), cursor, conn)
            
            elif choice == "3":
                delete_personal_info()
            elif choice == "4":
                update_personal_info()
            elif choice == "0":
                break

            
    except Exception as e:
        print("Unexpected Error" + str(e))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        if myclient:
            myclient.close()