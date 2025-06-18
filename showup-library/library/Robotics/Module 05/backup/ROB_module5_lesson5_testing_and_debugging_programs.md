# 5.5
# **Testing and Debugging Programs**

## **Lesson Podcast Discussion: The Art of Systematic Debugging**

A discussion about how professional programmers approach debugging methodically rather than randomly, with real-world examples of challenging bugs that were solved through systematic approaches.

---pagebreak---

## **Common Programming Errors**

When programming robots or any system, errors are inevitable. Understanding the common types of errors helps you identify and fix them more efficiently. There are three main categories of programming errors:

### **Syntax Errors**

These are spelling and grammar mistakes in your code. Just like a sentence needs proper punctuation and structure in English, programming languages have specific rules for how commands must be written. Examples include:
- Missing brackets or parentheses
- Misspelled commands
- Missing semicolons or other required punctuation

The good news is that most programming environments will detect these errors immediately and highlight them for you.

### **Logic Errors**

Logic errors occur when your code runs without crashing but produces incorrect results. The syntax is correct, but your instructions don't accomplish what you intended. These are often the most challenging errors to find because the program appears to work. Examples include:
- Using the wrong formula in a calculation
- Creating an infinite loop
- Testing conditions in the wrong order

In robotics, a common logic error might be telling your robot to turn right when it should turn left, or setting a sensor threshold too high or too low, causing your robot to miss important information.

### **Runtime Errors**

Runtime errors happen when your program encounters a problem while running. These errors cause your program to crash or stop executing. Examples include:
- Dividing by zero
- Referring to variables that don't exist
- Trying to perform operations on incompatible data types

For robots, runtime errors might occur when your program tries to access a sensor that isn't connected or when your robot attempts a movement that's physically impossible.

---pagebreak---

## **The Debugging Process**

Debugging is a systematic process, not random guesswork. Following these steps will help you find and fix errors efficiently:

### **Step 1: Reproduce the Problem**

The first step in fixing any bug is being able to make it happen consistently. Try to identify the specific conditions that cause the error to occur.

For example, if your robot only turns incorrectly when approaching a wall at a certain angle, you'll need to recreate that specific scenario to properly debug the issue.

### **Step 2: Identify the Expected vs. Actual Behavior**

Clearly define what you expected to happen and what actually happened instead. This gap is the essence of your bug.

For instance: "I expected the robot to stop when it detected an object 10cm away, but it continues moving until it bumps into the object."

### **Step 3: Locate the Source of the Error**

Narrow down where in your code the problem might be occurring. For larger programs, you can use techniques like:
- Print statements to show values at different points in your code
- Commenting out sections to see if the error disappears
- Working backwards from where the incorrect behavior appears

In robotics programming, it's helpful to check:
- Sensor readings (are they giving accurate values?)
- Motor commands (are they receiving the correct instructions?)
- Decision logic (are your if/then statements evaluating correctly?)

### **Step 4: Fix the Error and Test**

Make a single, focused change that you believe will fix the issue. Then test your program again to see if the error is resolved. If you make multiple changes at once, you won't know which one actually fixed the problem.

---pagebreak---

## **Activity 1: Bug Detective**

**Activity 1: Find the Bugs**

Review the following simple robot movement program that contains three different types of errors. Identify what type each error is (syntax, logic, or runtime) and how you would fix it:


function moveRobot() {
  forward(10);
  turn(90)
  forward(5;
  if (sensorValue > 50) {
    backwards(10);
  }
  turn(45);
  while (true) {
    forward(1);
  }
}


Try to find all three errors before checking the solution in your course materials!

---pagebreak---

## **Testing with Different Scenarios**

Thorough testing is crucial for creating reliable programs. It's important to test your code with various inputs and situations.

### **Input Testing**

Always test your program with:
- Normal expected values
- Boundary values (minimum and maximum allowed)
- Invalid inputs (what happens if a user enters text when a number is expected?)

For a robot that follows a line, you might test:
- Normal conditions: robot on a clear, dark line against a light background
- Boundary conditions: robot on a faded line or a line with varying thickness
- Invalid conditions: robot on a surface with multiple lines or no line at all

### **Edge Cases**

Edge cases are unusual but possible scenarios that might cause problems:
- What if a sensor returns zero?
- What if your robot reaches a physical barrier?
- What if the battery is low?

For example, if you're programming a robot to navigate a maze, edge cases might include:
- Dead ends that require the robot to turn around completely
- Very narrow passages that might cause sensor confusion
- Highly reflective surfaces that interfere with distance sensors

### **Incremental Testing**

Instead of writing a large program and then testing it all at once:
1. Write a small piece of functionality
2. Test it thoroughly
3. Only when it works correctly, add the next feature
4. Repeat

This approach makes it much easier to identify where errors occur.

For example, when programming a robot to pick up objects:
1. First, test just the movement toward the object
2. Then, test the gripper mechanism separately
3. Next, test the combination of movement and gripping
4. Finally, test the complete sequence including returning the object to a designated location

---stopandreflect---
## Stop and reflect
**CHECKPOINT:** Think about a time when you encountered a problem that required systematic troubleshooting (with technology, a game, or anything else). How did breaking down the problem help you solve it more effectively than random attempts?
---stopandreflectEND---

---pagebreak---

## **Improving Your Programs**

Debugging isn't just about fixing errors—it's also an opportunity to improve your code.

### **Refactoring for Clarity**

After fixing bugs, look for ways to make your code clearer and more maintainable:
- Use meaningful variable and function names
- Break long functions into smaller, focused ones
- Add comments explaining complex sections

For example, instead of using a variable name like "s1" for a sensor, use "distanceSensor" to make your code easier to understand.

### **Performance Optimization**

Once your program works correctly, you might want to make it run more efficiently:
- Remove unnecessary steps
- Look for repeated code that could be turned into a function
- Consider whether there are more efficient algorithms

In robotics, efficient code can save battery power and make your robot respond more quickly to its environment.

### **Documentation**

Good documentation helps you and others understand your code later:
- Explain what your program does
- Document any assumptions or limitations
- Note any special cases or considerations

For example, document that your line-following robot works best on high-contrast surfaces or that your obstacle-avoidance program expects objects to be at least 5cm tall to be detected reliably.

---pagebreak---

## **Creating a Robotics Test Plan**

When testing robot programs, it helps to create a simple test plan. Here's an example for a line-following robot:

1. **Basic Functionality Test**
   - Does the robot follow a straight line?
   - Does it follow a curved line?
   
2. **Sensor Test**
   - Do all sensors detect the line correctly?
   - What happens when sensors are partially on/off the line?
   
3. **Environmental Test**
   - Does the program work in different lighting conditions?
   - Does it work on different surfaces?
   
4. **Edge Case Test**
   - What happens at intersections?
   - What happens if the line ends?
   - What happens if the robot loses the line?

Having a structured test plan helps ensure your robot will work reliably in real-world conditions, not just in ideal situations.

---stopandreflect---
## Stop and reflect
**CHECKPOINT:** Consider your debugging process. Do you tend to make random changes hoping the problem will go away, or do you approach debugging systematically? How might adopting a more methodical approach improve your programming experience?
---stopandreflectEND---

---checkyourunderstanding---
What is the first step in debugging a program that isn't working?

A. Start over with a new program

B. Ask someone else to fix it

C. Identify exactly what's happening versus what should happen

D. Add more code to fix the problem
---answer---
The correct answer is C. Identify exactly what's happening versus what should happen. Effective debugging starts with clearly understanding the problem by identifying the difference between the current behavior and the expected behavior. If you chose a different answer, remember that debugging is about methodical problem-solving rather than blind fixes or starting over. Understanding the problem is always the first step to solving it.
---answerEND---
---checkyourunderstandingEND---

**This lesson could be followed by this game:**
Debug challenge game: Players are presented with a series of increasingly complex robot programs containing different types of errors. They must identify the specific error type (syntax, logic, or runtime) and select the correct fix from multiple options. For example, a simple robot navigation program might have a missing semicolon (syntax error), an incorrect turning angle (logic error), or a division by zero when calculating speed (runtime error). Players earn points based on speed and accuracy of their debugging.