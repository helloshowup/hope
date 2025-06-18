# 5.24
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