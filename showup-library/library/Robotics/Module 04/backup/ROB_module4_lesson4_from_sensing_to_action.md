# 4.
# From Sensing to Action

### **Lesson Podcast Discussion:** The Information Pathway in Robotics
This podcast explores how information flows from sensor inputs through processing systems to trigger meaningful robot actions.

## **The Information Pathway**

### **Sensor Input Collection**
Robots use sensors as their "eyes and ears" to understand the world around them. Just like how your eyes detect light and your ears detect sound, robot sensors detect different types of physical information from the environment. For example, a light sensor detects brightness levels, a distance sensor measures how far away objects are, and a touch sensor detects when something makes contact with the robot.

When a sensor detects something in the environment, it converts that physical information into electrical signals. Think of it like translating one language into another. A temperature sensor, for instance, converts heat levels into electrical signals that the robot can understand. These electrical signals are the "raw data" that flows into the robot's brain (its processor) for the next step in the pathway.

### **Data Processing and Interpretation**
The robot then interprets this filtered data using programmed rules. For example, if a light sensor detects a value below 20, the robot might interpret this as "it's dark." If a distance sensor reports a value of 5 centimeters, the robot might interpret this as "there's an obstacle very close to me." This interpretation transforms raw numbers into meaningful information that the robot can use to make decisions.

Some robots use special techniques to clean up messy sensor data. For instance, averaging multiple readings can help reduce errors, similar to how you might take the average of several test scores. Other robots use "threshold filtering" where they only respond when a sensor reading crosses a certain value - like only reacting to sounds louder than a whisper.

### **Triggering Robot Responses**
The connection between sensor interpretation and robot action is defined by the robot's programming. Programmers create rules that tell the robot exactly what to do in response to specific sensor information. This final step completes the information pathway from sensing the environment to taking action in it.

## **Activity 1: Sensor-Decision Flowcharts**
Create a simple flowchart showing how robots make decisions based on different sensor inputs, such as "If light sensor detects darkness, then turn on headlight." Add at least one additional decision branch showing what happens if the sensor detects bright light instead. Your flowchart should include the sensor input, decision point, and resulting robot actions.

## **Decision-Making Based on Sensor Data**

### **Simple If-Then Logic**
**If-then statements** are the building blocks of robot decision-making. These simple logical rules tell the robot what to do when certain conditions are met. For example: "IF the temperature sensor reads above 30 degrees Celsius, THEN turn on the cooling fan." This type of logic creates a direct connection between what the robot senses and how it responds.

### **Simple If-Then Logic**
Programmers often use **if-then-else structures** to cover all possible scenarios. The "else" part tells the robot what to do when the "if" condition isn't true. For example: "IF the distance sensor detects an object within 10 cm, THEN stop and turn right, ELSE continue moving forward." This ensures the robot always has a clear action to take, no matter what its sensors detect.

### **Combining Multiple Sensor Inputs**

Real-world robots rarely rely on just one sensor to make decisions. Instead, they combine information from multiple sensors to get a more complete picture of their environment. For example, a robot vacuum might use a combination of bump sensors, cliff sensors, and camera sensors to navigate safely around your home.

When working with multiple sensors, robots need ways to prioritize or combine the information. One approach is to use **"AND" and "OR" logic**. For example: "IF the light sensor detects darkness AND the motion sensor detects movement, THEN turn on the security light." This means both conditions must be true for the action to happen. With "OR" logic, only one condition needs to be true: "IF the smoke sensor detects smoke OR the temperature sensor reads above 100 degrees, THEN trigger the alarm."

### **Combining Multiple Sensor Inputs**
In self-driving cars, this combination of sensors is critical for safety. These vehicles use cameras to see lane markings, radar to detect other vehicles, and ultrasonic sensors to measure close distances when parking. The car's computer combines all this information to make driving decisions, giving highest priority to avoiding collisions with people or objects.

---stopandreflect---
**CHECKPOINT:** Think about a time when one of your senses gave you incorrect information, such as an optical illusion or misheard sound. How might similar sensory misinterpretations affect a robot's ability to function correctly in its environment?
---stopandreflectEND---



### **Prioritizing Conflicting Sensor Information**

Sometimes sensors provide contradictory information, and robots need strategies to resolve these conflicts. Imagine a robot with both a light sensor and a camera. The light sensor indicates it's dark, but the camera is still capturing clear images. Which sensor should the robot trust?

One common approach is to establish a **"sensor hierarchy"** where certain sensors are trusted more than others in specific situations. For example, safety-related sensors like obstacle detectors might always take priority over other sensors. If the obstacle sensor says "stop" but the line-following sensor says "go forward," the robot will stop to avoid a collision.

### **Prioritizing Conflicting Sensor Information**
Engineers design robots with **backup systems** so they can still function even if one sensor fails. For example, a delivery robot that normally uses cameras to navigate might switch to using sonar sensors if its cameras get covered in mud. This is like how you might use your sense of touch to find your way around a dark room when you can't see.
---pagebreak---
## **Troubleshooting Sensor Systems**

### **Common Sensor Failures**

Sensors can fail in several ways, each affecting robot behavior differently. One common issue is **complete sensor failure**, where the sensor stops working entirely. For example, a broken light sensor might always report the same value regardless of actual light conditions. This would prevent a robot from distinguishing between light and dark environments.

**Intermittent failures** occur when sensors work sometimes but not others. These can be particularly frustrating to diagnose because the robot might appear to function correctly during testing but fail during actual use. Loose connections often cause intermittent failures – the physical wires connecting the sensor to the robot's processor might disconnect temporarily when the robot moves.

**Environmental interference** can also cause sensor problems. For instance, infrared distance sensors might give false readings in bright sunlight, and magnetic sensors can be affected by nearby metal objects. Understanding these common failures helps in diagnosing why a robot isn't behaving as expected.
### **Common Sensor Failures**

Sensors often need **calibration** to provide accurate readings. Calibration is like setting a baseline or reference point for the sensor. For example, a color sensor might need to be calibrated to recognize what "red" looks like under current lighting conditions. Without proper calibration, sensors may misinterpret their environment.

Reliability issues can arise from **sensor drift**, where sensor readings gradually become less accurate over time. This might happen due to component aging, temperature changes, or physical wear. For example, a distance sensor that was perfectly accurate when new might gradually report distances that are slightly off, causing a robot to misjudge how far it is from obstacles.

To improve reliability, robots often include **redundant sensors** (multiple sensors that measure the same thing) or **complementary sensors** (different types of sensors that can verify each other's readings). For example, a robot might use both ultrasonic and infrared sensors to measure distance, comparing the readings to ensure accuracy.

### **Calibration and Reliability Issues**

Analyze this scenario: A line-following robot consistently veers off its path despite having properly functioning motors. Identify which sensor might be malfunctioning and explain why. Then describe what tests you would perform to confirm your diagnosis and how you would fix the issue.

### **Testing and Verification Methods**

Systematic testing is essential for verifying sensor functionality. One effective approach is **isolation testing**, where you check each sensor individually to see if it's working correctly. For a line-following robot, you might place it on different colored surfaces and observe whether the line sensor values change appropriately.

**Comparison testing** involves checking a suspect sensor against a known good sensor. If you have two identical robots, you can compare sensor readings between them under the same conditions. If one robot's light sensor reads 50 while the other reads 500 in the same lighting, you've likely found your problem.

## **Activity 2: Sensor Troubleshooting Scenarios**
Documentation is crucial during testing. Keep records of sensor readings under different conditions to establish what "normal" looks like. This baseline makes it easier to identify when a sensor is behaving unusually and needs attention.

A helpful troubleshooting decision tree for sensor problems might look like this:

### **Testing and Verification Methods**
3. Are the readings consistent or do they jump around? Inconsistent readings might indicate interference.
4. Do readings match what you expect? If not, calibration might be needed.

---stopandreflect---
**CHECKPOINT:** Consider a robot trying to navigate a maze. What sequence of sensor inputs and actions would help it find the exit? Think about how the robot would need to prioritize different types of sensor information to make effective navigation decisions.
---stopandreflectEND---

---checkyourunderstanding---
If a robot with a distance sensor keeps bumping into walls, what is the most likely problem?

A. The distance sensor is properly functioning but set to the wrong distance threshold

B. The robot's wheels are turning too quickly for the sensor to react

C. The distance sensor is malfunctioning or not properly connected to the processing unit

D. The walls are made of a material that is invisible to the sensor
---answer---
The correct answer is C. The distance sensor is malfunctioning or not properly connected to the processing unit. If a robot with a distance sensor continues to bump into walls, the most likely issue is that the sensor itself is malfunctioning or the connection between the sensor and the processing unit is faulty, preventing the robot from receiving accurate distance information. If you chose a different answer, remember that while threshold settings and speed can be factors, the complete failure to detect walls usually indicates a hardware or connection problem.
---answerEND---
---checkyourunderstandingEND---

**This lesson could be followed by this game:**
Role Play: Human Robot - One student acts as a 'robot' following simple sensor-based instructions from a 'programmer' student. The robot must respond to simulated sensor inputs (colored cards representing different sensor readings) with specific actions. For example, when shown a red card (representing a proximity alert), the "robot" must stop and change direction, while a green card might indicate clear path ahead, prompting the robot to move forward.


