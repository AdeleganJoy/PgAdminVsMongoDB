import pymongo

#Inserting a student informatioon to student table in MongoDB
def registration_noSql(stu_id, name, dep, course_id, credit, hours, students):
    """Insert Student Registration Information into MongoDB"""
    try:
        students.insert_one({  
            'student_id': stu_id,  
            'name': name,  
            'department': dep,  
            'course': {  
                'course_id': course_id,  
                'credits': credit,  
                'hours': hours,  
            }  
        })
        print("Student registered successfully in MongoDB!")
        
    except pymongo.errors as e:
        print("Unexpected Error: " + str(e))

#Printing information from the student table in MongoDB
def printStudentInfo_noSql(students):
    """Printing Student Registration Information from MongoDB"""
    combine_data = []
    print("\nMongoDB Student Table")
    try:
        cursor = students.find()
        for student in cursor:
            course = student.get('course', {})
            print(
                student.get('student_id', 'N/A'), "\t",
                student.get('name', 'N/A'), "\t",
                student.get('department', 'N/A'), "\t",
                course.get('course_id', 'N/A'), "\t",
                course.get('credits', 'N/A'), "\t",
                course.get('hours', 'N/A')
            )
            combine_data.append([
                student.get('student_id', 'N/A'),
                student.get('name', 'N/A'),
                student.get('department', 'N/A'),
                course.get('course_id', 'N/A'),
                course.get('credits', 'N/A'),
                course.get('hours', 'N/A')
            ])
        return combine_data

    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")

#Deleting a student from the student table in MongoDB
def delete_personal_info_noSQL(stu_id, students):
    """Deleting Student Registration Information from MongoDB"""
    try:
        students.delete_one({'student_id': stu_id})
        print("Student information deleted successfully from MongoDB!")
    except Exception as e: 
        print(f"An error occurred while deleting student information: {e}")

# Updating a student table in MongoDB
def update_personal_info_noSql(students, stu_id, new_credits, new_hours):
    """Updating Student Registration Information from MongoDB"""
    try:
        # Update the credits and hours for the specific student
        result = students.update_one(
            {'student_id': stu_id}, 
            {'$set': {  
                'course.credits': new_credits,  
                'course.hours': new_hours  
            }}
        )
        
        if result.matched_count > 0:
            print("Student course information updated successfully in MongoDB!")
        else:
            print("Student not found.")
    
    except Exception as e: 
        print(f"An error occurred while updating course information: {e}")
