# 5.11
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