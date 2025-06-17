# Admin
Module 8
Lesson 3
Lesson Title: Programming Robot Movement
# Template

# 8.3
# Programming Robot Movement
## Learning Objectives
By the end of this session, you'll be able to:
- Create programs that control robot movement
- Connect sequence concepts to physical robot actions
- Debug simple movement programs
## Lesson Podcast Discussion: Creating Programs for Robot Movement
This podcast explores how programming sequences translate into physical robot movements and why this connection is fundamental to robotics.

## Basic Movement Commands
The foundation of robot movement programming begins with understanding basic movement commands. Most robot platforms recognize simple directional instructions that serve as building blocks for more complex behaviors.

### Standard Movement Commands
Common movement commands include:
- **Forward/Backward**: Moves the robot in a straight line in the specified direction
- **Left/Right Turn**: Rotates the robot in place, typically by a specific degree (often 90°)
- **Stop**: Halts all movement
- **Speed Control**: Adjusts how quickly the robot executes movements

These commands are typically represented as functions or blocks in programming environments designed for robotics education. For example:

moveForward(distance)
turnLeft(degrees)
turnRight(degrees)
moveBackward(distance)
setSpeed(speedValue)


## Creating Movement Patterns
Once you understand basic commands, you can combine them to create deliberate movement patterns. These patterns allow robots to navigate environments or perform specific tasks.

### Sequential Programming
The key to effective movement programming is understanding that robots execute commands in sequence—one after another. This sequential execution creates paths and patterns:


moveForward(10)
turnRight(90)
moveForward(5)


This simple program would make the robot move forward, turn right at a 90-degree angle, and then move forward again, creating an L-shaped path.

## Activity 1: Program a Virtual Robot Path
Using the virtual robot simulator provided, create a program that navigates the robot from the starting point to the target location. The robot should follow the path marked on the grid while avoiding obstacles. Start by listing the sequence of commands you think will work, then implement them in the simulator. If your robot doesn't reach the target, try to identify where the movement sequence went wrong.

## Combining Multiple Movements
Complex robot behaviors come from combining multiple movement sequences. By understanding how to chain commands together, you can create sophisticated robot actions.

### Creating Reusable Movement Blocks
Grouping common movement patterns into reusable blocks makes programming more efficient:


function makeSquare(sideLength) {
  for (let i = 0; i < 4; i++) {
    moveForward(sideLength)
    turnLeft(90)
  }
}


This function allows your robot to create a square of any size with a single command. Similar patterns can be created for circles, triangles, or other complex movements.

### Timing and Coordination
When combining movements, timing is crucial:
- **Sequential timing**: Waiting for one movement to complete before starting another
- **Parallel timing**: Having multiple parts of the robot move simultaneously
- **Delayed execution**: Programming pauses between movements

## Stop and reflect

**CHECKPOINT:** Think about the last movement sequence you programmed. What challenges did you encounter when trying to get the robot to move exactly as you intended? Consider how breaking down complex movements into smaller steps might improve your results.

## Testing and Fixing Movement Programs
Even carefully planned movement programs often require debugging. Learning to test and fix movement issues is an essential skill for robotics programming.

### Common Movement Issues
- **Distance errors**: Robot moves too far or not far enough
- **Turning errors**: Robot doesn't turn at the expected angle
- **Environmental factors**: Wheel slippage or surface changes affecting movement
- **Battery levels**: Lower power can reduce movement accuracy

### Debugging Strategies
1. **Incremental testing**: Test one movement at a time
2. **Observation**: Watch the robot's actual versus expected movement
3. **Parameter adjustment**: Fine-tune distance and angle values
4. **Sensor feedback**: Use sensors to verify position (when available)


// Before debugging
moveForward(10)
turnRight(90)
moveForward(5)

// After debugging with adjusted parameters
moveForward(9.5)  // Adjusted for slight overrun
turnRight(93)     // Compensated for turning inaccuracy
moveForward(5.2)  // Adjusted for slight underrun


### Check your understanding
If a robot needs to make a square path, what sequence of commands would work?
A. Forward, Left, Forward, Right, Forward, Right
B. Forward, Left, Forward, Left, Forward, Left, Forward, Left
C. Forward, Forward, Forward, Forward
D. Left, Left, Left, Left

Choose your answer and check it below.

The correct answer is B. Forward, Left, Forward, Left, Forward, Left, Forward, Left. To create a square path, the robot needs to move forward, turn left (90 degrees), and repeat this sequence four times to complete all sides of the square. If you chose A, you created an irregular shape with only three sides. If you chose C, your robot would move in a straight line. If you chose D, your robot would spin in place without creating any path.

## Key Takeaways
- Movement programming connects abstract sequences to physical actions, allowing you to see immediate results of your code
- Testing is essential to verify movement programs work correctly, as physical factors can affect how commands execute
- Complex movements can be built from simple command sequences, allowing you to create sophisticated robot behaviors

## Instructional designer notes of lesson 8.3
**This lesson fits into the overall module of Robots Helping People in the following ways:**
- It helps students understand how to program robots to perform physical tasks that can assist people
- It builds on previous lessons about robot capabilities by teaching how to control those capabilities
- It prepares students for future lessons where robots will be programmed to solve specific human needs
- It connects abstract programming concepts to tangible, observable robot behaviors

**This lesson could be followed by this game:**
Sequencer game: Students are presented with a series of robot challenges (navigate a hospital hallway, deliver medicine to a patient, help someone stand up) and must arrange the correct sequence of movement commands to complete each task. Each challenge increases in complexity, requiring more sophisticated sequences and better understanding of how movement commands work together.