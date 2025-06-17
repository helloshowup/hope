# 6.5
# **Testing and Debugging Programs**

## **Learning Objectives**

By the end of this session, you'll be able to:
- Identify and fix common programming errors
- Apply a systematic debugging process
- Test programs with different inputs

### **Lesson Podcast Discussion: The Importance of Systematic Debugging**

This podcast explores how a structured debugging approach helps programmers efficiently identify and solve problems in their code.

## **Common Programming Errors**

When programming robots, several types of errors commonly occur. Understanding these error types helps you identify and fix them quickly.

### **Syntax Errors**

**Syntax errors** occur when your code doesn't follow the rules of the programming language. These are usually caught by the compiler or interpreter before your program runs. Examples include:
- Missing punctuation (like semicolons or parentheses)
- Misspelled commands
- Incorrect capitalization
- Using incorrect formatting

Think of syntax errors like spelling or grammar mistakes in writing. Just as your teacher might mark these errors in your essay, the computer marks these errors in your code. For example, if you wrote `forwrd()` instead of `forward()`, the computer would show a syntax error because it doesn't recognize the misspelled command.

### **Logic Errors**

**Logic errors** are mistakes in the program's design that cause it to behave incorrectly. These errors don't prevent the program from running but cause incorrect results. Examples include:
- Using the wrong operator (+ instead of -)
- Incorrect sequence of commands
- Faulty conditional statements (if/else)
- Infinite loops

Logic errors can be tricky because your program runs without error messages, but it doesn't do what you want. Imagine you're giving directions to a friend: "Turn left at the stop sign, then right at the traffic light." If you meant to say "Turn right at the stop sign," your friend would follow your directions perfectly but end up in the wrong place. That's similar to a logic error in programming.

### **Runtime Errors**

**Runtime errors** occur while your program is running. These can cause your program to crash or produce unexpected results. Examples include:
- Dividing by zero
- Accessing variables or functions that don't exist
- Running out of memory
- Trying to perform impossible actions (like telling a robot to move through a wall)

Runtime errors happen when your code tries to do something impossible. It's like if you tried to divide 10 by 0 on your calculator - the calculator would show an error because division by zero isn't possible. Similarly, if your robot program tries to move through a wall, you'll get a runtime error because the robot can't physically do that.

---pagebreak---

## **The Debugging Process**

**Debugging** is a systematic process for finding and fixing errors in your programs. Following a structured approach makes debugging more efficient and effective.

### **Step 1: Reproduce the Problem**

Before you can fix a bug, you need to consistently reproduce it. Try to identify:
- What specific inputs or conditions cause the error
- Whether the error happens every time or only occasionally
- The exact sequence of steps that lead to the error

The first step in solving any problem is understanding exactly when and how it happens. If your robot only turns the wrong way sometimes, try to figure out what's different about those times. Does it happen when the robot is moving fast? Does it happen when the battery is low? Being a good detective at this stage saves a lot of time later!

### **Step 2: Identify the Expected vs. Actual Behavior**

Clearly define:
- What your program should be doing
- What it's actually doing instead
- The specific point where behavior deviates from expectations

In this step, you need to be very clear about what's going wrong. Instead of saying "My robot program isn't working," be specific: "My robot should turn right and then move forward 5 steps, but instead it turns right and moves forward continuously without stopping." The more precise you are about the difference between what should happen and what is happening, the easier it will be to find the problem.

### **Step 3: Locate the Source of the Error**

Use these techniques to narrow down where the error occurs:
- Add print statements to show variable values at different points
- Comment out sections of code to isolate the problem
- Use a debugger tool if available
- Check your code against a working example

Now it's time to find exactly where in your code the problem is happening. One helpful technique is adding "print" statements that show what's happening at different points in your program. For example, if your robot is supposed to stop after 5 steps but keeps going, you could add code to print out the step count. You might discover that the counter isn't increasing properly, or that the condition to stop is written incorrectly.

### **Step 4: Fix the Error and Test**

Once you've found the error:
- Make a single change to fix the problem
- Test to make sure the fix works
- Check that your fix didn't create new problems

When fixing errors, it's best to make one change at a time and then test your program. This way, you'll know exactly which change fixed the problem. Sometimes fixing one problem can create new ones, so always test your program thoroughly after making changes. It's like fixing a bicycle - if you adjust the brakes, you should test them before riding down a big hill!

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

---pagebreak---

## **Testing with Different Scenarios**

Thorough testing involves checking how your program behaves under different conditions.

### **Test Case Design**

Good test cases should:
- Cover both typical and edge cases
- Include valid and invalid inputs
- Test boundary conditions (like minimum and maximum values)
- Check all possible paths through your code

When designing tests for your robot program, think about all the different situations your robot might encounter. For example, if your robot is programmed to follow a line, you should test it on straight lines, curved lines, and intersections. You should also test what happens if there's no line at all, or if the line has a gap in it. By testing these different scenarios, you can make sure your program works in all situations, not just the easy ones.

### **Creating a Test Plan**

A systematic test plan includes:
1. A list of specific scenarios to test
2. The expected outcome for each scenario
3. A way to verify the actual results
4. Documentation of any discrepancies

A test plan is like a checklist for your program. For a robot maze-solving program, your test plan might include tests like: "Robot reaches the end of a straight path," "Robot correctly turns at a T-junction," and "Robot doesn't crash into walls." For each test, write down what should happen and then check if your program actually does it. Keep track of any tests that fail so you know what to fix.

### **Automated vs. Manual Testing**

- **Manual testing**: You personally run the program and observe its behavior
- **Automated testing**: Write additional code that automatically tests your program
- Both approaches are valuable - manual testing helps you understand the user experience, while automated testing can quickly check many different scenarios

There are two main ways to test your programs. Manual testing is when you run your program yourself and watch what happens. This is like playing a video game to see if it's fun. Automated testing is when you write another program to test your main program. This is like having a robot play the video game for you, trying every possible move to make sure nothing breaks. Both types of testing are important - manual testing helps you see how your program feels to use, while automated testing can check many more situations much faster.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about a time when you encountered a problem in a program or game. How did you approach solving it? Consider how a systematic debugging process might have made finding the solution easier.
---stopandreflectEND---

## **Improving Your Programs**

Debugging isn't just about fixing errors—it's also an opportunity to improve your code.

### **Code Refactoring**

After fixing bugs, consider:
- Simplifying complex sections
- Breaking long functions into smaller ones
- Improving variable names for clarity
- Adding comments to explain tricky parts

Refactoring is like cleaning and organizing your room. Even if everything works, it can still be messy and hard to find things. When you refactor code, you make it cleaner and easier to understand without changing what it does. For example, if you have a long section of code that makes your robot dance, you might break it into smaller parts like "spinMove()", "jumpMove()", and "waveMove()". This makes your code easier to read and easier to fix if something goes wrong later.

### **Defensive Programming**

Prevent future bugs by:
- Adding error checking for unusual situations
- Validating input values before using them
- Creating clear error messages
- Using consistent formatting and styles

Defensive programming is like wearing a helmet when you ride a bike - it helps protect you from problems before they happen. For example, if your program asks the user to enter a number between 1 and 10, you should check that they actually entered a number in that range. If they enter 0 or 11 or "banana," your program should display a helpful message instead of crashing. By planning for things that might go wrong, you make your programs more reliable and user-friendly.

---checkyourunderstanding---
What is the first step in debugging a program that isn't working?

A. Start over with a new program

B. Ask someone else to fix it

C. Identify exactly what's happening versus what should happen

D. Add more code to fix the problem
---answer---
The correct answer is C. Identify exactly what's happening versus what should happen. Effective debugging starts with clearly understanding the problem by identifying the difference between the current behavior and the expected behavior. If you chose A, starting over is rarely the most efficient approach. If you chose B, while collaboration is valuable, you should first try to understand the problem yourself. If you chose D, adding more code without understanding the issue often makes the problem worse.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- Debugging is a normal part of programming that all developers experience, not a sign of failure
- Systematic testing helps identify programming errors more quickly and efficiently than random attempts
- Small, incremental tests make debugging easier by isolating problems to specific sections of code