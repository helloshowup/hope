# Admin
Module 6
Lesson 5
Lesson Title: Testing and Debugging Programs
# Template
[start of lesson]
# 6.5
# Testing and Debugging Programs
## Learning Objectives
By the end of this session, you'll be able to:
- Identify and fix common programming errors
- Apply a systematic debugging process
- Test programs with different inputs
### Lesson Podcast Discussion: The Importance of Systematic Debugging
This podcast explores how a structured debugging approach helps programmers efficiently identify and solve problems in their code.
## Common Programming Errors
When programming robots, several types of errors commonly occur. Understanding these error types helps you identify and fix them quickly.

### Syntax Errors
Syntax errors occur when your code doesn't follow the rules of the programming language. These are usually caught by the compiler or interpreter before your program runs. Examples include:
- Missing punctuation (like semicolons or parentheses)
- Misspelled commands
- Incorrect capitalization
- Using incorrect formatting

### Logic Errors
Logic errors are mistakes in the program's design that cause it to behave incorrectly. These errors don't prevent the program from running but cause incorrect results. Examples include:
- Using the wrong operator (+ instead of -)
- Incorrect sequence of commands
- Faulty conditional statements (if/else)
- Infinite loops

### Runtime Errors
Runtime errors occur while your program is running. These can cause your program to crash or produce unexpected results. Examples include:
- Dividing by zero
- Accessing variables or functions that don't exist
- Running out of memory
- Trying to perform impossible actions (like telling a robot to move through a wall)

## The Debugging Process
Debugging is a systematic process for finding and fixing errors in your programs. Following a structured approach makes debugging more efficient and effective.

### Step 1: Reproduce the Problem
Before you can fix a bug, you need to consistently reproduce it. Try to identify:
- What specific inputs or conditions cause the error
- Whether the error happens every time or only occasionally
- The exact sequence of steps that lead to the error

### Step 2: Identify the Expected vs. Actual Behavior
Clearly define:
- What your program should be doing
- What it's actually doing instead
- The specific point where behavior deviates from expectations

### Step 3: Locate the Source of the Error
Use these techniques to narrow down where the error occurs:
- Add print statements to show variable values at different points
- Comment out sections of code to isolate the problem
- Use a debugger tool if available
- Check your code against a working example

### Step 4: Fix the Error and Test
Once you've found the error:
- Make a single change to fix the problem
- Test to make sure the fix works
- Check that your fix didn't create new problems

## **Activity 1: Debug Detective**
Examine the following robot program that should move forward, turn right, and then move forward again to reach a destination. However, it's not working correctly. Identify at least three errors in the code and explain how you would fix each one.


function moveRobot() {
  forward(steps: 5);
  turnleft();
  forward(10 steps);
  if (atDestination = true) {
    celebrate();
  }
}


Try to identify syntax errors, logic errors, and any other issues that would prevent this program from working correctly.

## Testing with Different Scenarios
Thorough testing involves checking how your program behaves under different conditions.

### Test Case Design
Good test cases should:
- Cover both typical and edge cases
- Include valid and invalid inputs
- Test boundary conditions (like minimum and maximum values)
- Check all possible paths through your code

### Creating a Test Plan
A systematic test plan includes:
1. A list of specific scenarios to test
2. The expected outcome for each scenario
3. A way to verify the actual results
4. Documentation of any discrepancies

### Automated vs. Manual Testing
- **Manual testing**: You personally run the program and observe its behavior
- **Automated testing**: Write additional code that automatically tests your program
- Both approaches are valuable - manual testing helps you understand the user experience, while automated testing can quickly check many different scenarios

## Stop and reflect

**CHECKPOINT:** Think about a time when you encountered a problem in a program or game. How did you approach solving it? Consider how a systematic debugging process might have made finding the solution easier.

## Improving Your Programs
Debugging isn't just about fixing errors—it's also an opportunity to improve your code.

### Code Refactoring
After fixing bugs, consider:
- Simplifying complex sections
- Breaking long functions into smaller ones
- Improving variable names for clarity
- Adding comments to explain tricky parts

### Defensive Programming
Prevent future bugs by:
- Adding error checking for unusual situations
- Validating input values before using them
- Creating clear error messages
- Using consistent formatting and styles

### Check your understanding
What is the first step in debugging a program that isn't working?
A. Start over with a new program
B. Ask someone else to fix it
C. Identify exactly what's happening versus what should happen
D. Add more code to fix the problem

Choose your answer and check it below.

The correct answer is C. Identify exactly what's happening versus what should happen. Effective debugging starts with clearly understanding the problem by identifying the difference between the current behavior and the expected behavior. If you chose A, starting over is rarely the most efficient approach. If you chose B, while collaboration is valuable, you should first try to understand the problem yourself. If you chose D, adding more code without understanding the issue often makes the problem worse.

## Key Takeaways
- Debugging is a normal part of programming that all developers experience, not a sign of failure
- Systematic testing helps identify programming errors more quickly and efficiently than random attempts
- Small, incremental tests make debugging easier by isolating problems to specific sections of code
[End of Lesson]

## Instructional designer notes of lesson 6.5
**This lesson fits into the the overall module of Smarter Robot Instructions (Advanced Programming) in the following ways:**
- It provides essential troubleshooting skills that students will need throughout their programming journey
- It builds on the programming concepts learned in previous lessons by teaching how to identify and fix problems
- It prepares students for the more complex programming challenges in future modules
- It develops critical thinking skills as students learn to systematically analyze and solve problems

**This lesson could be followed by this game:**
Debug challenge - Students compete to identify and fix errors in provided programs. For example, provide 3-5 robot programs with various types of errors (syntax errors, logic errors, and runtime errors). Students work individually or in teams to identify all the errors and fix them in the shortest time. Programs could include errors like incorrect loop conditions, missing or extra brackets, incorrect function calls, or logical sequence errors in robot movement instructions.