# Admin
Module 6
Lesson 4
Lesson Title: Connecting Sensors to Actions
# Template
[start of lesson]
# 6.4
# Connecting Sensors to Actions
## Learning Objectives
By the end of this session, you'll be able to:
- Create programs that use sensor inputs to control robot actions
- Understand how sensors connect to the input-processing-output framework
- Test and debug sensor-based programs
### Lesson Podcast Discussion: How Sensors Enable Autonomous Robot Behavior
This podcast explores how properly programmed sensors transform robots from pre-programmed machines into responsive, adaptive systems capable of making decisions based on their environment.

## Sensor Inputs in Programming
Robot sensors are the "eyes and ears" that allow machines to perceive their environment. In programming terms, sensors provide the critical input data that robots need to make decisions. Understanding how to incorporate sensor data into your programs is essential for creating responsive, intelligent robots.

### Types of Sensor Inputs in Code
Different sensors provide different types of data that your program needs to handle:
- **Binary sensors** (like touch sensors) provide simple on/off or true/false values
- **Analog sensors** (like light or distance sensors) provide a range of numerical values
- **Complex sensors** (like cameras) provide structured data requiring more sophisticated processing

When programming with sensors, you'll need to access their values through specific functions or methods. For example:
python
if touch_sensor.is_pressed():
    robot.move_backward()
    
distance = ultrasonic_sensor.get_distance()
if distance < 20:
    robot.turn_left()


## The Input-Processing-Output Framework
The IPO (Input-Processing-Output) framework is fundamental to understanding how sensors connect to robot actions:

1. **Input**: Sensors collect data from the environment
2. **Processing**: Your program analyzes the sensor data and makes decisions
3. **Output**: The robot executes actions based on those decisions

### Decision Structures for Sensor Processing
The most common programming structures for handling sensor inputs are:

- **If-else statements**: Make simple decisions based on sensor readings
python
if light_sensor.get_value() < 50:
    robot.turn_on_lights()
else:
    robot.turn_off_lights()


- **Loops with conditionals**: Continuously monitor sensors and respond
python
while True:
    if distance_sensor.get_value() < 10:
        robot.stop()
    else:
        robot.move_forward()


- **Functions**: Encapsulate sensor-response behavior
python
def avoid_obstacle():
    robot.stop()
    robot.turn_right(90)
    robot.move_forward(2)


## Creating Sensor Response Programs
Now let's look at how to create complete programs that use sensors to drive robot behavior.

### Basic Sensor Response Pattern
Most sensor-based programs follow this basic pattern:

1. Initialize the robot and sensors
2. Enter a continuous loop that:
   - Reads sensor values
   - Processes the values using conditionals
   - Executes appropriate actions
3. Clean up resources when done

Here's a simple example of a light-following robot:

python
# Initialize
robot = Robot()
light_sensor = LightSensor(port=1)

# Main loop
while not robot.button.is_pressed():
    light_value = light_sensor.get_value()
    
    if light_value > 70:  # Bright light detected
        robot.move_forward()
    elif light_value > 30:  # Medium light
        robot.turn_toward_light()
    else:  # Low light
        robot.stop()
        
# Cleanup
robot.close()


## **Activity 1: Program a Robot to Respond to a Touch Sensor**

In this activity, you'll create a simple program for a virtual robot that uses a touch sensor to detect obstacles. Open the virtual robot simulator in a new tab and write a program that:
1. Makes the robot move forward continuously
2. Detects when the touch sensor is pressed (indicating an obstacle)
3. Makes the robot back up, turn 90 degrees right, and continue moving forward
4. Test your program with various obstacle configurations to see how well it works

## Testing Sensor-Based Programs
Sensor-based programs require thorough testing because they interact with the physical world, which can be unpredictable.

### Systematic Testing Approaches
When testing sensor programs:

1. **Test individual sensor readings**: Verify that your program correctly reads the sensor values
2. **Test thresholds and boundaries**: Check if your program responds correctly at the edge of decision thresholds
3. **Test response actions**: Ensure the robot performs the expected actions when sensor conditions are met
4. **Test in different environments**: Try your program under different lighting conditions, surfaces, or obstacle arrangements

### Debugging Sensor Programs
Common issues in sensor programming include:

- **Incorrect thresholds**: Your sensor values may need calibration for different environments
- **Timing issues**: Sensor readings might be too fast or too slow for effective decision-making
- **Conflicting sensor inputs**: Multiple sensors might suggest contradictory actions

## Stop and reflect

**CHECKPOINT:** Consider a robot that navigates through a room without bumping into walls or objects. What sensors would it need, and how would you connect those sensors to movement decisions in your code?

## Common Sensor Programming Challenges
Even experienced programmers face challenges when working with sensors. Here are some common issues and solutions:

### Sensor Noise and Fluctuation
Sensors rarely provide perfectly stable readings. They often fluctuate due to environmental factors or hardware limitations.

**Solutions:**
- Add averaging to smooth out readings: `average_value = (reading1 + reading2 + reading3) / 3`
- Implement debouncing for binary sensors to prevent rapid switching
- Use hysteresis (different thresholds for turning on vs. turning off)

### Multiple Sensor Coordination
Many advanced robots use multiple sensors that must work together.

**Solutions:**
- Create priority systems for when sensors conflict
- Fuse sensor data to get more reliable information
- Implement state machines to manage complex decision-making

### Failure Detection and Recovery
Sensors can fail or provide incorrect readings.

**Solutions:**
- Add validation checks to identify impossible readings
- Implement timeouts for when sensors stop responding
- Create fallback behaviors when sensors fail

### **Check your understanding**
Which programming approach would be best for a robot that needs to avoid obstacles?
A. A fixed movement sequence programmed in advance
B. A random movement generator
C. A program that responds to touch or distance sensor inputs
D. A program that only works when controlled by a human

Choose your answer and check it below.
The correct answer is C. A program that responds to touch or distance sensor inputs. For obstacle avoidance, the robot needs to sense obstacles (input) and change its movement (output) accordingly, which requires sensor-based programming. If you chose A, fixed sequences don't adapt to unpredictable obstacles. If you chose B, random movements aren't reliable for avoiding obstacles. If you chose D, you've eliminated the autonomous capability needed for independent obstacle avoidance.

## Key Takeaways
- Sensors provide the input that drives robot decision-making, allowing robots to respond to their environment
- Sensor-based programming makes robots more autonomous by enabling them to adapt their behavior based on what they detect
- The input-processing-output framework shows how sensors connect to actions through your program's decision logic
[End of Lesson]

## Instructional designer notes of lesson 6.4
**This lesson fits into the the overall module of Advanced Programming in the following ways:**
- It builds on basic programming concepts by adding sensor inputs as a way to make programs more dynamic and responsive
- It introduces conditional logic and decision-making based on external inputs, a key advanced programming concept
- It demonstrates how the input-processing-output model is implemented in real robot behaviors
- It prepares students for more complex programming challenges that involve multiple sensors and sophisticated decision logic

**This lesson could be followed by this game:**
Sequencer game: Players must arrange the correct sequence of programming steps to make a robot respond to specific sensor inputs. For example, students would need to arrange code blocks in the correct order to program a robot that stops when its distance sensor detects an object within 10cm, backs up for 2 seconds, turns right, and then continues forward until it detects another obstacle.