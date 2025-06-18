# 6.3
# **Programming Robot Movement**

## **Learning Objectives**

By the end of this session, you'll be able to:
- Create programs that control robot movement
- Connect sequence concepts to physical robot actions
- Debug simple movement programs

### **Lesson Podcast Discussion: Programming Movement Sequences for Robots**

This podcast explores how programming sequences translate into physical robot actions and the common challenges faced when designing movement programs.

## **Introduction to Robot Movement**

Programming a robot to move is one of the most fundamental and exciting aspects of robotics. When we create movement programs, we're translating our abstract code into physical actions in the real world. This connection between the digital and physical realms is what makes robot programming particularly engaging and also challenging.

In this lesson, we'll explore how to create programs that control robot movement, how to develop movement patterns, and techniques for testing and fixing your programs when they don't work as expected. Building on the basic movement concepts you learned in earlier modules, we'll now focus on creating more efficient and optimized movement programs.

### **Why Movement Matters**

Movement is often the primary way robots interact with their environment. Whether it's a robot vacuum navigating a room, a robotic arm in a factory, or a rover exploring another planet, programmed movement instructions allow robots to accomplish their tasks. The quality of movement programming directly impacts how effective a robot is at achieving its goals.

In real-world applications, robots often need to navigate different surfaces and environments. For example, robots that deliver medications in hospitals must navigate hallways, doorways, and around people, requiring sophisticated movement programming that adapts to changing conditions.

## **Basic Movement Commands**

Most robot programming environments provide a standard set of movement commands that serve as the building blocks for more complex behaviors. These typically include:

- **Forward/Backward**: Commands that move the robot in a straight line
- **Left/Right**: Commands that rotate the robot in place
- **Wait/Pause**: Commands that make the robot stop for a specified duration

Each command usually requires parameters that specify details like distance, speed, or duration. For example:

moveForward(10) // Move forward 10 units
turnLeft(90)    // Turn left 90 degrees
pause(2)        // Wait for 2 seconds

### **Parameters and Units**

When programming robot movement, it's important to understand the units used by your specific robot:

- Distance may be measured in centimeters, inches, or arbitrary "steps"
- Turns might be specified in degrees or radians
- Speed could be represented as a percentage of maximum speed or specific units like cm/s
- Timing is typically in seconds or milliseconds

Misunderstanding these units is a common source of errors in movement programming.

---pagebreak---

## **Creating Movement Patterns**

Movement patterns are sequences of basic commands that create a specific path or behavior. Simple patterns include:

- Square paths (forward, turn, forward, turn, etc.)
- Zigzag patterns (forward, turn slight, forward, turn opposite, etc.)
- Spirals (forward with gradually increasing turning)
- Circles (constant forward motion with constant turning)

The key to creating effective patterns is to break down the desired movement into a sequence of simple steps that the robot can execute one after another.

For example, a robot that needs to navigate around a classroom might use different movement patterns depending on the situation:
- Following walls using a "wall-following" pattern
- Navigating between desks using a "zigzag" pattern
- Returning to a charging station using a "homing" pattern

### **Planning Before Programming**

Before writing any code, it's helpful to:

1. Draw the desired path on paper
2. Mark each straight section and turn
3. Note the approximate distances and angles
4. Convert your drawing into a sequence of commands

This planning process saves time and reduces errors when you start coding.

Professional robotics engineers often create detailed movement plans before programming, especially for robots that operate in complex environments like warehouses or hospitals. They might use computer simulations to test movement patterns before implementing them on real robots.

## **Activity 1: Program a Virtual Robot to Navigate a Simple Path**

Using the virtual robot environment provided, program your robot to navigate from the starting point to the goal while avoiding the obstacles in between. The environment shows a grid with walls that the robot must navigate around. Start by planning your path on paper, then translate that path into a sequence of movement commands. Test your program step by step, observing how each command affects the robot's position and orientation.

## **Combining Multiple Movements**

Complex robot behaviors often require combining multiple movement patterns. There are several approaches to this:

1. **Sequential execution**: Run one pattern after another
2. **Conditional execution**: Choose patterns based on sensor input or other conditions
3. **Looped execution**: Repeat patterns a specified number of times
4. **Nested patterns**: Define patterns that include other patterns

For example, a delivery robot might use a "navigate_hallway" pattern, followed by a "turn_corner" pattern, followed by an "approach_door" pattern—each of which consists of more basic movement commands.

In school security systems, robots might patrol hallways using different movement patterns depending on the time of day or whether an alarm has been triggered. During normal hours, they might follow a standard patrol route, but switch to a more thorough search pattern if sensors detect unusual activity.

---pagebreak---

### **Using Functions for Reusable Movements**

To make your code more organized and reusable, define functions for common movement patterns:

```
function square(sideLength) {
  for (let i = 0; i < 4; i++) {
    moveForward(sideLength);
    turnLeft(90);
  }
}

// Now you can create squares of any size
square(10);  // Small square
square(50);  // Large square
```

This approach makes your code easier to read and maintain.

### **Optimizing Movement Programs**

As you become more experienced with programming robot movements, you'll want to optimize your programs for:

1. **Efficiency**: Using the fewest commands to accomplish a task
2. **Battery usage**: Creating movement patterns that conserve energy
3. **Time**: Completing tasks as quickly as possible while maintaining accuracy
4. **Smoothness**: Creating natural-looking movements without jerky stops and starts

For example, instead of having a robot make four separate 90-degree turns to face the opposite direction, you could optimize by using a single 180-degree turn, saving time and battery power.

---stopandreflect---
## Stop and reflect
**CHECKPOINT:** Think about a time when you gave someone directions to a location. How is programming robot movement similar to or different from giving verbal directions to a person? What additional considerations do you need to make when the recipient of instructions is a robot rather than a human?
---stopandreflectEND---

## **Testing and Fixing Movement Programs**

Even with careful planning, movement programs rarely work perfectly on the first try. Testing and debugging are essential skills for successful robot programming.

### **Common Movement Problems**

Several issues commonly arise with movement programs:

1. **Alignment errors**: Small turning errors that compound over time
2. **Surface variations**: Different surfaces affect movement differently
3. **Battery levels**: Lower battery can mean slower movements
4. **Hardware differences**: Two seemingly identical robots may move differently

To address these issues, you need a systematic approach to testing and debugging.

### **Debugging Strategies**

When your robot doesn't move as expected:

1. Test one command at a time to identify where the problem occurs
2. Use visual markers to track expected positions
3. Add pauses between commands to observe each step
4. Adjust parameters incrementally rather than making large changes
5. Consider environmental factors that might be affecting movement

Remember that physical robots have mechanical limitations and variability that virtual simulations don't always capture accurately.

---pagebreak---

### **Systematic Testing Approaches**

Professional robotics developers use systematic testing to ensure their movement programs work reliably:

1. **Unit testing**: Testing individual movement commands in isolation
2. **Integration testing**: Testing how commands work together in sequences
3. **Environmental testing**: Testing movements on different surfaces and conditions
4. **Edge case testing**: Testing extreme situations like very tight turns or long distances

For example, when debugging a robot that keeps turning too far to the right, you might:
1. Test just the turning command with different angle values
2. Check if the wheels are properly calibrated
3. Test the turn on different surfaces to see if friction is affecting the turn
4. Add a small correction factor to compensate for the over-turning

## **Activity 2: Debug a Movement Sequence**

Examine the provided movement program that's supposed to make the robot draw a triangle, but it's not working correctly. The robot moves forward, turns, moves forward again, but ends up in the wrong position for the third side. Use the debugging techniques we've discussed to identify what's wrong with the program. Make the necessary corrections to fix the program so the robot successfully draws a complete triangle and returns to its starting position.

---stopandreflect---
## Stop and reflect
**CHECKPOINT:** What was the most challenging aspect of programming robot movements in today's activities? Was it planning the sequence, understanding the commands, or dealing with unexpected behavior? Consider how breaking down complex movements into smaller, testable parts could help overcome these challenges.
---stopandreflectEND---

---checkyourunderstanding---
If a robot needs to make a square path, what sequence of commands would work?

A. Forward, Left, Forward, Right, Forward, Right

B. Forward, Left, Forward, Left, Forward, Left, Forward, Left

C. Forward, Forward, Forward, Forward

D. Left, Left, Left, Left
---answer---
The correct answer is B. Forward, Left, Forward, Left, Forward, Left, Forward, Left. To create a square path, the robot needs to move forward, turn left (90 degrees), and repeat this sequence four times to complete all sides of the square. If you chose A, you created an irregular path with unnecessary right turns. If you chose C, you only moved in a straight line without forming a square. If you chose D, you made the robot spin in place without any forward movement.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- Movement programming connects abstract sequences to physical actions, allowing us to see the direct results of our code in the real world
- Testing is essential to verify movement programs work correctly, as physical robots often behave differently than expected due to environmental factors
- Complex movements can be built from simple command sequences, making it possible to create sophisticated robot behaviors from basic building blocks