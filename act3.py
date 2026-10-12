import copy

# constants
PASSING_GRADE = 75
MIN_GRADE = 0
MAX_GRADE = 100



class Student:
    
    def __init__(self, StudentId, Name, Program, YearLevel):
        # Using a tuple to store immutable base information
        self.Identity = (StudentId, Name)
        self.Program = Program.strip().upper()  
        self.YearLevel = YearLevel
        self.Grades = []  
        
    def AddGrade(self, Grade):
        self.Grades.append(Grade)
        
    def CalculateAverage(self):
        """Calculates the average of the student's grades."""
        if not self.Grades:
            return 0.0
        
        Total = sum(self.Grades)
        Average = Total / len(self.Grades)
        return Average
        
    def GetStatus(self):

        Avg = self.CalculateAverage()
        
        if Avg >= 90:
            return "Excellent"
        elif Avg >= 85:
            return "Very Good"
        elif Avg >= 80:
            return "Good"
        elif Avg >= 75:
            return "Passed"
        else:
            return "Failed"
            
    def DisplayInfo(self):
        StudentId, Name = self.Identity
        Avg = self.CalculateAverage()
        Status = self.GetStatus()
        print(f"ID: {StudentId} | Name: {Name} | Program: {self.Program} | Year: {self.YearLevel}")
        print(f"Grades: {self.Grades} | Average: {Avg:.2f} | Status: {Status}")

class ScholarshipStudent(Student):
   

    def __init__(self, StudentId, Name, Program, YearLevel, RequiredAverage):
        # Inherit parent attributes
        super().__init__(StudentId, Name, Program, YearLevel)
        self.RequiredAverage = RequiredAverage  
        
    def CheckQualification(self):
        # checks if qualified for scholarship
        Avg = self.CalculateAverage()
        
        IsQualified = Avg >= self.RequiredAverage 
        
        if IsQualified:
            print(f"{self.Identity[1]} QUALIFIES to keep the scholarship. (Avg: {Avg:.2f} >= Req: {self.RequiredAverage})")
        else:
            print(f"{self.Identity[1]} DOES NOT QUALIFY to keep the scholarship. (Avg: {Avg:.2f} < Req: {self.RequiredAverage})")


# --- FUNCTIONS ---

# Global Dictionary 
StudentDb = {}

def GetHighestGradeRecursive(GradesList):
    
    if not GradesList:
        return 0

    if len(GradesList) == 1:
        return GradesList[0]
        
    MaxInRest = GetHighestGradeRecursive(GradesList[1:])
    return GradesList[0] if GradesList[0] > MaxInRest else MaxInRest

def AddStudent():

    print("\n--- Register Student ---")
    StudentId = input("Enter Student ID: ").strip().upper()
    
    if StudentId in StudentDb:
        print("Error: Student ID already exists!")
        return

    Name = input("Enter Name: ").strip().title()
    Program = input("Enter Program: ").strip().upper()
    YearLevel = input("Enter Year Level: ").strip()
    
    IsScholar = input("Is this a scholarship student? (Y/N): ").strip().upper()
    
    if IsScholar == 'Y':
        try:
            ReqAvg = float(input("Enter Required Average: "))
            NewStudent = ScholarshipStudent(StudentId, Name, Program, YearLevel, ReqAvg)
        except ValueError:
            print("Invalid input for average. Registration failed.")
            return
    else:
        NewStudent = Student(StudentId, Name, Program, YearLevel)
        
    StudentDb[StudentId] = NewStudent
    print(f"Student {Name} registered successfully!")

def AddGradeToStudent():
    print("\n--- Add Grades ---")
    StudentId = input("Enter Student ID: ").strip().upper()
    
    # check if ID is not in StudentDb
    if StudentId not in StudentDb:
        print("Error: Student not found!")
        return
        
    StudentObj = StudentDb[StudentId]
    
    while True:
        Entry = input("Enter grade (or type 'done' to finish): ").strip().lower()
        if Entry == 'done':
            break
            
        try:
            Grade = float(Entry)
            # Validate grades from constants MIN_GRADE and MAX_GRADE
            if Grade < MIN_GRADE or Grade > MAX_GRADE:
                print(f"Invalid grade! Please enter a value between {MIN_GRADE} and {MAX_GRADE}.")
                continue 
            
            StudentObj.AddGrade(Grade)
            print(f"Grade {Grade} added to {StudentObj.Identity[1]}.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def ViewAllStudents():
    print("\n--- All Students ---")
    if not StudentDb:
        print("No students registered yet.")
        return
        
    for StudentId, StudentObj in StudentDb.items():
        print("-" * 30)
        StudentObj.DisplayInfo()

def SearchForStudent():
    print("\n--- Search Student ---")
    StudentId = input("Enter Student ID: ").strip().upper()
    
    if StudentId in StudentDb:
        StudentDb[StudentId].DisplayInfo()
    else:
        print("Student not found.")

def CalculateStudentAvg():
    print("\n--- Calculate Average ---")
    StudentId = input("Enter Student ID: ").strip().upper()
    
    if StudentId in StudentDb:
        StudentObj = StudentDb[StudentId]
        Avg = StudentObj.CalculateAverage()
        print(f"Student: {StudentObj.Identity[1]} | Average: {Avg:.2f} | Status: {StudentObj.GetStatus()}")
    else:
        print("Student not found.")

def DisplayTopStudent():
    print("\n--- Top Performing Student ---")
    if not StudentDb:
        print("No students registered yet.")
        return
        
    TopStudent = None
    HighestAvg = -1
    
    for StudentObj in StudentDb.values():
        Avg = StudentObj.CalculateAverage()
        if Avg > HighestAvg:
            HighestAvg = Avg
            TopStudent = StudentObj
            
    if TopStudent:
        print("Top Student Award Goes To:")
        TopStudent.DisplayInfo()

def CheckScholarshipQualification():
    print("\n--- Scholarship Check ---")
    StudentId = input("Enter Student ID: ").strip().upper()
    
    if StudentId in StudentDb:
        StudentObj = StudentDb[StudentId]
        if isinstance(StudentObj, ScholarshipStudent):
            StudentObj.CheckQualification()
        else:
            print(f"{StudentObj.Identity[1]} is a Regular Student, not a Scholarship Student.")
    else:
        print("Student not found.")

def DemoRecursion():
    print("\n--- Demonstrate Recursion ---")
    StudentId = input("Enter Student ID to find their highest grade: ").strip().upper()
    
    if StudentId in StudentDb:
        StudentObj = StudentDb[StudentId]
        if not StudentObj.Grades:
            print(f"No grades recorded for {StudentObj.Identity[1]}.")
        else:
            Highest = GetHighestGradeRecursive(StudentObj.Grades)
            print(f"Grades: {StudentObj.Grades}")
            print(f"Highest grade: {Highest}")
    else:
        print("Student not found.")

def DemoMutableImmutable():
    print("\n--- Mutable vs. Immutable & Assignment Semantics ---")
    
    #mutable lists
    print("Part 1: Lists (Mutable) and Assignment")
    OriginalList = [85, 90, 88]
    ReferenceList = OriginalList         
    CopiedList = list(OriginalList)      
    
    OriginalList.append(95)             
    
    print(f"Original List (mutated): {OriginalList}")
    print(f"Reference List (a = b):  {ReferenceList} <- Changed too, because it points to the same object.")
    print(f"Copied List (a = list(b)): {CopiedList} <- Untouched, because it's a separate copy.")
    
    # immutable strings
    print("\nPart 2: Strings (Immutable)")
    MyString = "hello"
    print(f"Original String: {MyString}")
    print("Strings cannot be changed in place (immutable). Functions like upper() create a NEW string.")
    
    NewString = MyString.upper()
    print(f"MyString is still: {MyString}")
    print(f"NewString is: {NewString}")
    print("Trying to execute MyString[0] = 'H' would raise a TypeError.")


def Main():
    while True:
        # Program Menu
        print("\n")
        print(" STUDENT PERFORMANCE MANAGEMENT SYSTEM")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. View All Students")
        print("4. Search Student")
        print("5. Calculate Student Average")
        print("6. Display Top Student")
        print("7. Check Scholarship Qualification")
        print("8. Demonstrate Recursion")
        print("9. Demonstrate Mutable and Immutable Types")
        print("10. Exit")
        
        Choice = input("\nEnter your choice: ").strip()
        
        if Choice == '1':
            AddStudent()
        elif Choice == '2':
            AddGradeToStudent()
        elif Choice == '3':
            ViewAllStudents()
        elif Choice == '4':
            SearchForStudent()
        elif Choice == '5':
            CalculateStudentAvg()
        elif Choice == '6':
            DisplayTopStudent()
        elif Choice == '7':
            CheckScholarshipQualification()
        elif Choice == '8':
            DemoRecursion()
        elif Choice == '9':
            DemoMutableImmutable()
        elif Choice == '10':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please select from 1-10.")

if __name__ == "__main__":
    Main()