# 5.22
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