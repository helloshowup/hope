# 2.1
# **Understanding Robot Systems**

## **Learning Objectives**

By the end of this session, you'll be able to:
- Define what constitutes a 'system' in robotics context
- Explain the input-processing-output model with practical examples
- Compare robot systems to human systems and everyday technology

### **Lesson Podcast Discussion: Understanding the Input-Processing-Output Model in Robotics**

This podcast should discuss how the input-processing-output model serves as a fundamental framework for understanding robot systems and their interactions with the environment.

## **What is a System?**

A system is a collection of parts that work together to achieve a specific purpose or goal. Think about your bicycle - it has wheels, pedals, a chain, and handlebars that all work together to help you move from one place to another. Without any one of these parts, the bicycle wouldn't work properly!

In robotics, systems are especially important. A robot isn't just one thing - it's many different components working together. Just like how your body has different systems (like your digestive system or nervous system) that help you function, robots have systems that allow them to sense their environment, make decisions, and take actions.

Systems have boundaries that separate them from their environment, but they also interact with the world around them. For example, a robot vacuum cleaner is its own system, but it interacts with your home environment by detecting dirt and obstacles.

### **Systems in Our World**

Systems are everywhere around us! Your school is a system with teachers, students, classrooms, and schedules all working together to help you learn. Your favorite video game console is a system with hardware, software, controllers, and a screen that work together to create fun experiences.

Even natural things like ant colonies are systems. Each ant has a specific job, and they all work together to find food, protect the queen, and build their home. Weather is another system where air temperature, moisture, and pressure interact to create sunshine, rain, or snow.

Understanding systems helps us make sense of complex things by breaking them down into parts and seeing how those parts work together.

### **Parts Working Together**

For a system to function properly, all its parts must work together in a coordinated way. Imagine an orchestra - each musician plays their own instrument, but they must all follow the conductor and play in harmony to create beautiful music.

In a robot, motors, sensors, batteries, and computer chips must all work together. The sensors collect information about the environment, the computer chip processes this information and makes decisions, and the motors move the robot based on those decisions. The battery provides power to all these components.

When parts work well together, the system can do things that no individual part could do alone. This is called "emergence" - when the whole system has abilities that emerge from the combination of its parts working together.

### **System Boundaries and Interactions**

Every system has boundaries that define what's part of the system and what isn't. For a robot, the boundary might be its outer shell or casing. Things inside this boundary (like motors and circuits) are part of the robot system, while things outside (like the floor it moves on) are part of its environment.

Systems interact with their environment through inputs and outputs. Inputs are things that come into the system from outside, like when a robot's camera sees an obstacle or its microphone hears a command. Outputs are things the system sends out to its environment, like when a robot moves its wheels or plays a sound.

These interactions are crucial for robots to be useful. A robot that couldn't take in information from its environment or affect its environment in some way wouldn't be very helpful!

## **Activity 1: System Mapping**

Map a system you use daily (like a smartphone or bicycle) by identifying its inputs, processing mechanisms, and outputs on the provided diagram. Consider what information the system takes in, how it processes that information, and what actions or results it produces.

---pagebreak---

## **The Input-Processing-Output Model**

The input-processing-output model is like a recipe for how systems work. Just as a recipe has ingredients (inputs), cooking steps (processing), and a finished dish (output), systems follow this same pattern. This model helps us understand how robots and other systems function in a step-by-step way.

This model is especially useful for understanding robots because it breaks down their complex behavior into three simpler parts that we can study one at a time. Let's explore each part of this model in detail.

### **Input: Gathering Information**

Inputs are all the ways a robot gathers information from its environment. Think of inputs as the robot's senses - similar to how we use our eyes, ears, and sense of touch to understand what's happening around us.

Robots use special devices called sensors to collect this information. Some common robot sensors include:

- Cameras that act like eyes, allowing robots to "see" objects, colors, and movement
- Microphones that work like ears, letting robots "hear" sounds and voice commands
- Touch sensors that detect when the robot bumps into something, like our sense of touch
- Distance sensors that use sound waves or light to measure how far away objects are
- Light sensors that can tell how bright or dark it is
- Temperature sensors that measure how hot or cold things are

For example, a robot vacuum cleaner uses sensors to detect walls, furniture, and stairs so it doesn't bump into things or fall down steps. A weather robot might use temperature sensors, humidity sensors, and barometers to collect data about current weather conditions.

Without inputs, a robot would be like a person with no senses - unable to respond to its environment or make informed decisions.

### **Processing: Making Decisions**

Processing is what happens after a robot collects information through its inputs. This is like the robot's "brain" thinking about what to do with the information it has gathered.

Inside most robots is a small computer called a microcontroller or processor. This computer runs programs (sets of instructions) that tell the robot how to interpret the information from its sensors and decide what actions to take. Here's what happens during processing:

1. The robot receives data from its sensors (inputs)
2. The processor analyzes this data using its programming
3. The processor makes decisions based on this analysis
4. The processor sends commands to the robot's output devices

For example, when a robot vacuum's sensors detect a wall, its processor calculates that it needs to change direction. A more complex robot might use artificial intelligence to learn from past experiences and make better decisions over time.

The quality of a robot's processing determines how "smart" it seems. A robot with simple processing might just follow basic if-then rules (if sensor detects wall, then turn), while advanced robots can handle complex situations and adapt to new environments.

### **Output: Taking Action**

Outputs are all the ways a robot affects or changes its environment. After the robot has gathered information through its inputs and decided what to do through processing, it uses its output devices to take action.

Common robot output devices include:

- Motors that make wheels turn or arms move
- Speakers that produce sounds or speech
- Lights that can turn on, off, or change colors
- Displays that show text or images
- Grippers or tools that can manipulate objects

For example, after a robot vacuum's processor decides to change direction when it detects a wall, it sends signals to its wheel motors (outputs) to turn and move in a new direction. A robot designed to help people might speak through a speaker to provide information or flash lights to get attention.

Outputs are what make robots useful - without them, a robot could sense its environment and think about what to do, but it couldn't actually do anything to accomplish tasks or communicate with us.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about your morning routine. How does it represent a system with inputs, processing, and outputs? Consider what information you take in, how you process it, and what actions result.
---stopandreflectEND---

---pagebreak---

## **Comparing Systems**

By comparing different types of systems, we can better understand how robot systems work and discover interesting similarities and differences. These comparisons help us see that the principles we're learning about robots apply to many other things in our world.

### **Human Body as a System**

The human body is an amazing system that has many similarities to robot systems. Just like robots, our bodies follow the input-processing-output model:

**Inputs:** Our body gathers information through our senses:
- Eyes detect light and colors (similar to robot cameras)
- Ears detect sounds (like robot microphones)
- Skin feels touch, temperature, and pain (like robot touch and temperature sensors)
- Nose detects smells and tongue detects tastes (some advanced robots have chemical sensors)

**Processing:** Our brain processes all this sensory information:
- It interprets what we see, hear, and feel
- It makes decisions based on this information and our past experiences
- It sends signals to different parts of our body
- It can learn and adapt over time (like robots with artificial intelligence)

**Outputs:** Our body responds through various actions:
- Muscles move our limbs (like robot motors)
- Vocal cords produce speech (like robot speakers)
- Hands can manipulate objects (like robot grippers)
- We can communicate through facial expressions and body language

The human body even has specialized subsystems, just like complex robots:
- The digestive system processes food for energy (like a robot's power system)
- The circulatory system transports nutrients and oxygen (like a robot's wiring)
- The nervous system carries signals (like a robot's communication network)

Understanding these parallels helps robot designers create machines that can function effectively in human environments.

#### **Brain vs. Robot Processing**

While both human brains and robot processors make decisions, they work in very different ways:

- Our brains use billions of connected neurons that work together, while most robot processors follow step-by-step instructions
- Human brains can learn naturally from experience, while robots need specific programming to learn
- Our brains can handle many tasks at once without getting confused, but simpler robots often focus on one task at a time
- Human brains use emotions and instincts to help make decisions, while robots typically rely on logical rules

Recent advances in artificial intelligence are helping robots process information more like humans. For example, some newer robots can:
- Recognize faces and voices they've seen before
- Learn from their mistakes without being reprogrammed
- Adapt to new situations they weren't specifically programmed for
- Work together with other robots to solve problems

These advances are exciting, but even the smartest robots today still process information very differently than humans do!

### **Everyday Technology Systems**

Many technologies we use every day are systems that follow the same input-processing-output model as robots:

**Smartphones:**
- Inputs: Touchscreen, microphone, camera, various sensors
- Processing: Computer chip running the operating system and apps
- Outputs: Screen display, speaker, vibration motor

**Video Game Consoles:**
- Inputs: Controllers, cameras, microphones
- Processing: Computer that runs the game software
- Outputs: TV screen, speakers, controller vibration

**Smart Home Devices:**
- Inputs: Microphones, motion sensors, temperature sensors
- Processing: Computer chips that interpret commands and sensor data
- Outputs: Speakers, lights, control signals to other devices

**Cars:**
- Inputs: Steering wheel, pedals, various sensors
- Processing: Engine control unit and other computers
- Outputs: Engine power, braking, dashboard displays

By recognizing these systems in everyday life, we can see that the principles of robotics are all around us, not just in devices we call "robots."

---pagebreak---

### **Robot Systems Overview**

Robot systems combine all the concepts we've discussed into machines that can sense, think, and act in their environment. What makes robots special compared to other technology systems is their ability to perform physical actions in the world based on the information they gather.

Robot systems typically include:

1. **A physical body or structure** that houses all components and allows the robot to exist in the physical world

2. **Input systems** with various sensors that gather information:
   - Vision systems (cameras)
   - Audio systems (microphones)
   - Touch and collision detection
   - Distance measurement
   - Environmental sensors (temperature, humidity, etc.)

3. **Processing systems** that make decisions:
   - Microcontrollers or computers
   - Software and algorithms
   - Memory for storing information
   - Communication systems for connecting with other devices

4. **Output systems** that take action:
   - Movement systems (motors, wheels, legs, arms)
   - Manipulation systems (grippers, tools)
   - Communication systems (screens, lights, speakers)

5. **Power systems** that provide energy:
   - Batteries
   - Solar panels
   - Power management circuits

Different types of robots emphasize different aspects of these systems. For example, industrial robot arms focus on precise movement outputs, while social robots emphasize communication inputs and outputs. Autonomous vehicles need sophisticated sensor inputs and processing to navigate safely.

Understanding robots as systems helps us design better robots and use them more effectively to solve problems and improve our lives.

### **Real-World Robot Examples**

Let's look at how the input-processing-output model works in different types of robots:

**Remote-Controlled Toy Car vs. Autonomous Toy Robot:**
- Remote-Controlled Car:
  - Inputs: Radio signals from the remote control
  - Processing: Simple circuits that convert signals to motor commands
  - Outputs: Motors that turn wheels, maybe lights or sounds
  
- Autonomous Toy Robot:
  - Inputs: Light sensors, bump sensors, maybe a simple camera
  - Processing: A small computer that makes decisions based on sensor data
  - Outputs: Motors for movement, speakers for sounds, lights for communication

The key difference is that the remote-controlled car relies on a human for all decisions, while the autonomous robot makes its own decisions based on what it senses.

**Service Robot (like a hotel delivery robot):**
- Inputs: Cameras to see hallways, sensors to detect obstacles, touchscreen for human input
- Processing: Maps of the hotel, programs to navigate hallways and avoid people
- Outputs: Wheel motors for movement, compartment that opens to deliver items, screen and speaker to communicate with guests

**Industrial Robot Arm:**
- Inputs: Precise position sensors, vision systems to identify parts, signals from the factory control system
- Processing: Complex calculations for movement paths, quality control checks
- Outputs: Powerful motors that move with extreme precision, grippers that handle parts, status lights

**Autonomous Vehicle:**
- Inputs: Many cameras, radar, lidar (laser sensors), GPS location
- Processing: Powerful computers running artificial intelligence to recognize roads, signs, pedestrians, and other vehicles
- Outputs: Control systems for steering, acceleration, and braking; displays and sounds to communicate with passengers

Each of these robots uses the same basic input-processing-output model, but with different types of components based on what job they need to do!

## **Activity 2: Human-Robot Comparison Chart**

Create a visual chart comparing human body systems (digestive, nervous, etc.) to equivalent robot systems. For each human system, identify what similar functions robots might need and what components would handle those functions.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider how inputs and outputs might differ between a robot vacuum cleaner and a robot used in space exploration. What unique challenges might each environment present to a robot's systems?
---stopandreflectEND---

---checkyourunderstanding---
Which of the following best represents the input-processing-output model in a robot?

A. The robot has a battery that powers all its systems

B. The robot is made of lightweight materials for easier movement

C. The robot can be programmed using a computer

D. The robot has a camera, analyzes what it sees, and moves accordingly
---answer---
The correct answer is D. The robot has a camera, analyzes what it sees, and moves accordingly. This option clearly shows all three components of the input-processing-output model: the camera serves as an input device gathering information, the robot analyzes this information (processing), and then takes action by moving (output). The other options describe important robot features but don't represent the complete input-processing-output cycle.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- Robots function as systems with interconnected parts working together toward specific goals
- The input-processing-output model provides a framework for understanding how robots interact with their environment
- Many systems we encounter daily, including our own bodies, follow similar principles to robot systems