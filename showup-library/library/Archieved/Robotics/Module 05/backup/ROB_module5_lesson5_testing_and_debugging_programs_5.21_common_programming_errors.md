# 5.21
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