# 5.17
## **Creating Sensor Response Programs**

Now that we understand how sensors fit into the programming framework, let's examine how to write programs that respond to sensor inputs.

### **Conditional Statements**

The most common way to handle sensor inputs is through **conditional statements**—typically "if-then-else" structures. These allow the robot to make decisions based on sensor readings.

Basic structure:

```
if (sensor_value meets condition) {
    do_something();
} else {
    do_something_else();
}
```

For example, a program for an obstacle-avoiding robot might look like:

```
if (distance_sensor < 10) {
    turn_right();
} else {
    move_forward();
}
```

This simple program tells the robot: "If there's an obstacle less than 10 centimeters away, turn right; otherwise, keep moving forward."

Conditional statements work like the decisions you make every day. If it's raining, you bring an umbrella. If it's not raining, you leave the umbrella at home. Robots make similar decisions, but they need us to write these rules in code.

You can also create more complex decisions by adding more conditions:

```
if (distance_sensor < 5) {
    back_up();
} else if (distance_sensor < 15) {
    turn_right();
} else {
    move_forward();
}
```

This program gives the robot three possible actions depending on how close an obstacle is.

### **Threshold Values**

When working with sensors, we often need to determine appropriate **"threshold values"** that trigger different actions. These thresholds depend on:

1. The specific sensor being used
2. The environment the robot operates in
3. The desired behavior of the robot

For instance, a light sensor might return values from 0 (complete darkness) to 1023 (bright light). You might set a threshold of 500, where values below indicate a dark line, and values above indicate a light background.

Finding the right threshold often takes experimentation. If you set a light sensor threshold too high or too low, your line-following robot might not detect the line correctly. The perfect threshold depends on the lighting in the room and the contrast between the line and the background.

Think of thresholds like the temperature setting on a thermostat. If you set it to 70°F, the heater turns on when the temperature drops below 70°F and turns off when it rises above 70°F. The threshold (70°F) determines when the action changes.