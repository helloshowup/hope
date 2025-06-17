# 5.4
# **Connecting Sensors to Actions**

## **Lesson Podcast Discussion: Enabling Robot Autonomy Through Sensors**

This podcast explores how sensor-based programming allows robots to make decisions independently, responding to their environment without human intervention.

---pagebreak---

## **Sensor Inputs in Programming**

In traditional programming, we create sequences of instructions that execute exactly as written. However, robots that interact with their environment need to gather information about the world around them. This is where sensors become essential.

Sensors act as the "eyes," "ears," and "sense of touch" for robots. They convert physical phenomena like light, sound, or pressure into electrical signals that the robot's processor can understand. In programming terms, sensors provide the **inputs** that drive decision-making.

Think about how you use your own senses. When you touch something hot, your brain quickly processes that information and tells your hand to pull away. Robots work in a similar way, but they need us to program these reactions.

Without sensors, a robot would be like a person trying to walk through a room with their eyes closed and ears plugged. It might follow instructions perfectly, but it couldn't adapt to anything unexpected in its path.

### **The Input-Processing-Output Framework**

Every robotic system follows the **Input-Processing-Output (IPO)** framework:

1. **Input**: Sensors collect data from the environment
2. **Processing**: The robot's program interprets the data and makes decisions
3. **Output**: Actuators (motors, lights, speakers) perform actions based on those decisions

For example, in a line-following robot:
- **Input**: Light sensors detect the contrast between a black line and white background
- **Processing**: The program determines if the robot is veering off the line
- **Output**: Motors adjust speed to steer the robot back onto the line

This framework forms the foundation of all sensor-based programming.

Let's consider another example you might be familiar with: automatic doors at a grocery store. The door uses a motion sensor (input) to detect when someone approaches. The control system processes this information and decides the door should open (processing). Finally, the motors activate to slide the door open (output).

A school security system works in a similar way. Motion sensors (input) detect movement in hallways after hours. The security system (processing) determines if this is unusual activity. Then, it might turn on lights or sound an alarm (output) to respond to the situation.

---pagebreak---

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

---pagebreak---

## **Activity 1: Program a Sensor-Responsive Robot**

Using our virtual robot simulator, create a program that makes the robot respond to different sensor inputs. Your robot should stop when its distance sensor detects an object within 15cm, turn left when a touch sensor on its right side is pressed, and turn right when a touch sensor on its left side is pressed. Test your program with different obstacles to see how effectively your robot navigates around them. This activity demonstrates how sensor inputs directly influence robot behavior.

## **Testing Sensor-Based Programs**

Creating a sensor-based program is only the first step. Testing and refining these programs ensures reliable robot behavior.

### **Systematic Testing Approaches**

To effectively test sensor-based programs:

1. **Start with controlled inputs**: Begin by manually activating sensors to verify basic functionality
2. **Test edge cases**: Check behavior at the boundaries of your threshold values
3. **Create realistic test scenarios**: Test your robot in conditions similar to its intended environment
4. **Incremental development**: Start with simple behaviors and build complexity gradually

When testing a robot with a distance sensor, for example, you might first place an object exactly at your threshold distance (like 15cm) to see if the robot responds correctly. Then try moving the object slightly closer and slightly farther to test the boundaries of your program's decision-making.

It's also important to test in different lighting conditions if you're using light sensors, or on different surfaces if you're using touch sensors. The more thoroughly you test, the more reliable your robot will be when faced with real-world situations.

A good testing plan might look like this:
- Test each sensor individually before combining them
- Test on different surfaces (carpet, tile, wood)
- Test in different lighting conditions (bright, dim, natural light)
- Test with different obstacles (soft objects, hard objects, different shapes)
- Test with multiple obstacles at once

Remember that testing isn't just about finding problems—it's about making your robot smarter and more reliable. Each test helps you refine your program and improve your robot's performance.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider how a robot that follows pre-programmed instructions differs from one that responds to sensor inputs. How does the addition of sensors transform what the robot can accomplish and how it interacts with the world around it?
---stopandreflectEND---

---pagebreak---

## **Common Sensor Programming Challenges**

Even experienced roboticists face challenges when creating sensor-based programs. Understanding these common issues can help you avoid or resolve them.

### **Sensor Reliability Issues**

Sensors don't always provide consistent readings. Factors that can affect sensor reliability include:

1. **Environmental conditions**: Lighting, temperature, and humidity can affect sensor performance
2. **Calibration drift**: Sensors may need regular recalibration to maintain accuracy
3. **Power fluctuations**: Changes in battery voltage can affect sensor readings

To address these issues, robust programs often include:
- Calibration routines that run when the robot starts
- Averaging multiple readings to reduce noise
- Built-in tolerance for minor variations in sensor values

For example, instead of reading a light sensor just once, your program might take five readings and average them together. This helps filter out random fluctuations that could cause your robot to make incorrect decisions.

Another common technique is to add a small "buffer zone" around your threshold values. Instead of triggering an action exactly at a threshold of 500, you might only change behavior if the value goes below 480 or above 520. This prevents the robot from rapidly switching between two behaviors when sensor values hover near the threshold.

### **Sensor Calibration**

Sensors often need calibration to work correctly in different environments. Calibration is like teaching your robot what "normal" looks like so it can detect when something changes.

For a line-following robot, calibration might involve:
1. Holding the robot over the white background and recording the light sensor value
2. Holding the robot over the black line and recording the light sensor value
3. Setting the threshold halfway between these two values

Many robots perform a quick calibration routine when they first turn on. This helps them adjust to the specific lighting and conditions of their environment. Without calibration, a robot that worked perfectly in your classroom might fail completely in a different room with brighter or dimmer lighting.

### **Debugging Sensor Programs**

When your sensor-based program isn't working as expected, try these debugging approaches:

1. **Isolate components**: Test sensors independently from the rest of the program
2. **Print sensor values**: Output sensor readings to understand what the robot is "seeing"
3. **Simplify the program**: Start with basic functionality before adding complexity
4. **Check thresholds**: Ensure your threshold values are appropriate for your environment

One of the most useful debugging techniques is to display sensor values on a screen or through console output. This lets you see exactly what information your robot is receiving. For instance, if your light sensor is reading 300 when you expected 700, you might need to adjust your lighting or recalibrate the sensor.

Remember that debugging is a normal part of programming. Even professional roboticists spend a lot of time testing and fixing their code. Each problem you solve helps you become a better programmer and roboticist.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about everyday devices that use sensors to trigger actions (automatic doors, smart thermostats, or motion-activated lights). How might the functionality of these devices be improved with more sophisticated sensor programming?
---stopandreflectEND---

---checkyourunderstanding---
Which programming approach would be best for a robot that needs to avoid obstacles?

A. A fixed movement sequence programmed in advance

B. A random movement generator

C. A program that responds to touch or distance sensor inputs

D. A program that only works when controlled by a human
---answer---
The correct answer is C. A program that responds to touch or distance sensor inputs. For obstacle avoidance, the robot needs to sense obstacles (input) and change its movement (output) accordingly, which requires sensor-based programming. If you chose A, this approach wouldn't work because the robot couldn't adapt to unpredictable obstacles. If you chose B, random movements wouldn't efficiently avoid obstacles. If you chose D, the robot wouldn't be autonomous and would require constant human monitoring.
---answerEND---
---checkyourunderstandingEND---

**This lesson could be followed by this game:**
Sequencer game: Students are presented with scrambled steps of a sensor-response program and must arrange them in the correct logical order. For example, they might need to sequence the steps for a line-following robot: 1) Read light sensor value, 2) Compare value to threshold, 3) If below threshold, turn left, 4) If above threshold, turn right, 5) Repeat process. This tests students' understanding of the logical flow in sensor-based programming while reinforcing the input-processing-output framework.