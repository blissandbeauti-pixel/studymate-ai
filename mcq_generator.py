<<<<<<< HEAD
# ============================================
# StudyMate AI - MCQ Generator v2.0
# Interactive Version with Full Details
# ============================================


# ============================================
# PROGRAM MENU
# ============================================

def select_program():
    print("\n========================================")
    print("       Welcome to StudyMate AI 📚      ")
    print("========================================\n")
    
    programs = {
        "1": "BSN Nursing",
        "2": "DAE Civil Engineering",
        "3": "DAE Electrical Engineering",
        "4": "DAE Mechanical Engineering",
        "5": "FSc Pre-Medical",
        "6": "FSc Pre-Engineering",
        "7": "BA/BSc General",
        "8": "Other"
    }
    
    print("Select Program:")
    for key, value in programs.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("\nEnter choice (1-8): ").strip()
        if choice in programs:
            if choice == "8":
                return input("Enter your program name: ").strip()
            return programs[choice]
        print("❌ Invalid choice. Please enter 1-8.")


# ============================================
# GET STUDENT DETAILS
# ============================================

def get_student_details():

    # Program selection
    program = select_program()

    # Year/Semester
    print("\n----------------------------------------")
    year = input("Enter Year/Semester (e.g. 1st Year, Semester 3): ").strip()

    # Subject
    subject = input("Enter Subject (e.g. Anatomy, Physics): ").strip()

    # Topic
    topic = input("Enter Topic (e.g. Cardiovascular System): ").strip()

    # Number of questions
    print("\nNumber of Questions:")
    print("  1. 5 Questions")
    print("  2. 10 Questions")
    print("  3. 15 Questions")
    print("  4. 20 Questions")
    
    q_map = {"1": 5, "2": 10, "3": 15, "4": 20}
    while True:
        q_choice = input("\nEnter choice (1-4): ").strip()
        if q_choice in q_map:
            num_questions = q_map[q_choice]
            break
        print("❌ Invalid choice. Please enter 1-4.")

    # Difficulty
    print("\nDifficulty Level:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")
    
    d_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
    while True:
        d_choice = input("\nEnter choice (1-3): ").strip()
        if d_choice in d_map:
            difficulty = d_map[d_choice]
            break
        print("❌ Invalid choice. Please enter 1-3.")

    return program, year, subject, topic, num_questions, difficulty


# ============================================
# GENERATE MCQs
# ============================================

def generate_mcqs(program, year, subject, topic, num_questions, difficulty):

    prompt = f"""
    You are an expert educator for {program} students in Pakistan.
    
    Student Details:
    - Program : {program}
    - Year/Semester : {year}
    - Subject : {subject}
    - Topic : {topic}
    - Difficulty : {difficulty}
    
    Generate {num_questions} high quality MCQs strictly based on 
    Pakistani curriculum and HEC guidelines.
    
    Format EACH MCQ exactly like this:
    
    Q[number]. [Clear, specific question]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    ✅ Correct Answer: [Letter]) [Answer text]
    📝 Explanation: [1 clear line explaining why this is correct]
    🔑 Key Note: [1 important point student must remember]
    
    ---
    
    Rules:
    - Questions must match {difficulty} difficulty level
    - All questions relevant to {program} {year} level
    - No repeated concepts
    - Explanations must be simple and clear
    - Key notes must be exam-focused
    """

    from ai_backend import chat
    return chat(prompt)

    return response["message"]["content"]


# ============================================
# DISPLAY HEADER
# ============================================

def display_header(program, year, subject, topic, difficulty, num_questions):
    print("\n\n========================================")
    print("     📚 StudyMate AI - MCQ Generator    ")
    print("========================================")
    print(f"  Program    : {program}")
    print(f"  Year       : {year}")
    print(f"  Subject    : {subject}")
    print(f"  Topic      : {topic}")
    print(f"  Difficulty : {difficulty}")
    print(f"  Questions  : {num_questions}")
    print("========================================\n")


# ============================================
# MAIN PROGRAM
# ============================================

def main():
    # Get all details from student
    program, year, subject, topic, num_questions, difficulty = get_student_details()

    # Show what we're generating
    print("\n⏳ Generating your MCQs... Please wait")
    print("(This may take 1-2 minutes)\n")

    # Generate MCQs
    result = generate_mcqs(program, year, subject, topic, num_questions, difficulty)

    # Display header
    display_header(program, year, subject, topic, difficulty, num_questions)

    # Display MCQs
    print(result)

    # Footer
    print("\n========================================")
    print("     ✅ MCQs Generated Successfully!    ")
    print("  StudyMate AI | Good Luck with Exams  ")
    print("========================================\n")

    # Ask to generate more
    again = input("Generate more MCQs? (yes/no): ").strip().lower()
    if again in ["yes", "y"]:
        main()
    else:
        print("\n👋 Good luck with your studies!\n")
    # Run the program
main()