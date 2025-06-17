# 5.13
## **Testing and Fixing Movement Programs**

Even well-planned robot movement programs often don't work perfectly the first time. Learning to identify and fix issues in your movement programs is an essential robotics programming skill.

### **Common Movement Errors**

Some typical errors in movement programs include:

1. **Incorrect distances or angles**: The robot doesn't move the intended distance or turn the correct angle
2. **Sequence errors**: Commands are executed in the wrong order
3. **Missing commands**: A required movement is omitted from the sequence
4. **Timing issues**: The robot executes commands too quickly or with improper delays

### **Debugging Process**

When your robot doesn't move as expected, follow this debugging process:

1. **Observe**: Watch the robot's actual behavior compared to what you expected
2. **Identify**: Determine where the deviation from expected behavior occurs
3. **Hypothesize**: Formulate a theory about what's causing the problem
4. **Test**: Make a single change to your program and observe the result
5. **Repeat**: Continue the process until the robot behaves as expected

For example, if your robot should make a square but instead makes an odd shape, you might:
- Check your turn angles (are they exactly 90 degrees?)
- Verify movement distances (are all sides the same length?)
- Confirm the sequence has the correct number of movements (four sides require four forward commands and four turns)

### **Debugging Example: School Robot Gone Wrong**

Imagine programming a robot to deliver items between classrooms. Your program should make the robot:
1. Leave the office
2. Turn right down the hallway
3. Go to the third classroom
4. Turn left into the classroom
5. Deliver the item
6. Return to the office

But instead, your robot keeps going past the third classroom! Here's how you might debug:

1. **Observe**: The robot passes the third classroom without stopping
2. **Identify**: The robot isn't counting classrooms correctly
3. **Hypothesize**: Maybe the distance between classrooms varies
4. **Test**: Change the program to use door sensors instead of fixed distances
5. **Repeat**: Test the new program and adjust as needed

This real-world example shows how the same debugging process applies to more complex robot tasks.

---checkyourunderstanding---
If a robot needs to travel from point A to point B, then return to point A following a different path, what sequence elements are essential in your program?

A. The robot must first determine its current location before starting movement

B. The program must include at least one wait command between movements

C. The sequence must use the same movement distances going and returning

D. The program must include different command sequences for the outbound and return journeys
---answer---
The correct answer is D. The program must include different command sequences for the outbound and return journeys. Since the robot needs to follow a different path on the return journey, the program must contain distinct command sequences for each part of the journey. If you chose a different answer, remember that robots follow commands literally - to take different paths, you must provide different instructions for each path.
---answerEND---
---checkyourunderstandingEND---

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider a time when your robot movement program didn't work as expected. What specific debugging steps did you take to identify and fix the problem? What did this experience teach you about the importance of testing in robotics programming?
---stopandreflectEND---