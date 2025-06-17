# 8.3
# **Programming Robot Movement**

## **Learning Objectives**

By the end of this session, you'll be able to:
- Create programs that control robot movement
- Connect sequence concepts to physical robot actions
- Debug simple movement programs

## **Lesson Podcast Discussion: Creating Programs for Robot Movement**

This podcast explores how programming sequences translate into physical robot movements and why this connection is fundamental to robotics.

When we program a robot, we're creating a set of instructions that tell the robot exactly what to do. These instructions are like a recipe that the robot follows step by step. What makes robotics so exciting is that you can immediately see the results of your code in the physical world! 

Unlike programs that just display information on a screen, robot programs make things move, interact with objects, and navigate through spaces. This connection between the digital world of programming and the physical world of movement is what makes robotics such a powerful learning tool.

Think about it: when you write a line of code telling a robot to move forward, you're converting your thoughts into actions that happen in the real world. This direct connection helps us understand both programming concepts and how machines operate in our environment.

## **Basic Movement Commands**

The foundation of robot movement programming begins with understanding basic movement commands. Most robot platforms recognize simple directional instructions that serve as building blocks for more complex behaviors.

### **Standard Movement Commands**

Common movement commands include:
- **Forward/Backward**: Moves the robot in a straight line in the specified direction
- **Left/Right Turn**: Rotates the robot in place, typically by a specific degree (often 90°)
- **Stop**: Halts all movement
- **Speed Control**: Adjusts how quickly the robot executes movements

These commands are typically represented as functions or blocks in programming environments designed for robotics education. For example:

```
moveForward(distance)
turnLeft(degrees)
turnRight(degrees)
moveBackward(distance)
setSpeed(speedValue)
```

Think of these commands as the robot's basic vocabulary. Just like we use simple words to build complex sentences, these basic movement commands are combined to create sophisticated robot behaviors. Each command tells the motors in the robot exactly what to do - whether to spin forward or backward, how fast to move, or when to stop completely.

The distance parameter in movement commands usually represents centimeters or inches, while degrees in turning commands tell the robot exactly how far to rotate. For example, `turnRight(90)` would make the robot turn 90 degrees to the right - a perfect right angle turn!

---pagebreak---

## **Creating Movement Patterns**

Once you understand basic commands, you can combine them to create deliberate movement patterns. These patterns allow robots to navigate environments or perform specific tasks.

### **Sequential Programming**

The key to effective movement programming is understanding that robots execute commands in sequence—one after another. This sequential execution creates paths and patterns:

```
moveForward(10)
turnRight(90)
moveForward(5)
```

This simple program would make the robot move forward, turn right at a 90-degree angle, and then move forward again, creating an L-shaped path.

When programming robot movements, it's helpful to think like the robot. Imagine you are the robot following instructions one at a time. If you want your robot to trace a square, you need to break down that pattern into individual steps: move forward, turn, move forward, turn, and so on.

The order of commands matters tremendously in robotics. If you switch the order of two commands, your robot will follow a completely different path! This is why planning your movement sequence before programming can save you time and help avoid mistakes. Many robotics programmers sketch out their intended paths on paper first, then translate those paths into sequences of movement commands.

## **Activity 1: Program a Virtual Robot Path**

Using the virtual robot simulator provided, create a program that navigates the robot from the starting point to the target location. The robot should follow the path marked on the grid while avoiding obstacles. Start by listing the sequence of commands you think will work, then implement them in the simulator. If your robot doesn't reach the target, try to identify where the movement sequence went wrong.

## **Combining Multiple Movements**

Complex robot behaviors come from combining multiple movement sequences. By understanding how to chain commands together, you can create sophisticated robot actions.

### **Creating Reusable Movement Blocks**

Grouping common movement patterns into reusable blocks makes programming more efficient:

```
function makeSquare(sideLength) {
  for (let i = 0; i < 4; i++) {
    moveForward(sideLength)
    turnLeft(90)
  }
}
```

This function allows your robot to create a square of any size with a single command. Similar patterns can be created for circles, triangles, or other complex movements.

Creating reusable movement blocks is like building with LEGO bricks. Instead of starting from scratch each time, you can use pre-built patterns to quickly create complex behaviors. For example, once you've created a `makeSquare` function, you can use it multiple times in different parts of your program without rewriting all the individual movement commands.

These reusable blocks also make your code easier to read and understand. Instead of seeing a long list of individual movement commands, someone reading your code can quickly understand that the robot is making a square or following another recognizable pattern.

---pagebreak---

### **Timing and Coordination**

When combining movements, timing is crucial:
- **Sequential timing**: Waiting for one movement to complete before starting another
- **Parallel timing**: Having multiple parts of the robot move simultaneously
- **Delayed execution**: Programming pauses between movements

Timing affects how smoothly your robot performs tasks. For example, if your robot has an arm attachment, you might want the robot to drive forward and then raise its arm to pick up an object. The timing between these actions needs to be just right - if the arm starts moving too early or too late, the robot might miss the object completely!

Many robot programming platforms include wait or delay commands that pause execution for a specific amount of time. These pauses can be essential for coordinating complex movements or giving mechanical parts time to complete their actions before the next command begins.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about the last movement sequence you programmed. What challenges did you encounter when trying to get the robot to move exactly as you intended? Consider how breaking down complex movements into smaller steps might improve your results.
---stopandreflectEND---

## **Testing and Fixing Movement Programs**

Even carefully planned movement programs often require debugging. Learning to test and fix movement issues is an essential skill for robotics programming.

### **Common Movement Issues**
- **Distance errors**: Robot moves too far or not far enough
- **Turning errors**: Robot doesn't turn at the expected angle
- **Environmental factors**: Wheel slippage or surface changes affecting movement
- **Battery levels**: Lower power can reduce movement accuracy

When programming robots, what works perfectly in theory doesn't always work perfectly in practice. The physical world introduces variables that can affect how your robot moves. For example, a robot might turn slightly less than 90 degrees on carpet but slightly more than 90 degrees on a smooth floor due to differences in friction.

These real-world factors make testing and observation crucial parts of robotics programming. Don't be discouraged if your robot doesn't move exactly as planned on the first try - even professional roboticists spend a lot of time adjusting and fine-tuning their movement programs!

### **Debugging Strategies**
1. **Incremental testing**: Test one movement at a time
2. **Observation**: Watch the robot's actual versus expected movement
3. **Parameter adjustment**: Fine-tune distance and angle values
4. **Sensor feedback**: Use sensors to verify position (when available)

```
// Before debugging
moveForward(10)
turnRight(90)
moveForward(5)

// After debugging with adjusted parameters
moveForward(9.5)  // Adjusted for slight overrun
turnRight(93)     // Compensated for turning inaccuracy
moveForward(5.2)  // Adjusted for slight underrun
```

Debugging robot movement is like being a detective. You need to carefully observe what's happening, identify patterns in the errors, and make small adjustments until the robot behaves as expected. One effective strategy is to break down complex movements into smaller parts and test each part individually.

Keep a notebook handy to record your observations and adjustments. This helps you track what changes you've made and how they affected the robot's movement. Over time, you'll develop an intuition for how your specific robot responds to different commands and environments, making future programming much easier.

### **Real-World Applications: Assistive Robots**

Movement programming is especially important for robots that help people. Imagine programming a robot that needs to help someone with limited mobility navigate around their home. The robot would need to:

- Move smoothly without jerky motions that could startle the person
- Navigate carefully around furniture and through doorways
- Adjust its speed based on whether it's following alongside someone or delivering an item
- Respond to different floor surfaces like carpet, tile, or thresholds between rooms

For example, a robot that helps carry items for someone might need this program:

```
// Approach person carefully
setSpeed(SLOW)
moveForward(untilProximity)
stop()

// Wait for item to be placed
wait(untilWeightSensorActivated)

// Follow person to destination
setSpeed(MEDIUM)
followPersonWithSensors()

// Stop and wait for item retrieval
stop()
wait(untilWeightSensorDeactivated)
```

This shows how movement programming for assistive robots needs to coordinate with sensors and be especially careful about timing and safety.

---checkyourunderstanding---
If a robot needs to make a square path, what sequence of commands would work?

A. Forward, Left, Forward, Right, Forward, Right

B. Forward, Left, Forward, Left, Forward, Left, Forward, Left

C. Forward, Forward, Forward, Forward

D. Left, Left, Left, Left
---answer---
The correct answer is B. Forward, Left, Forward, Left, Forward, Left, Forward, Left. To create a square path, the robot needs to move forward, turn left (90 degrees), and repeat this sequence four times to complete all sides of the square. If you chose A, you created an irregular shape with only three sides. If you chose C, your robot would move in a straight line. If you chose D, your robot would spin in place without creating any path.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- Movement programming connects abstract sequences to physical actions, allowing you to see immediate results of your code
- Testing is essential to verify movement programs work correctly, as physical factors can affect how commands execute
- Complex movements can be built from simple command sequences, allowing you to create sophisticated robot behaviors

## **Instructional designer notes of lesson 8.3**

**This lesson fits into the overall module of Robots Helping People in the following ways:**
- It helps students understand how to program robots to perform physical tasks that can assist people
- It builds on previous lessons about robot capabilities by teaching how to control those capabilities
- It prepares students for future lessons where robots will be programmed to solve specific human needs
- It connects abstract programming concepts to tangible, observable robot behaviors

**This lesson could be followed by this game:**
Sequencer game: Students are presented with a series of robot challenges (navigate a hospital hallway, deliver medicine to a patient, help someone stand up) and must arrange the correct sequence of movement commands to complete each task. Each challenge increases in complexity, requiring more sophisticated sequences and better understanding of how movement commands work together.

Additional Writer Notes:
I addressed the following SME feedback points:
1. Reframed part of the lesson to focus on programming movement for assistive robots
2. Added a real-world example section showing how movement programming applies to robots that help people
3. Included a more complex, multi-stage movement sequence example for an assistive robot
4. Maintained age-appropriate language and examples suitable for 11-14 year olds
5. Incorporated the "Movement Methods and Applications" example from the Cross-Module Example Index by showing how robots need to adjust to different environments