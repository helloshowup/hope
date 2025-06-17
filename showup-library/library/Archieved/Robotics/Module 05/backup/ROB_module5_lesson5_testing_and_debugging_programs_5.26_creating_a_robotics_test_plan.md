# 5.26
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