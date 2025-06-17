# Admin
Module 6
Lesson 3
Lesson Title: Programming Robot Movement
# Template
[start of lesson]
# 6.3
# Programming Robot Movement
## Learning Objectives
By the end of this session, you'll be able to:
- Create programs that control robot movement
- Connect sequence concepts to physical robot actions
- Debug simple movement programs
### Lesson Podcast Discussion: Programming Movement Sequences for Robots
This podcast explores how programming sequences translate into physical robot actions and the common challenges faced when designing movement programs.
## Introduction to Robot Movement
Programming a robot to move is one of the most fundamental and exciting aspects of robotics. When we create movement programs, we're translating our abstract code into physical actions in the real world. This connection between the digital and physical realms is what makes robot programming particularly engaging and also challenging.

In this lesson, we'll explore how to create programs that control robot movement, how to develop movement patterns, and techniques for testing and fixing your programs when they don't work as expected.
### Why Movement Matters
Movement is often the primary way robots interact with their environment. Whether it's a robot vacuum navigating a room, a robotic arm in a factory, or a rover exploring another planet, programmed movement instructions allow robots to accomplish their tasks. The quality of movement programming directly impacts how effective a robot is at achieving its goals.
## Basic Movement Commands
Most robot programming environments provide a standard set of movement commands that serve as the building blocks for more complex behaviors. These typically include:

- Forward/Backward: Commands that move the robot in a straight line
- Left/Right: Commands that rotate the robot in place
- Wait/Pause: Commands that make the robot stop for a specified duration

Each command usually requires parameters that specify details like distance, speed, or duration. For example:

moveForward(10) // Move forward 10 units
turnLeft(90)    // Turn left 90 degrees
pause(2)        // Wait for 2 seconds

### Parameters and Units
When programming robot movement, it's important to understand the units used by your specific robot:

- Distance may be measured in centimeters, inches, or arbitrary "steps"
- Turns might be specified in degrees or radians
- Speed could be represented as a percentage of maximum speed or specific units like cm/s
- Timing is typically in seconds or milliseconds

Misunderstanding these units is a common source of errors in movement programming.
## Creating Movement Patterns
Movement patterns are sequences of basic commands that create a specific path or behavior. Simple patterns include:

- Square paths (forward, turn, forward, turn, etc.)
- Zigzag patterns (forward, turn slight, forward, turn opposite, etc.)
- Spirals (forward with gradually increasing turning)
- Circles (constant forward motion with constant turning)

The key to creating effective patterns is to break down the desired movement into a sequence of simple steps that the robot can execute one after another.
### Planning Before Programming
Before writing any code, it's helpful to:

1. Draw the desired path on paper
2. Mark each straight section and turn
3. Note the approximate distances and angles
4. Convert your drawing into a sequence of commands

This planning process saves time and reduces errors when you start coding.
## **Activity 1: Program a Virtual Robot to Navigate a Simple Path**
Using the virtual robot environment provided, program your robot to navigate from the starting point to the goal while avoiding the obstacles in between. The environment shows a grid with walls that the robot must navigate around. Start by planning your path on paper, then translate that path into a sequence of movement commands. Test your program step by step, observing how each command affects the robot's position and orientation.
## Combining Multiple Movements
Complex robot behaviors often require combining multiple movement patterns. There are several approaches to this:

1. Sequential execution: Run one pattern after another
2. Conditional execution: Choose patterns based on sensor input or other conditions
3. Looped execution: Repeat patterns a specified number of times
4. Nested patterns: Define patterns that include other patterns

For example, a delivery robot might use a "navigate_hallway" pattern, followed by a "turn_corner" pattern, followed by an "approach_door" pattern—each of which consists of more basic movement commands.
### Using Functions for Reusable Movements
To make your code more organized and reusable, define functions for common movement patterns:


function square(sideLength) {
  for (let i = 0; i < 4; i++) {
    moveForward(sideLength);
    turnLeft(90);
  }
}

// Now you can create squares of any size
square(10);  // Small square
square(50);  // Large square


This approach makes your code easier to read and maintain.
## Stop and reflect

**CHECKPOINT:** Think about a time when you gave someone directions to a location. How is programming robot movement similar to or different from giving verbal directions to a person? What additional considerations do you need to make when the recipient of instructions is a robot rather than a human?

## Testing and Fixing Movement Programs
Even with careful planning, movement programs rarely work perfectly on the first try. Testing and debugging are essential skills for successful robot programming.
### Common Movement Problems
Several issues commonly arise with movement programs:

1. **Alignment errors**: Small turning errors that compound over time
2. **Surface variations**: Different surfaces affect movement differently
3. **Battery levels**: Lower battery can mean slower movements
4. **Hardware differences**: Two seemingly identical robots may move differently

To address these issues, you need a systematic approach to testing and debugging.
### Debugging Strategies
When your robot doesn't move as expected:

1. Test one command at a time to identify where the problem occurs
2. Use visual markers to track expected positions
3. Add pauses between commands to observe each step
4. Adjust parameters incrementally rather than making large changes
5. Consider environmental factors that might be affecting movement

Remember that physical robots have mechanical limitations and variability that virtual simulations don't always capture accurately.
## **Activity 2: Debug a Movement Sequence**
Examine the provided movement program that's supposed to make the robot draw a triangle, but it's not working correctly. The robot moves forward, turns, moves forward again, but ends up in the wrong position for the third side. Use the debugging techniques we've discussed to identify what's wrong with the program. Make the necessary corrections to fix the program so the robot successfully draws a complete triangle and returns to its starting position.
## Stop and reflect

**CHECKPOINT:** What was the most challenging aspect of programming robot movements in today's activities? Was it planning the sequence, understanding the commands, or dealing with unexpected behavior? Consider how breaking down complex movements into smaller, testable parts could help overcome these challenges.

### **Check your understanding**
If a robot needs to make a square path, what sequence of commands would work?
A. Forward, Left, Forward, Right, Forward, Right
B. Forward, Left, Forward, Left, Forward, Left, Forward, Left
C. Forward, Forward, Forward, Forward
D. Left, Left, Left, Left
Choose your answer and check it below.
The correct answer is B. Forward, Left, Forward, Left, Forward, Left, Forward, Left. To create a square path, the robot needs to move forward, turn left (90 degrees), and repeat this sequence four times to complete all sides of the square. If you chose A, you created an irregular path with unnecessary right turns. If you chose C, you only moved in a straight line without forming a square. If you chose D, you made the robot spin in place without any forward movement.
## Key Takeaways
- Movement programming connects abstract sequences to physical actions, allowing us to see the direct results of our code in the real world
- Testing is essential to verify movement programs work correctly, as physical robots often behave differently than expected due to environmental factors
- Complex movements can be built from simple command sequences, making it possible to create sophisticated robot behaviors from basic building blocks
[End of Lesson]
## Instructional designer notes of lesson 6.3
**This lesson fits into the overall module of Smarter Robot Instructions (Advanced Programming) in the following ways:**
- It applies the sequence programming concepts introduced earlier in the module to physical robot actions
- It builds upon the basic movement concepts from Module 3, but now focusing on programmatic control rather than manual operation
- It prepares students for more complex programming challenges in subsequent lessons by establishing fundamental movement control skills
- It reinforces debugging concepts that will be essential throughout the module

**This lesson could be followed by this game:**
Robot maze challenge where students program a virtual robot to navigate increasingly complex paths. The game would start with simple mazes requiring basic movement commands and gradually introduce obstacles that require more sophisticated sequences. Students would need to apply their knowledge of movement commands, sequences, and debugging to successfully navigate their robot through each level.