'''
Created on Mar 30, 2020

@author: Elif_Kaya_HW12 Kaya 

Estimate number of students eligible for a course, based on files in a directory
'''

#Import necessary libraries
import os 

def processProgramFile(file_path): 
    '''
    Produces a dictionary based on the information in the file
    
    :param file_path: provides the path to a program description file
    :return: dictionary of programs numbers with their names
    
    '''
    #Open and read the file lines
    file = open(file_path, 'r')
    file_lines = file.readlines()

    #Loop through the file lines to create a dictionary with course numbers as keys, names as values 
    programs = {}
    for line in file_lines[1:]: #start looping after the course number till the end
        
        if len(line.strip()) != 0: # Ignore empty lines
            new_list = line.strip().split()
            programs[new_list[0]] = " ".join(new_list[1:]) #join the elements from second to end in list to have full course name
                    
    return programs



def processPrereqsFile(prereqs_file):
    '''
    Read information about the prerequisites and construct a dictionary for classes that only have prerequisites
    keys equal to the course number, and values for keys equal to the corresponding prerequisite courses
    
    :param prereqs_file: path to a file defining prerequisites
    :return dictionary of classes with their prerequisites 
    
    '''
    
    #Open and read the file lines
    file = open(prereqs_file, 'r')
    file_lines = file.readlines()
    
    #Loop through the file find the class with prerequisites and store it in a dictionary, class as key and the prereqs as values
    prerequisites = {}
    for line in file_lines: 
        prereqs_file_lines = line.strip().split(":") #Split the lines from the :
        
        if len(prereqs_file_lines[1].strip()) != 0: #Check if the line has a value 
            splitted_lines = prereqs_file_lines[1].strip().split() #Extract the part that has prerequisites
            prerequisites[prereqs_file_lines[0]] = splitted_lines
    
    return prerequisites    
 

def processClassFiles(class_path):
    '''
    Create a single dictionary that combines enrollments into courses from multiple files organized by course number
    
    :param class_path: subfolder with the class list files
    :return: dictionary with course and list of students
    
    '''
    
    #get all the files in the defined subfolder
    all_files = os.listdir(class_path)
    
    #We only need the class files therefore we ignore the ones we need to exclude
    files_to_ignore = ["program1.txt", "program2.txt", "prereqs.txt"]
    
    #Loop through all the files to find students of each class
    course_list = {}
    
    for file in all_files: 
        if file not in files_to_ignore: #check if the file is in files to be excluded list and read the file 
            with open(os.path.join(class_path, file),"r") as f: #
                all_lines = f.readlines()
                course_numbers = all_lines[0].strip().replace("c", "") #get rid of the c in course numbers

                #Create a list where the student names will be stored
                student_names = []
                for line in all_lines[1:]: #exclude the course number while we loop
                    split_list = line.strip().split()
                    student_names.append(split_list[0]) #add the student names only to our student_names

                if course_numbers in course_list:
                    course_list[course_numbers]  = student_names + course_list[course_numbers]                
                else: 
                    course_list[course_numbers] = student_names

    
    return course_list


def initFromFiles(sub_folder):
    '''
    create data structures by calling the functions identified above
    
    :param:  sub_folder: the subfolder with the files
    :return: school information tuple
    
    '''
    
    #Read in both program1 and program2 files
    programs_1 = processProgramFile(os.path.join(sub_folder, 'program1.txt')) 
    programs_2 = processProgramFile(os.path.join(sub_folder, 'program2.txt'))
    
    #combine both dictionaries 
    programs =  {**programs_1, **programs_2}
    
    #Join the subfolder file path with prerequisites file
    prerequisites = processPrereqsFile(os.path.join(sub_folder, 'prereqs.txt'))
    class_list = processClassFiles(sub_folder)
    
    #create a tuple 
    school_info = programs, prerequisites, class_list
    
    return school_info


def estimateClass(course_number, school_info):
    '''
    find a list of eligible students for a given class and return a sorted list
    
    :param course_number: takes the course number that needs to be checked 
    :param school_info: program names, prerequisite and class list
    :return: sorted list of students    
    '''
    
    #unpack course information 
    programs, prerequisites, class_list = school_info
    
    #check if course number is a valid course number if not return and empty list
    if course_number not in class_list:
        return list()
    
    
    #If course number has prerequisites then get the intersection of students in prerequisites 
    elif course_number in prerequisites:
        course_prereqs = prerequisites[course_number]

        #Find the list of students who took prerequisite class
        all_student_list = []
        for course in course_prereqs:
            if course in class_list:
                all_student_list.append(class_list[course])
    

        if len(course_prereqs) == 1:
            student_set = set(all_student_list[0]) - set(class_list[course_number]) #subtract the ones who have already taken the class
            return sorted(student_set)
        
        else: 
            
            final_list = set(all_student_list[0])
            
            for l in all_student_list[1:]:
                final_list = final_list.intersection(l)
            return sorted(final_list - set(class_list[course_number])) #subtract the ones who have already taken the class
            
    else: #find students for a class that does not have a prerequisite 
        all_students = set()
        for no_req in class_list:
            if no_req != course_number:
                all_students = all_students.union(class_list[no_req])
                

        return sorted(all_students - set(class_list[course_number])) #subtract the ones who have already taken the class


def main():
    '''
    Call the functions and ask user to enter subfoler and a course number until they hit enter
    Once the course number is entered, display how  many students can take that course next semester along with course name
    
    '''
    
    #Ask user the file path 
    file_path = input('Please enter the name of the subfolder with files: ')
    full_path = os.path.join(os.getcwd(), file_path)
    
    #Verify if the path is a valid directory
    while not os.path.isdir(full_path):
        file_path = input('Please enter the name of the subfolder with files: ')
        full_path = os.path.join(os.getcwd(), file_path)

        
    school_info = initFromFiles(file_path)    
    
    #ask user a course name until they hit enter
    course_number = input('Enter course number or press enter to stop:')
    
    while course_number != "":
        students = estimateClass(course_number, school_info)
        
        course_name = school_info[0][course_number] if course_number in school_info[0] else None
        print("There are", len(students),\
              "students who could take course", course_number, course_name )       
                               
        course_number = input('Enter course number or press enter to stop:')
        

#Call main function
main() 
 

        
        
        
        