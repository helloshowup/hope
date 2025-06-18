# 8.5
# **Testing and Debugging Programs**

## **Learning Objectives**

By the end of this session, you'll be able to:
- Identify and fix common programming errors
- Apply a systematic debugging process
- Test programs with different inputs

## **Lesson Podcast Discussion: The Systematic Approach to Debugging**

When programming robots, things don't always work perfectly the first time. In fact, professional programmers spend a lot of their time finding and fixing problems in their code! This podcast discusses how having a step-by-step plan for finding bugs (errors) in your code can save you time and frustration. 

Just like a doctor uses a systematic approach to figure out why someone is sick, programmers use debugging techniques to diagnose what's wrong with their code. By following a clear process instead of making random changes, you can solve problems more quickly and learn from your mistakes.

## **Common Programming Errors**

When programming robots to help people, even small errors can cause the robot to behave unexpectedly. Understanding common errors will help you identify and fix them more efficiently.

### **Syntax Errors**

Syntax errors occur when your code doesn't follow the programming language's rules. These are typically caught by the programming environment before the program runs.

Examples include:
- Missing punctuation (forgetting semicolons or brackets)
- Misspelled commands or variable names
- Incorrect capitalization in languages that are case-sensitive

Think of syntax errors like spelling or grammar mistakes in writing. The computer can't understand what you're trying to say because you're not following the rules of the language. The good news is that most programming tools will point out these errors with underlines or error messages to help you fix them quickly.

### **Logic Errors**

Logic errors are more challenging to identify because the program runs without crashing, but doesn't behave as expected.

Examples include:
- Using the wrong mathematical operator (+ instead of -)
- Creating infinite loops that never terminate
- Setting incorrect values for variables
- Writing conditions that never evaluate as expected

Logic errors are like giving someone directions to your house but accidentally telling them to turn left when they should turn right. The person follows your instructions exactly, but ends up in the wrong place! These errors can be tricky because the computer doesn't know what you intended - it just follows your instructions precisely.

### **Runtime Errors**

Runtime errors occur while the program is running and often cause it to crash.

Examples include:
- Dividing by zero
- Accessing undefined variables
- Attempting to use resources that don't exist
- Memory overflow errors

Runtime errors happen when your program tries to do something impossible during execution. Imagine telling a robot to pick up an object that isn't there or asking it to move through a wall. The robot can't complete the task and has to stop. Similarly, when your program encounters a runtime error, it usually stops running and displays an error message explaining what went wrong.

---pagebreak---

## **The Debugging Process**

Debugging is a systematic approach to finding and fixing errors in your code. Following a structured process makes troubleshooting more efficient.

### **Step 1: Understand the Problem**

Before attempting to fix an issue, clearly identify:
- What is the robot currently doing?
- What should the robot be doing instead?
- When exactly does the problem occur?

This first step is crucial because you can't fix a problem if you don't understand it. Take time to observe exactly what's happening. For example, if your robot is supposed to follow a line but keeps veering off to the right, make note of exactly when and how this happens. Does it happen immediately or after a certain amount of time? Does it happen on straight sections or only on curves?

### **Step 2: Reproduce the Error**

Create a reliable way to make the error happen consistently. You can't fix what you can't see.

If you can make the error happen every time under specific conditions, you'll be able to test whether your fix actually works. For example, if your robot only crashes when it tries to turn left, create a simple test program that makes it turn left repeatedly. This helps you focus on the specific part of the code that's causing problems.

### **Step 3: Isolate the Issue**

Narrow down where in your code the problem is occurring:
- Use print statements to show variable values
- Comment out sections of code to identify which part causes the problem
- Check one piece of functionality at a time

This step is like being a detective. You're gathering clues about what might be causing the problem. Print statements are especially helpful because they let you see what's happening inside your program as it runs. For example, if your robot is turning at the wrong angle, you could add print statements to show what angle value the program is calculating.

### **Step 4: Fix and Test**

Make one change at a time and test after each change to see if it resolves the issue.

It's important to make just one change at a time. If you change multiple things and the problem is fixed, you won't know which change actually solved it! After each change, run your program to see if the error still occurs. Keep track of what you've tried so you don't repeat the same attempts.

## **Activity 1: Find the Bug**

Review the following robot navigation program that should guide a helper robot through a room to deliver medicine to a patient, but it's not working correctly:

```
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
```

Identify the error in this code and determine how to fix it. Hint: The robot sometimes gets stuck moving in only one direction.

---pagebreak---

## **Testing with Different Scenarios**

Thorough testing is essential for creating reliable robot programs that help people safely.

### **Edge Cases**

Test your program with unusual or extreme inputs:
- What happens if the robot is asked to navigate to its current position?
- What if it needs to move a very long distance?
- What if obstacles are present?

Edge cases are special situations that might not happen often but could cause big problems if not handled correctly. For example, what if someone accidentally tells your delivery robot to bring medicine to room 999, but your building only has 10 rooms? A good program should recognize this impossible request and respond appropriately instead of malfunctioning.

Testing edge cases helps make your robot more reliable in unexpected situations. Think about what might happen in rare or unusual circumstances, and make sure your program can handle these situations gracefully.

### **User Scenarios**

Test your program based on real-world situations:
- How would different users interact with the robot?
- What if the user gives unexpected commands?
- What if the environment changes while the robot is operating?

User scenario testing means thinking about how real people will use your robot in the real world. For example, if you're programming a robot to help elderly people, you might need to make the interface extra simple and provide clear feedback. If children might interact with the robot, you should make sure it responds safely to unpredictable commands.

Consider different environments too. A robot that works perfectly in your classroom might struggle in a busy hospital hallway or a home with pets running around. Testing with realistic scenarios helps ensure your robot will be helpful in actual use.

### **Systematic Testing**

Create a testing plan that covers all possible scenarios:
- Start with simple, known inputs
- Progress to more complex cases
- Document results to track improvements

Systematic testing means having an organized plan to test your program thoroughly. Start with basic tests that you know should work, like having your robot move forward 10 centimeters. Once those pass, try more complicated tests like navigating through a simple maze.

Keep a record of what you've tested and the results. This helps you track your progress and avoid repeating tests unnecessarily. It also helps you remember what worked and what didn't if you need to make changes later.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about a time when you encountered a problem with a device or application. How did you go about troubleshooting it? Did you follow steps similar to the debugging process we discussed?
---stopandreflectEND---

## **Improving Your Programs**

Once your program works correctly, you can focus on making it better.

### **Code Readability**

Clear, well-organized code is easier to debug:
- Use meaningful variable and function names
- Add comments explaining complex sections
- Format your code consistently

Writing readable code is like writing a clear essay instead of a messy note. When you use descriptive names like "robotSpeed" instead of just "s", anyone reading your code (including your future self!) will understand what it means. Comments are like footnotes that explain your thinking and help others understand tricky parts of your code.

For example, instead of:
```
x = 5
y = x * 2
```

You could write:
```
// Set the robot's maximum speed
maxSpeed = 5
// Calculate safe turning speed (half of maximum)
turningSpeed = maxSpeed * 2
```

This makes it much easier to understand what your code is doing and why.

---pagebreak---

### **Defensive Programming**

Anticipate potential problems in your code:
- Validate user inputs before processing them
- Include error handling for unexpected situations
- Add safeguards for critical operations

Defensive programming is like wearing a helmet when riding a bike - it's about protecting your program from things that might go wrong. For example, if your program asks for a number between 1 and 10, check that the input is actually a number and is within that range before using it.

Error handling means your program can respond gracefully when something unexpected happens. Instead of crashing when a sensor fails, your robot could display a message saying "Sensor error detected" and safely stop moving until the problem is fixed.

#### **Graceful Degradation**

An important part of defensive programming is graceful degradation - making sure your robot can still function in a limited way even when something goes wrong.

For example, if your kitchen helper robot has three sensors to detect obstacles but one stops working:
- A poorly programmed robot might crash or freeze completely
- A robot with graceful degradation would display a warning message, move more slowly, and continue working with the remaining sensors

This is like how your phone can still make calls even when the internet isn't working. Your robot should have backup plans for when things don't go perfectly!

### **Incremental Development**

Build and test your program in small pieces:
- Start with a minimal working version
- Add one feature at a time
- Test thoroughly after each addition

Incremental development means building your program step by step instead of all at once. It's like building with blocks - you make sure each piece is solid before adding the next one. For example, when programming a helper robot, you might:

1. First make sure it can move forward and stop safely
2. Then add turning capabilities
3. Then add object detection
4. Finally add the specific helper functions

This approach makes it much easier to find and fix problems because you know exactly what changed when something stops working.

## **Activity 2: Test Different Inputs**

Take the corrected robot navigation program from the earlier activity and test it with these different scenarios:

1. Starting and ending positions are the same
2. The robot needs to navigate around a simple obstacle
3. The destination is unreachable

For each scenario, predict what will happen, run the test, and record the results. What changes would you make to improve the program's handling of these situations?

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider how systematic debugging differs from random trial-and-error approaches. How does having a structured debugging process help you solve programming problems more efficiently? Think about how this might apply to other types of problem-solving beyond programming.
---stopandreflectEND---

---checkyourunderstanding---
What is the first step in debugging a program that isn't working?

A. Start over with a new program

B. Ask someone else to fix it

C. Identify exactly what's happening versus what should happen

D. Add more code to fix the problem
---answer---
The correct answer is C. Identify exactly what's happening versus what should happen. Effective debugging starts with clearly understanding the problem by identifying the difference between the current behavior and the expected behavior. If you chose a different answer, remember that fixing a problem requires first understanding it thoroughly - adding code blindly or starting over are inefficient approaches when a systematic process can help identify the specific issue.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- Debugging is a normal part of programming that becomes easier with practice and a systematic approach
- Systematic testing with various inputs helps uncover and address potential problems before they affect users
- Small, incremental tests and changes make debugging easier and help create more reliable programs