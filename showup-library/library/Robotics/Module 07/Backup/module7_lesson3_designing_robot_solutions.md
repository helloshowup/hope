# 7.3
# **Designing Robot Solutions**
## **Learning Objectives**
By the end of this session, you'll be able to:
- Develop comprehensive robot design plans that address specific problems
- Select appropriate sensors, processors, and actuators based on the input-processing-output framework
- Incorporate ethical considerations into robot design decisions

### **Lesson Podcast Discussion: The Input-Processing-Output Framework for Effective Robot Design**

The Input-Processing-Output (IPO) framework gives us a simple but powerful way to think about how robots work. Just like humans use our senses to gather information, our brains to think about it, and our muscles to respond, robots follow a similar pattern. They collect data through **sensors** (input), analyze this information with their **processors** (processing), and then take action through motors and other mechanisms (output). This framework helps us break down complex robot designs into manageable parts that work together. By thinking about robot design this way, we can make sure our robots have all the right parts to solve the specific problem we're working on.

For example, a weather station robot that helps monitor school garden conditions uses this framework effectively:
- Input: Temperature sensors, humidity sensors, and light sensors gather environmental data
- Processing: A microcontroller analyzes the readings to determine if conditions are too dry, too wet, or just right
- Output: The robot activates water pumps, opens shade covers, or sends alerts to student caretakers

---pagebreak---

## **From Problem to Design Specifications**

### **Translating Requirements into Specifications**

When we identify a problem that a robot could solve, we need to turn our general ideas into specific technical details. For example, if we want a robot to help elderly people pick up items from the floor, we need to figure out exactly what the robot needs to do. How heavy should the items be? How will the robot know what to pick up? How fast should it move?

This process is like turning a wish list into a shopping list. Instead of saying "I want a robot that helps people," we need to say "I need a robot that can detect objects on the floor, pick up items weighing up to 2 pounds, and safely hand them to a person." These specific details help us choose the right parts and design the right programs for our robot.

To help organize your ideas, try creating a simple design documentation table like this:

| General Requirement | Specific Specification |
|---------------------|------------------------|
| "Help people pick up items" | Detect and lift objects up to 2 pounds |
| "Be safe to use" | Move at maximum speed of 1 foot per second |
| "Work when needed" | Battery lasts at least 3 hours |

### **Setting Design Parameters**

**Design parameters** are the measurable goals that our robot needs to meet. These are like the rules of a game - they tell us what success looks like. For a delivery robot, parameters might include:
- Maximum speed: 3 miles per hour
- Battery life: at least 4 hours
- Weight capacity: up to 10 pounds
- Navigation accuracy: within 6 inches of target

By setting clear parameters, we can test our robot to see if it meets our needs. These numbers also help us choose the right components. If we need to carry 10 pounds, we'll need motors strong enough for that weight. If we need 4 hours of battery life, we'll need to calculate power consumption and choose the right battery size.

### **Creating Design Constraints**

**Constraints** are the limitations we need to work within. These might include:
- Budget: how much money we can spend
- Size: how big the robot can be
- Weight: how heavy the robot can be
- Time: how long we have to build it
- Available materials: what parts we can use

For example, if we're designing a robot for a school hallway, it needs to be small enough to navigate without blocking students. If we're working with a $200 budget, we need to choose affordable components. Identifying these constraints early helps us avoid designing something that can't actually be built or used in the real world.

While constraints might seem limiting, they can actually spark creativity! When the Mars rover designers had strict weight limits for their robot, they had to invent clever new ways to make lightweight but strong components. Sometimes having boundaries forces us to think of solutions we wouldn't have considered otherwise.

---pagebreak---

## **Input Component Selection**

### **Matching Sensors to Information Needs**

Choosing the right sensors is like giving your robot the senses it needs to understand its world. Different problems require different types of information:

- If your robot needs to follow a line, **light sensors** can detect the difference between the line and the background.
- If your robot needs to avoid obstacles, **ultrasonic or infrared distance sensors** can measure how far away objects are.
- If your robot needs to identify colors, a **color sensor** would be essential.
- If your robot needs to know which way is up or how it's moving, **accelerometers and gyroscopes** can provide that information.

The key is to think about what information your robot needs to solve its specific problem. A robot that sorts recycling needs to identify different materials, while a robot that waters plants needs to detect soil moisture. By matching sensors to these information needs, we make sure our robot can "see" what it needs to see.

For example, a garden helper robot might use these sensors:
- Soil moisture sensors to know when plants need water
- Light sensors to track sunlight levels
- Temperature sensors to monitor growing conditions
- Color sensors to identify ripe vegetables

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider a robot you might design to solve a real-world problem. What types of information would this robot need to gather from its environment, and what sensors would be most appropriate for collecting this data?
---stopandreflectEND---

### **Environmental Considerations for Sensors**

The environment where your robot will operate greatly affects which sensors will work best. Imagine trying to use a regular camera in a dark room or a paper-based touch sensor in the rain - they simply wouldn't work!

For outdoor robots, you need sensors that can handle sunlight, rain, dust, and temperature changes. Waterproof ultrasonic sensors might be better than infrared sensors that can be confused by bright sunlight. For robots in noisy factories, sound-based sensors might not work well, but vibration or proximity sensors could be perfect.

Even the surfaces in the environment matter. A line-following robot might work perfectly on smooth floors but fail on carpet where the line is harder to detect. By thinking about the specific conditions your robot will face, you can choose sensors that will work reliably in that environment.

### **Sensor Placement and Configuration**

Where you place sensors on your robot is just as important as which sensors you choose. Think about how humans position our eyes, ears, and hands to best sense the world around us.

For a robot that needs to avoid obstacles, placing distance sensors at the front makes sense, but adding sensors to the sides and back provides a more complete view of the surroundings. A line-following robot needs its light sensors positioned close to the ground and directly over the line.

Sometimes you need multiple sensors of the same type working together. For example, two light sensors side by side can help a line-following robot stay centered on the line. Three ultrasonic sensors pointing in different directions give a robot better awareness of obstacles than just one sensor pointing forward.

The height, angle, and spacing of sensors all affect what information the robot receives. Testing different configurations helps find the optimal placement for your specific robot's needs.

## **Activity 1: Robot Blueprint Creation**

Using the provided template, develop a detailed design plan that specifies all inputs, processing algorithms, and outputs for a robot designed to solve a specific challenge of your choice. Include diagrams indicating sensor placement, processor specifications, and actuator configurations that directly address the problem requirements.

---pagebreak---

## **Processing Component Planning**

### **Algorithm Development**

**Algorithms** are step-by-step instructions that tell your robot how to make sense of sensor data. Think of algorithms as recipes that transform raw information into meaningful understanding.

For example, a simple algorithm for a line-following robot might be:
1. Read values from left and right light sensors
2. If the left sensor detects the line (sees black), turn slightly right
3. If the right sensor detects the line, turn slightly left
4. If both sensors detect the line, go straight
5. If neither sensor detects the line, make a larger turn to find the line again

More complex robots might use algorithms that combine data from multiple sensors. A robot that navigates a room might combine distance sensor readings with information from a digital compass to create a map of its surroundings.

The key is to start with simple algorithms and test them thoroughly before adding complexity. Even advanced robots often use combinations of simple algorithms rather than one extremely complicated one.

When developing algorithms, it's important to balance structure with creativity. While following a step-by-step approach helps ensure your robot works reliably, don't be afraid to experiment with new ideas! Some of the best robot designs come from trying unusual approaches to solving problems. For example, robot designers working on the Mars rovers had to create entirely new algorithms for navigating the Martian surface because no one had driven a robot on Mars before.

### **Decision Logic Design**

**Decision logic** is how your robot chooses what to do based on the information it has processed. This is like creating a flowchart of "if-then" statements that guide your robot's behavior.

For example, a plant-watering robot might use decision logic like:
- IF soil moisture is below 30%, THEN activate water pump for 5 seconds
- IF soil moisture is between 30-60%, THEN check again in 6 hours
- IF soil moisture is above 60%, THEN check again in 12 hours

Good decision logic anticipates different situations and provides clear instructions for each one. It's important to include what the robot should do in unexpected situations too. What if a sensor fails? What if the robot gets stuck? Adding safety conditions and fallback behaviors makes your robot more reliable.

Creating a visual flowchart of your decision logic before programming can help you spot potential problems and ensure your robot will behave as expected in all situations.

### **Programming Considerations**

Once you've designed your algorithms and decision logic, you need to translate them into a programming language your robot can understand. Different robots use different programming languages and environments:

- Block-based languages like Scratch or Blockly are great for beginners and provide a visual way to create programs
- Text-based languages like Python or C++ offer more flexibility but require more coding knowledge
- Some robot kits come with their own specialized programming environments

When programming your robot, consider these best practices:
- Break your program into smaller functions that each handle one specific task
- Add comments to explain what each part of your code does
- Use variables with clear names that describe what they represent
- Test small parts of your program before combining them into the full system

Remember that programming is an iterative process - you'll likely need to test, adjust, and improve your code multiple times before it works perfectly.

A helpful way to document your robot's programming is to create a simple decision tree diagram that shows how your robot will respond to different situations. This can serve as a blueprint before you start coding and help others understand how your robot works.

## **Output Component Selection**

### **Choosing Appropriate Actuators**

**Actuators** are the parts that allow your robot to move and interact with the world. Choosing the right actuators depends on what actions your robot needs to perform:

- **DC motors** provide continuous rotation and are great for wheels that need to spin continuously
- **Servo motors** can move to precise positions and are perfect for robot arms, grippers, or steering mechanisms
- **Stepper motors** move in exact increments and work well for precise positioning like in 3D printers
- **Solenoids** create linear (straight line) motion and can be used for simple pushing or pulling actions
- Speakers, lights, and displays are also actuators that provide feedback or information

Match your actuator to the specific movement needed. If your robot needs to pick up delicate objects, a gripper with servo motors and pressure sensors might be best. If it needs to move quickly across a room, powerful DC motors with good wheels would be more appropriate.

### **Power and Movement Requirements**

Every actuator needs power to work, and choosing the right power system is crucial for your robot's success. Here's how to think about power requirements:

1. Calculate how much power each motor or actuator needs when running at maximum effort
2. Determine how many actuators might be running at the same time
3. Add some extra capacity for safety (usually 20-30% more than your calculation)
4. Choose batteries that can provide this power for your desired run time

For movement, consider:
- How fast does your robot need to move?
- How much weight does it need to carry or push?
- Does it need to climb inclines or navigate rough terrain?
- How precise does its movement need to be?

These questions help you select motors with the right speed, torque (turning force), and control capabilities. For example, a robot that needs to climb stairs needs motors with high torque, while a robot that draws pictures needs motors with precise positioning.

### **Feedback Mechanisms**

**Feedback mechanisms** help your robot confirm that its actions worked as intended. Without feedback, a robot is like a person trying to pick up objects while blindfolded!

Simple feedback can come from the same sensors used for input. For example, a line-following robot can tell if it's successfully following the line by continuing to detect it with its sensors.

More complex feedback might include:
- Encoders on motors that count rotations to track movement distance
- Current sensors that detect if a motor is straining (perhaps because it's stuck)
- Cameras that verify if an object was successfully picked up
- Contact switches that confirm when a gripper has closed on an object

Good feedback systems allow your robot to detect and correct errors. If a robot arm tries to pick up an object but the object slips, feedback sensors can detect this failure and trigger another attempt or alert the user.

## **Activity 2: Ethical Design Checklist**

Review your robot blueprint design using the provided ethical considerations checklist. Evaluate your design for safety features, privacy protections, accessibility considerations, and environmental impact. Modify your design to address any ethical concerns identified, documenting the changes and their justifications.

---pagebreak---

## **Ethical Design Considerations**

### **Safety in Robot Design**

Safety should always be a top priority when designing robots. Even simple robots can cause harm if not designed carefully. Here are key safety considerations to include in your designs:

Physical safety features might include:
- Rounded edges instead of sharp corners
- Speed limitations to prevent dangerous collisions
- Weight distribution that prevents tipping over
- Emergency stop buttons or commands
- Protective covers over moving parts like gears or motors

Operational safety features include:
- Obstacle detection and avoidance systems
- Battery level monitoring to prevent unexpected shutdowns
- Fail-safe behaviors (what the robot does if something goes wrong)
- Testing procedures to verify safe operation before use

Remember that safety isn't just about preventing immediate physical harm. A robot that makes loud, startling noises might be safe physically but still cause stress or fear. A complete safety approach considers all ways your robot might affect people and animals around it.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider what potential unintended consequences your robot design might have, and think about specific design modifications you could implement to mitigate these risks.
---stopandreflectEND---

### **Privacy and Data Collection**

Many robots collect data about their environment and the people around them. As designers, we need to be thoughtful about what data our robots collect and how that data is used:

- Collect only the data your robot truly needs to function
- Be transparent about what information is being collected
- Store data securely and delete it when it's no longer needed
- Consider using on-device processing instead of sending data to the cloud
- Provide clear ways for users to control data collection

For example, if your robot uses a camera to navigate, does it need to save the images it captures? Could it process the visual information and then immediately delete the raw images? If your robot records sound to respond to voice commands, can you add a clear indicator light that shows when it's listening?

Even simple robots can raise privacy concerns. A robot that maps a home to vacuum floors is creating a detailed layout of private spaces. Thinking about these issues during the design phase helps create robots that respect people's privacy.

### **Accessibility and Inclusivity**

Good robot design considers the needs of all potential users, including people with different abilities, ages, and backgrounds. Here are ways to make your robot more accessible and inclusive:

- Provide multiple ways to interact with the robot (voice, touch, visual)
- Use clear, simple language in any instructions or interfaces
- Test your robot with diverse users to identify potential barriers
- Consider height, reach, and strength requirements for physical interaction
- Make sure any visual indicators are visible to people with color blindness
- Provide adjustable settings for speed, volume, and sensitivity

For example, a robot with buttons should have tactile indicators so users can feel the difference between buttons without seeing them. A robot that gives instructions should provide both visual and audio feedback.

Remember that accessibility features often benefit everyone, not just people with specific needs. Clear instructions, intuitive controls, and multiple feedback methods make robots easier for all users to understand and operate.

---checkyourunderstanding---
When designing a line-following robot, which of the following represents the most appropriate application of the input-processing-output framework?

A. Input: Motors, Processing: Light sensors, Output: Program code

B. Input: Light sensors, Processing: Decision algorithm, Output: Motor activation

C. Input: Battery, Processing: Motors, Output: Movement

D. Input: Program code, Processing: Battery, Output: Sensors
---answer---
The correct answer is B. Input: Light sensors, Processing: Decision algorithm, Output: Motor activation. In a line-following robot, light sensors detect the line (input), a decision algorithm processes this information to determine position relative to the line (processing), and motors are activated to adjust the robot's direction accordingly (output). This properly represents the flow of information through the robot system. If you chose a different answer, review the input-processing-output framework to ensure you understand how information flows through a robot system.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- Effective robot designs directly address the identified problem with appropriate components selected for specific purposes
- The input-processing-output framework provides a structured approach to selecting and integrating robot components
- Ethical considerations like safety, privacy, and accessibility should be incorporated throughout the design process

[End of Lesson]

## Instructional designer notes of lesson 7.3

**This lesson fits into the the overall module of 7 in the following ways:**
- This lesson builds on the problem definition and research from Lesson 2, focusing on translating those insights into concrete design plans
- It prepares students for implementation and testing in Lesson 4 by ensuring they have comprehensive design specifications
- It reinforces the systematic approach to robotics design established throughout the module

**This lesson could be followed by this game:**
Component Matchmaker - An interactive design challenge where students are given specific robotics problems and must select the most appropriate inputs, processing methods, and outputs from a collection of options. Example: Designing a robot that can sort recycling materials by type requires matching appropriate sensors (color/material sensors), decision algorithms (material classification), and sorting mechanisms (servo-controlled gates).

Additional Writer Notes:
I addressed the following SME feedback points:
1. Added a real-world example of the input-processing-output framework applied to a weather station robot for school gardens
2. Added content on balancing structured processes with creative exploration in the algorithm development section
3. Added simple documentation templates (design table and decision tree diagram suggestions)
4. Added a note about how constraints can spark creativity using the Mars rover example
5. Simplified language throughout to be appropriate for 11-14 year old students