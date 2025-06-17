# Admin
Module 8
Lesson 4
Lesson Title: Connecting Sensors to Actions
# Template
[start of lesson]
# 8.4
# Connecting Sensors to Actions
## Learning Objectives
By the end of this session, you'll be able to:
- Create programs that use sensor inputs to control robot actions
- Understand how sensors connect to the input-processing-output framework
- Test and debug sensor-based programs
## Lesson Podcast Discussion: How Sensors Enable Robot Autonomy
This podcast explores how programming robots to interpret sensor data transforms them from simple pre-programmed machines into autonomous systems capable of reacting to their environment.

## Sensor Inputs in Programming
When we program robots, we need a way to incorporate information from the physical world. Sensors serve as the robot's senses, allowing it to perceive its environment. In programming terms, sensors provide the input data that the robot can use to make decisions.

### The Input-Processing-Output Framework
The input-processing-output (IPO) framework is fundamental to understanding how sensors work in robotics:
- **Input**: Sensor data (light levels, distance measurements, touch detection, etc.)
- **Processing**: Code that interprets sensor readings and makes decisions
- **Output**: Actions the robot takes (motors moving, lights turning on, sounds playing)

This framework helps us think systematically about how to connect sensor readings to robot behaviors. For example, an autonomous vacuum robot uses:
- Input: Proximity sensors detect walls and obstacles
- Processing: Code interprets these readings to determine when to change direction
- Output: Motor controllers adjust wheel speeds to turn or stop

## Creating Sensor Response Programs
The essence of sensor-based programming is creating conditional responses to sensor inputs. This is typically done using if-then structures and comparison operators.

### Basic Sensor Response Pattern

if (sensor_reading > threshold) {
    perform_action_A();
} else {
    perform_action_B();
}


This pattern can be expanded to handle multiple conditions or sensor types. For example, a line-following robot might use:


if (left_light_sensor < dark_threshold && right_light_sensor > dark_threshold) {
    turn_right();
} else if (left_light_sensor > dark_threshold && right_light_sensor < dark_threshold) {
    turn_left();
} else if (both_sensors < dark_threshold) {
    move_forward();
} else {
    stop_and_search();
}


### Continuous vs. Threshold-Based Responses
Robots can respond to sensors in two primary ways:
1. **Threshold-based**: Taking different actions based on whether sensor readings cross specific values
2. **Continuous**: Adjusting actions proportionally to sensor readings (like slowing down as an obstacle gets closer)

## Activity 1: Program a Virtual Robot with Sensor Responses

In this activity, you'll use a virtual robot simulator to create a program that responds to sensor inputs. Your robot has a distance sensor on the front and touch sensors on each side.

1. Write a program that makes the robot:
   - Move forward when no obstacles are detected
   - Turn right when the distance sensor detects an object less than 10cm away
   - Turn away from a wall when either touch sensor is activated

Test your program in different virtual environments to see how the robot navigates using sensor inputs. How does changing the distance threshold affect the robot's behavior?

## Testing Sensor-Based Programs
Sensor programs require thorough testing since they interact with the physical world, which can be unpredictable.

### Test-Driven Development for Sensors
A systematic approach to testing sensor programs includes:
1. Test individual sensor inputs first (verify sensors are reading correctly)
2. Test simple conditional responses (one sensor, one action)
3. Test complex interactions (multiple sensors affecting behavior)
4. Test edge cases (extreme sensor values, rapid changes in readings)
5. Test in various environmental conditions (different lighting, surfaces, etc.)

### Debugging Sensor Programs
Common debugging approaches include:
- Adding print/log statements to show sensor values during operation
- Using visualization tools to display sensor readings graphically
- Simplifying complex programs to isolate problems
- Checking sensor calibration and physical mounting

## Stop and reflect

**CHECKPOINT:** Consider a robot that needs to navigate through your home environment. How would adding different types of sensors make it more autonomous than one that follows a pre-programmed path? Think about how sensors would allow it to adapt to unexpected situations.

## Common Sensor Programming Challenges
Even experienced roboticists face challenges when working with sensors. Being aware of these issues can help you troubleshoot your own robot programs.

### Sensor Reliability Issues
- **Noise and Fluctuations**: Sensor readings often contain random variations that must be filtered
- **Environmental Interference**: Lighting conditions can affect vision sensors; magnetic fields can disturb compass sensors
- **Cross-Sensitivity**: Some sensors respond to multiple environmental factors (e.g., temperature affecting humidity readings)

### Handling Unreliable Sensor Data
- **Filtering Techniques**: Using averages or median of multiple readings
- **Sensor Fusion**: Combining data from multiple sensors for more reliable information
- **Graceful Degradation**: Designing programs to function (perhaps with limited capability) when sensor data is unreliable

### **Check your understanding**
Which programming approach would be best for a robot that needs to avoid obstacles?
A. A fixed movement sequence programmed in advance
B. A random movement generator
C. A program that responds to touch or distance sensor inputs
D. A program that only works when controlled by a human

Choose your answer and check it below.
The correct answer is C. A program that responds to touch or distance sensor inputs. For obstacle avoidance, the robot needs to sense obstacles (input) and change its movement (output) accordingly, which requires sensor-based programming. If you chose A, this approach doesn't allow for adaptation to unpredictable obstacles. If you chose B, random movements aren't efficient for avoiding obstacles. If you chose D, human control removes autonomy, defeating the purpose of automated obstacle avoidance.

## Key Takeaways
- Sensors provide the input that drives robot decision-making, enabling them to respond to their environment
- Sensor-based programming makes robots more autonomous by allowing them to adapt to changing conditions without human intervention
- The input-processing-output framework shows how sensors connect to actions through the programming logic that interprets sensor data

[End of Lesson]
## Instructional designer notes of lesson 8.4
**This lesson fits into the the overall module of Robots Helping People in the following ways:**
- It builds on previous lessons about robot capabilities and sensor types, showing how programming connects these components to create useful behaviors
- It demonstrates how sensors enable robots to interact with humans and environments more effectively and safely
- It connects the technical aspects of programming with the practical applications of robots that can respond to their surroundings
- It prepares students for later lessons on complex robot behaviors by establishing the foundation of sensor-based decision-making

**This lesson could be followed by this game:**
Sequencer game: Students would be presented with scrambled steps for creating a sensor-based robot program and must arrange them in the correct order. For example, they might need to sequence these steps: 1) Identify the needed sensor type, 2) Set up sensor input in the program, 3) Create a conditional statement to check sensor values, 4) Program the corresponding robot actions, 5) Test the sensor response, 6) Debug any issues. This game reinforces the systematic process of developing sensor-based programs.