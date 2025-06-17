# 5.3
# **Programming Robot Movement**

### **Lesson Podcast Discussion: Connecting Programming to Physical Robot Actions**

This podcast explores how abstract code sequences translate into real-world robot behaviors and why understanding this connection is crucial for effective robotics programming.

## **Understanding Basic Movement Commands**

Before we can create complex robot behaviors, we need to understand the fundamental movement commands that control our robots. Most educational robots support a standard set of basic movement instructions that serve as building blocks for more complex behaviors.

### **Core Movement Commands**

The most common movement commands include:

- **forward(distance)**: Moves the robot forward by the specified distance
- **backward(distance)**: Moves the robot backward by the specified distance  
- **left(degrees)**: Rotates the robot left by the specified number of degrees
- **right(degrees)**: Rotates the robot right by the specified number of degrees
- **wait(seconds)**: Pauses the robot's execution for the specified number of seconds

These commands may look slightly different depending on your programming environment, but the concepts remain the same. For example, in some environments you might see `move(100)` instead of `forward(100)`, or `turn(-90)` instead of `left(90)`.

## **Creating Movement Patterns**

Movement patterns are sequences of commands that create specific paths or behaviors. By combining basic movement commands in the right order, we can create precise movement patterns for our robots.

### **Simple Patterns**

Let's look at some common movement patterns:

**Line pattern:**

```
forward(100)
wait(1)
backward(100)
```

**Square pattern:**

```
forward(100)
left(90)
forward(100)
left(90)
forward(100)
left(90)
forward(100)
left(90)
```

**Triangle pattern:**

```
forward(100)
left(120)
forward(100)
left(120)
forward(100)
left(120)
```

Notice how these patterns use repetition of simple commands to create recognizable shapes. The key is understanding how the sequence affects the robot's path.

### **Real-World Movement Applications**

Think about how robots move in different environments. A robot vacuum needs to move differently on carpet versus tile floors. On carpet, it might need to move more slowly and use more power. On tile, it can move faster but needs to be careful not to slip. The same basic movement commands are used, but how they're combined changes based on the surface.

Similarly, a school security robot might patrol hallways using these movement patterns:

```
# Patrol a hallway
forward(500)  # Move down the hall
wait(5)       # Pause to scan the area
backward(500) # Return to starting point
```

This simple pattern helps the robot monitor a specific area before returning to its starting position.


## **Activity 1: Program a Virtual Robot Path**

Using the virtual robot simulator provided in the course resources, create a program that makes the robot draw a rectangle. Your rectangle should have sides with a 2:1 ratio (longer sides should be twice the length of shorter sides). Start by planning your command sequence on paper, then implement it in the simulator. How many commands did you need? Did your robot end up facing the same direction it started?
---pagebreak---

## **Combining Multiple Movements**

More complex robot behaviors require combining different types of movement patterns. By nesting patterns within each other or creating functions for reusable movements, we can build sophisticated robot behaviors.

### **Creating Functions for Reusable Movements**

Rather than repeating the same sequence of commands multiple times, we can define functions that perform specific movement patterns:

```
function square(size) {
  for (let i = 0; i < 4; i++) {
    forward(size)
    left(90)
  }
}

function zigzag(length, height, count) {
  for (let i = 0; i < count; i++) {
    forward(length)
    right(90)
    forward(height)
    left(90)
  }
}
```

By creating these reusable functions, we can simplify our main program:

```
square(100)
forward(50)
zigzag(50, 25, 3)
```

This approach makes our code more readable and easier to modify.

### **Complex Movement Examples**

Let's look at how we can combine basic movements to create more interesting robot behaviors:

**Line-following robot:**
```
while (sensor.detectsLine()) {
  if (sensor.lineIsLeft()) {
    left(10)  // Small correction to the left
  } else if (sensor.lineIsRight()) {
    right(10) // Small correction to the right
  } else {
    forward(20) // Move forward when centered on the line
  }
}
```

**Obstacle-avoiding robot:**
```
function avoidObstacle() {
  backward(20)    // Back up a bit
  left(90)        // Turn left
  forward(50)     // Move forward to go around obstacle
  right(90)       // Turn right
  forward(50)     // Move forward past the obstacle
  right(90)       // Turn right again
  forward(50)     // Return to original path
  left(90)        // Face original direction
}

// Main program
while (true) {
  if (sensor.detectsObstacle()) {
    avoidObstacle()
  } else {
    forward(20)
  }
}
```

These examples show how the same basic movement commands can be combined in different ways to create robots that can follow lines or navigate around obstacles.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about the relationship between the code you write and the physical movement of the robot. How does understanding this connection help you write better movement programs?
---stopandreflectEND---

---pagebreak---

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
---pagebreak---

**This lesson could be followed by this game:**
Sequencer game: "Path Programmer" - Students are shown a maze with a start and end point. They must arrange movement commands (forward, backward, left, right) in the correct sequence to navigate the robot through the maze. As levels increase, the maze complexity increases, requiring more precise sequencing and the use of compound movements or repeated patterns to solve efficiently.
