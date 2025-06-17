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

Think about how you use your own senses. When you touch something hot, your brain processes that information and tells your hand to pull away. Robots work in a similar way! A touch sensor can detect pressure, and the robot's program can tell its motors to move away from that pressure.

Sensors come in many types - light sensors detect brightness, distance sensors measure how far away objects are, and sound sensors can hear noises. Each type gives the robot different information about the world around it.

### The Input-Processing-Output Framework

The input-processing-output (IPO) framework is fundamental to understanding how sensors work in robotics:
- **Input**: Sensor data (light levels, distance measurements, touch detection, etc.)
- **Processing**: Code that interprets sensor readings and makes decisions
- **Output**: Actions the robot takes (motors moving, lights turning on, sounds playing)

This framework helps us think systematically about how to connect sensor readings to robot behaviors. For example, an autonomous vacuum robot uses:
- **Input**: Proximity sensors detect walls and obstacles
- **Processing**: Code interprets these readings to determine when to change direction
- **Output**: Motor controllers adjust wheel speeds to turn or stop

Let's look at another example: a robot that follows a line on the floor. The robot uses light sensors pointed at the ground to detect the difference between the dark line and the lighter floor. When the sensor detects the line, the robot's program processes this information and sends commands to the motors to adjust the robot's path and stay on the line. This simple input-processing-output cycle happens continuously, allowing the robot to follow the line even when it curves or changes direction.

In your kitchen, temperature sensors in appliances work the same way. Your refrigerator uses temperature sensors to detect when it's getting too warm inside. The program processes this information and turns on the cooling system to keep your food fresh. When the temperature is low enough, the sensor detects this change, and the program turns the cooling system off again.

---pagebreak---

## Creating Sensor Response Programs

The essence of sensor-based programming is creating conditional responses to sensor inputs. This is typically done using if-then structures and comparison operators.

When we program robots to respond to sensors, we're essentially creating a set of rules for the robot to follow. These rules usually take the form of "if this happens, then do that." For example, "if the distance sensor detects an object less than 10 centimeters away, then stop moving forward and turn right."

In programming, we use conditional statements to create these rules. The most common type is the if-else statement, which allows the robot to choose between different actions based on sensor readings.

### Basic Sensor Response Pattern

```
if (sensor_reading > threshold) {
    perform_action_A();
} else {
    perform_action_B();
}
```

This pattern can be expanded to handle multiple conditions or sensor types. For example, a line-following robot might use:

```
if (left_light_sensor < dark_threshold && right_light_sensor > dark_threshold) {
    turn_right();
} else if (left_light_sensor > dark_threshold && right_light_sensor < dark_threshold) {
    turn_left();
} else if (both_sensors < dark_threshold) {
    move_forward();
} else {
    stop_and_search();
}
```

### Continuous vs. Threshold-Based Responses

Robots can respond to sensors in two primary ways:
1. **Threshold-based**: Taking different actions based on whether sensor readings cross specific values
2. **Continuous**: Adjusting actions proportionally to sensor readings (like slowing down as an obstacle gets closer)

Threshold-based responses are like on-off switches. For example, if a light sensor reading goes above 50, turn on a light; otherwise, keep it off. This is simple to program and works well for many situations.

Continuous responses are more like a dimmer switch. As a robot gets closer to a wall, it might gradually slow down rather than stopping suddenly when it reaches a specific distance. This creates smoother, more natural-looking movements but requires more complex programming.

For example, a robot might adjust its speed based on how close it is to an obstacle:
- When far away (more than 50cm): move at full speed
- When getting closer (20-50cm): slow down proportionally
- When very close (less than 20cm): stop completely

This gradual response makes the robot's movements appear more fluid and natural.

## Activity 1: Program a Virtual Robot with Sensor Responses

In this activity, you'll use a virtual robot simulator to create a program that responds to sensor inputs. Your robot has a distance sensor on the front and touch sensors on each side.

1. Write a program that makes the robot:
   - Move forward when no obstacles are detected
   - Turn right when the distance sensor detects an object less than 10cm away
   - Turn away from a wall when either touch sensor is activated

Test your program in different virtual environments to see how the robot navigates using sensor inputs. How does changing the distance threshold affect the robot's behavior?

---pagebreak---

## Testing Sensor-Based Programs

Sensor programs require thorough testing since they interact with the physical world, which can be unpredictable.

When we program robots to use sensors, we're asking them to interact with the real world, which is messy and unpredictable. A robot might work perfectly in a well-lit classroom but fail completely in a dimly lit hallway. That's why testing is so important!

Testing helps us find problems before they cause our robot to crash into walls or get stuck in corners. It also helps us understand how our robot will behave in different situations and environments.

### Test-Driven Development for Sensors

A systematic approach to testing sensor programs includes:
1. Test individual sensor inputs first (verify sensors are reading correctly)
2. Test simple conditional responses (one sensor, one action)
3. Test complex interactions (multiple sensors affecting behavior)
4. Test edge cases (extreme sensor values, rapid changes in readings)
5. Test in various environmental conditions (different lighting, surfaces, etc.)

When testing sensors, start simple and gradually add complexity. First, make sure each sensor is working correctly on its own. For example, if you're using a light sensor, check that it gives different readings when you shine a flashlight on it versus when you cover it with your hand.

Once you know the sensors are working, test simple responses like "when the touch sensor is pressed, the robot stops." After that, you can test more complex behaviors that use multiple sensors together.

Don't forget to test extreme situations! What happens if all sensors are triggered at once? What if a sensor gives unusually high or low readings? These "edge cases" often reveal problems in your program that you might not have anticipated.

### Debugging Sensor Programs

Common debugging approaches include:
- Adding print/log statements to show sensor values during operation
- Using visualization tools to display sensor readings graphically
- Simplifying complex programs to isolate problems
- Checking sensor calibration and physical mounting

When your robot isn't behaving as expected, debugging helps you find and fix the problem. One of the most useful debugging techniques is to add print statements to your code that show the sensor values as the program runs. This helps you see what the robot is "seeing" and understand why it's making certain decisions.

Sometimes the problem isn't in your code but in how the sensor is mounted or calibrated. A distance sensor that's tilted slightly downward might detect the floor instead of obstacles ahead. A light sensor covered in dust might not detect changes in brightness accurately. Always check the physical setup of your sensors when troubleshooting.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider a robot that needs to navigate through your home environment. How would adding different types of sensors make it more autonomous than one that follows a pre-programmed path? Think about how sensors would allow it to adapt to unexpected situations.
---stopandreflectEND---

---pagebreak---

## Common Sensor Programming Challenges

Even experienced roboticists face challenges when working with sensors. Being aware of these issues can help you troubleshoot your own robot programs.

### Sensor Reliability Issues

- **Noise and Fluctuations**: Sensor readings often contain random variations that must be filtered
- **Environmental Interference**: Lighting conditions can affect vision sensors; magnetic fields can disturb compass sensors
- **Cross-Sensitivity**: Some sensors respond to multiple environmental factors (e.g., temperature affecting humidity readings)

Sensors aren't perfect - they can give slightly different readings even when measuring the same thing. This "noise" in the data can make your robot behave erratically if you don't account for it. For example, a distance sensor might report that an object is 30cm away, then 32cm, then 29cm, even though the object hasn't moved.

Environmental factors can also affect sensor readings. A robot that works perfectly in your classroom might struggle in a different location because of changes in lighting, flooring material, or even temperature. For instance, a line-following robot programmed to detect a black line on a white floor might get confused on a gray carpet.

Some sensors are affected by multiple factors at once. A humidity sensor might give inaccurate readings if the temperature changes dramatically. Understanding these limitations helps you design more robust robot programs.

### Handling Unreliable Sensor Data

- **Filtering Techniques**: Using averages or median of multiple readings
- **Sensor Fusion**: Combining data from multiple sensors for more reliable information
- **Graceful Degradation**: Designing programs to function (perhaps with limited capability) when sensor data is unreliable

To deal with noisy sensor data, you can take multiple readings and calculate an average. For example, instead of reacting to a single distance reading of 25cm, your program might take 5 readings and average them to get a more stable value.

Another approach is to use multiple types of sensors together - called "sensor fusion." A robot might use both a camera and distance sensors to detect obstacles. If one sensor gives unreliable data, the other can compensate. For example, a robot vacuum uses both bumper sensors and infrared distance sensors. If bright sunlight interferes with the infrared sensors, the bumper sensors still work as a backup to prevent collisions.

It's also important to design your programs to handle situations where sensor data might be missing or incorrect. This is called "graceful degradation." For example, if a line-following robot loses sight of the line, instead of freezing in place, it might execute a search pattern to find the line again. This is like when you're walking in the dark and lose your way - you might move your hands around carefully to find the wall again rather than just standing still.

#### Sensor Fusion in Action

Here's a simple example of how sensor fusion works in a robot that needs to navigate a room:

1. **Distance sensor**: Detects walls and large objects from far away
2. **Touch sensor**: Detects when the robot bumps into something
3. **Light sensor**: Helps identify different surfaces or lines to follow

By combining these sensors, the robot can:
- Use the distance sensor to plan paths around obstacles
- Use the touch sensor as a backup if the distance sensor misses something
- Use the light sensor to follow specific paths or avoid certain areas

If one sensor fails or gives bad readings, the others can help the robot continue functioning. For instance, if bright sunlight makes the distance sensor unreliable, the robot can slow down and rely more on its touch sensors until it moves into a shadier area.

#### Graceful Degradation Strategies

When sensors become unreliable, robots need backup plans. Here are some simple strategies:

1. **Safe mode**: If sensors detect conflicting information, the robot can slow down or stop until things make sense again
2. **Backup behaviors**: If a main sensor fails, the robot can switch to using other sensors
3. **Confidence levels**: The robot can assign "trust scores" to different sensor readings and make decisions based on the most trustworthy information

For example, a delivery robot that normally uses GPS to navigate might switch to following visual landmarks if it enters a building where GPS signals are weak. It continues its mission, just using a different method!

---checkyourunderstanding---
Which programming approach would be best for a robot that needs to avoid obstacles?

A. A fixed movement sequence programmed in advance

B. A random movement generator

C. A program that responds to touch or distance sensor inputs

D. A program that only works when controlled by a human
---answer---
The correct answer is C. A program that responds to touch or distance sensor inputs. For obstacle avoidance, the robot needs to sense obstacles (input) and change its movement (output) accordingly, which requires sensor-based programming. If you chose A, this approach doesn't allow for adaptation to unpredictable obstacles. If you chose B, random movements aren't efficient for avoiding obstacles. If you chose D, human control removes autonomy, defeating the purpose of automated obstacle avoidance.
---answerEND---
---checkyourunderstandingEND---

## Key Takeaways

- Sensors provide the input that drives robot decision-making, enabling them to respond to their environment
- Sensor-based programming makes robots more autonomous by allowing them to adapt to changing conditions without human intervention
- The input-processing-output framework shows how sensors connect to actions through the programming logic that interprets sensor data