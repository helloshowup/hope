# Admin
Module 8
Lesson 5
Lesson Title: Testing and Debugging Programs
# Template

# 8.5
# Testing and Debugging Programs
## Learning Objectives
By the end of this session, you'll be able to:
- Identify and fix common programming errors
- Apply a systematic debugging process
- Test programs with different inputs

## Lesson Podcast Discussion: The Systematic Approach to Debugging
A conversation about how applying a structured debugging process can save time and frustration when programming robots.

## Common Programming Errors
When programming robots to help people, even small errors can cause the robot to behave unexpectedly. Understanding common errors will help you identify and fix them more efficiently.

### Syntax Errors
Syntax errors occur when your code doesn't follow the programming language's rules. These are typically caught by the programming environment before the program runs.

Examples include:
- Missing punctuation (forgetting semicolons or brackets)
- Misspelled commands or variable names
- Incorrect capitalization in languages that are case-sensitive

### Logic Errors
Logic errors are more challenging to identify because the program runs without crashing, but doesn't behave as expected.

Examples include:
- Using the wrong mathematical operator (+ instead of -)
- Creating infinite loops that never terminate
- Setting incorrect values for variables
- Writing conditions that never evaluate as expected

### Runtime Errors
Runtime errors occur while the program is running and often cause it to crash.

Examples include:
- Dividing by zero
- Accessing undefined variables
- Attempting to use resources that don't exist
- Memory overflow errors

## The Debugging Process
Debugging is a systematic approach to finding and fixing errors in your code. Following a structured process makes troubleshooting more efficient.

### Step 1: Understand the Problem
Before attempting to fix an issue, clearly identify:
- What is the robot currently doing?
- What should the robot be doing instead?
- When exactly does the problem occur?

### Step 2: Reproduce the Error
Create a reliable way to make the error happen consistently. You can't fix what you can't see.

### Step 3: Isolate the Issue
Narrow down where in your code the problem is occurring:
- Use print statements to show variable values
- Comment out sections of code to identify which part causes the problem
- Check one piece of functionality at a time

### Step 4: Fix and Test
Make one change at a time and test after each change to see if it resolves the issue.

## **Activity 1: Find the Bug**
Review the following robot navigation program that should guide a helper robot through a room to deliver medicine to a patient, but it's not working correctly:


function navigateToPatient(startPosition, patientPosition):
    current = startPosition
    path = []
    
    while current != patientPosition:
        if current.x < patientPosition.x:
            current.x += 1
        else if current.x > patientPosition.x:
            current.x -= 1
        if current.y < patientPosition.y:
            current.y += 1
        else if current.y > patientPosition.y:
            current.y -= 1
        path.append(current)
    
    return path


Identify the error in this code and determine how to fix it. Hint: The robot sometimes gets stuck moving in only one direction.

## Testing with Different Scenarios
Thorough testing is essential for creating reliable robot programs that help people safely.

### Edge Cases
Test your program with unusual or extreme inputs:
- What happens if the robot is asked to navigate to its current position?
- What if it needs to move a very long distance?
- What if obstacles are present?

### User Scenarios
Test your program based on real-world situations:
- How would different users interact with the robot?
- What if the user gives unexpected commands?
- What if the environment changes while the robot is operating?

### Systematic Testing
Create a testing plan that covers all possible scenarios:
- Start with simple, known inputs
- Progress to more complex cases
- Document results to track improvements

## Stop and reflect

**CHECKPOINT:** Think about a time when you encountered a problem with a device or application. How did you go about troubleshooting it? Did you follow steps similar to the debugging process we discussed?

## Improving Your Programs
Once your program works correctly, you can focus on making it better.

### Code Readability
Clear, well-organized code is easier to debug:
- Use meaningful variable and function names
- Add comments explaining complex sections
- Format your code consistently

### Defensive Programming
Anticipate potential problems in your code:
- Validate user inputs before processing them
- Include error handling for unexpected situations
- Add safeguards for critical operations

### Incremental Development
Build and test your program in small pieces:
- Start with a minimal working version
- Add one feature at a time
- Test thoroughly after each addition

## **Activity 2: Test Different Inputs**
Take the corrected robot navigation program from the earlier activity and test it with these different scenarios:

1. Starting and ending positions are the same
2. The robot needs to navigate around a simple obstacle
3. The destination is unreachable

For each scenario, predict what will happen, run the test, and record the results. What changes would you make to improve the program's handling of these situations?

## Stop and reflect

**CHECKPOINT:** Consider how systematic debugging differs from random trial-and-error approaches. How does having a structured debugging process help you solve programming problems more efficiently? Think about how this might apply to other types of problem-solving beyond programming.

### **Check your understanding**
What is the first step in debugging a program that isn't working?
A. Start over with a new program
B. Ask someone else to fix it
C. Identify exactly what's happening versus what should happen
D. Add more code to fix the problem

Choose your answer and check it below.

The correct answer is C. Identify exactly what's happening versus what should happen. Effective debugging starts with clearly understanding the problem by identifying the difference between the current behavior and the expected behavior. If you chose a different answer, remember that fixing a problem requires first understanding it thoroughly - adding code blindly or starting over are inefficient approaches when a systematic process can help identify the specific issue.

## Key Takeaways
- Debugging is a normal part of programming that becomes easier with practice and a systematic approach
- Systematic testing with various inputs helps uncover and address potential problems before they affect users
- Small, incremental tests and changes make debugging easier and help create more reliable programs

## Instructional designer notes of lesson 8.5
**This lesson fits into the overall module of Robots Helping People in the following ways:**
- It provides essential troubleshooting skills needed for programming reliable robot assistants
- It emphasizes the importance of thorough testing when robots interact with humans
- It builds on previous programming concepts by focusing on quality and reliability

**This lesson could be followed by this game:**
Debug challenge where students compete to identify and fix errors in provided programs. For example, students could be given a robot assistance program with 5-7 deliberately placed errors (syntax, logic, and runtime). They must identify all errors, explain the problem, and provide the correct solution within a time limit. Points would be awarded for speed, accuracy of fixes, and quality of explanations.