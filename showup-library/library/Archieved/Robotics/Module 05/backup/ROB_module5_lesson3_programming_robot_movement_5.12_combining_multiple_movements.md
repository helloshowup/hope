# 5.12
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