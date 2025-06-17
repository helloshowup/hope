# Admin
Module 2
Lesson 3
Lesson Title: Robot Processing Systems
# Template
[start of lesson]
# 2.3
# **Robot Processing Systems**
## Learning Objectives
By the end of this session, you'll be able to:
- Describe the function of controllers and computers in robots
- Explain how robots use programs to process information
- Create a simple decision tree showing robot information processing

### Lesson Podcast Discussion: Processing Information in Robotic Systems
This podcast explores how robots process information from inputs to make decisions, comparing different processing architectures and their capabilities.

## **The Robot Brain**

Just like humans have brains to think and make decisions, robots have processing systems that act as their "brains." These electronic brains allow robots to take in information from sensors, figure out what that information means, and decide what actions to take.

Unlike our human brains, robot brains are made of electronic components like circuit boards, chips, and wires. These components work together to run programs that tell the robot what to do in different situations. Without this processing system, a robot would just be a collection of parts with no ability to function on its own.

The processing system is what makes a robot "smart" - though different robots have different levels of intelligence depending on how powerful their processing systems are and what kind of programming they use.

### **Microcontrollers vs. Computers**

Robots can use different types of electronic "brains," and the two main categories are microcontrollers and full computers.

**Microcontrollers** are small, simple, and use less power. Think of them like a basic calculator - they're good at specific tasks but can't do many things at once. Microcontrollers are perfect for robots that do simple, repetitive jobs like following a line or responding to basic commands. They're cheaper and use less battery power, which is why you'll find them in toys and simple household robots like robot vacuum cleaners.

**Full computers**, on the other hand, are more like the laptop or tablet you might use at school. They're more powerful and can handle complex tasks, run advanced software, and process lots of information at once. Robots that need to navigate complicated environments, recognize objects, or interact with people often use full computers. The trade-off is that computers need more power, cost more money, and generate more heat than microcontrollers.

Choosing between a microcontroller and a computer depends on what the robot needs to do. A simple robot arm in a factory might only need a microcontroller, while a self-driving car would definitely need a powerful computer system.

### **Processing Components and Architecture**

Inside a robot's processing system, several important components work together to handle information:

The **Central Processing Unit (CPU)** is like the robot's main thinking center. It carries out instructions from the robot's program, performs calculations, and makes decisions based on the robot's programming. Some advanced robots have multiple CPUs working together to handle more complex tasks.

**Graphics Processing Units (GPUs)** help robots process visual information quickly. Originally designed for video games, these specialized chips are now used in robots that need to understand what they're seeing through cameras or other visual sensors.

The robot's **architecture** refers to how all these components are connected and organized. Some robots use a centralized architecture, where one main processor handles everything. Others use a distributed architecture, with multiple smaller processors handling different tasks and communicating with each other. For example, a robot might have one processor for movement, another for vision, and a third for decision-making.

The way these components are arranged affects how quickly the robot can respond to its environment and how many tasks it can handle at once.

### **Memory and Storage in Robots**

Just like you need to remember things for school, robots need memory to function properly. Robots use two main types of memory: temporary working memory (RAM) and long-term storage memory.

**RAM (Random Access Memory)** is like a robot's short-term memory. It holds information the robot is currently using, such as sensor readings, calculations, and immediate tasks. When the robot is turned off, everything in RAM is erased. The more RAM a robot has, the more information it can work with at once.

**Storage memory** is like a robot's long-term memory. This is where the robot's programs, learned behaviors, and saved data are kept even when the power is turned off. Storage can be on hard drives, solid-state drives (SSDs), or memory cards. A robot with more storage can keep more programs and remember more information from past experiences.

Memory affects how well a robot performs. With limited memory, a robot might move slowly because it can only process a little information at a time. With more memory, robots can handle complex tasks like recognizing faces or navigating through changing environments. Advanced robots that learn from experience need plenty of both types of memory to store what they've learned and use that knowledge to make better decisions.


## **Activity 1: Processing Power Comparison**

Compare three different types of controllers (basic microcontroller, mid-range processor, advanced computer) and identify which would be most appropriate for specific robot applications. For each controller, consider processing speed, memory capacity, and power requirements, then match it to either a factory line robot, household robot vacuum, or autonomous research vehicle.
---pagebreak---

## **How Robots Process Information**

Robots process information in a step-by-step way that's similar to how we follow a recipe when cooking. Let's explore how robots take raw data and turn it into meaningful actions.

### **From Inputs to Decisions**

When a robot receives information from its sensors, it doesn't automatically understand what that information means. The processing system has to convert raw sensor data into something useful through several steps:

First, the robot receives raw signals from its sensors - maybe a number representing distance from an ultrasonic sensor, or an image from a camera. These signals are often just electrical values that don't mean much on their own.

Next, the processing system filters this information to remove errors or "noise." For example, if a distance sensor is giving slightly different readings each time, the processor might average several readings to get a more accurate measurement.

Then, the robot interprets what the filtered data means. If a distance sensor reports "10 cm," the processor recognizes this means "there's an object 10 centimeters away." If a camera sees a red circle, the processor might identify this as "a red ball" or "a stop sign" depending on its programming.

Finally, the robot compares this interpreted information against its programmed rules to decide what to do. If the robot detects an object 10 cm away and its rule says "stop if any object is closer than 15 cm," then the robot will decide to stop.

This entire process happens very quickly - sometimes hundreds or thousands of times per second - allowing robots to continuously respond to their environment.

Let's look at a real example: a remote-controlled toy car versus an autonomous toy robot. The remote-controlled car doesn't process information on its own - it just receives signals from the remote and follows those commands. But an autonomous toy robot, like a simple line-following robot, processes information from its light sensors to detect the line, interprets that data to determine if it's on or off the line, and then decides whether to turn left, right, or continue straight ahead. All this happens continuously as the robot moves along the line.

### **Programming and Algorithms**

Programming is like giving a robot its instruction manual. It provides the rules and steps the robot follows to process information and make decisions.

Programs for robots are written in special computer languages like Python, C++, or block-based languages designed for beginners. These programs contain **algorithms** - step-by-step procedures for solving problems or completing tasks. Think of algorithms as detailed recipes that tell the robot exactly what to do in different situations.

For example, a simple algorithm for a line-following robot might look like:
1. Check the line sensor
2. If the sensor detects the line is to the left, turn slightly right
3. If the sensor detects the line is to the right, turn slightly left
4. If the sensor detects the line is centered, go straight
5. Repeat steps 1-4 continuously

More complex algorithms might include multiple sensors and more sophisticated decision-making. The quality of a robot's programming directly affects how well it performs its tasks. Even the most advanced robot hardware won't work properly without good programming.

Programmers need to anticipate different situations the robot might encounter and provide instructions for handling each one. This is why robot programming can be challenging but also creative and rewarding.

### **Simple vs. Complex Processing**

Robots can process information in different ways, ranging from very simple to incredibly complex:

**Simple processing** uses basic if-then rules. For example, "If the temperature sensor reads above 30°C, then turn on the cooling fan." These robots follow fixed instructions and can't adapt to situations they weren't specifically programmed for. Most toy robots and many industrial robots use this type of processing.

More advanced processing might use **fuzzy logic**, which allows for "partially true" conditions rather than just yes/no decisions. This helps robots handle uncertainty better. For example, instead of just "hot" or "cold," a robot might recognize "slightly warm" and respond accordingly.

The most complex processing uses **machine learning**, where robots can improve their performance based on experience. These robots aren't just following pre-written rules - they're actually learning patterns from data. For instance, a robot vacuum might learn the layout of your home over time and create a more efficient cleaning path.

The difference between simple and complex processing is like the difference between following a map with one specific route versus learning to navigate by understanding roads, traffic patterns, and shortcuts. Simple processing is reliable for specific tasks in controlled environments, while complex processing allows robots to handle unpredictable situations and improve over time.

**Artificial intelligence (AI)** and machine learning represent the cutting edge of robot processing. Modern robots like Boston Dynamics' Spot robot dog use AI to navigate rough terrain, climb stairs, and avoid obstacles in ways that would be impossible to program with simple if-then rules. These advanced robots can recognize objects, understand speech, and even learn new tasks without being explicitly programmed for each situation. While industrial robots in factories might use simpler processing to perform the same task repeatedly with high precision, robots designed to work alongside humans in changing environments need these more advanced AI capabilities to be useful and safe.


---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about how your brain processes information compared to a robot. What are the similarities and differences in how you make decisions versus how a robot would be programmed to decide?
---stopandreflectEND---

---pagebreak---

## **Decision-Making in Robots**

Once a robot has processed information from its sensors, it needs to decide what actions to take. This decision-making process is a crucial part of what makes robots autonomous and useful in various situations.

### **Logic Patterns and Decision Trees**

Robots use structured logic patterns to make decisions. One of the most common patterns is the **decision tree** - a flowchart-like structure that maps out different possible choices based on specific conditions.

In a decision tree, the robot starts at the top and follows branches down based on whether certain conditions are true or false. For example, a robot might start by checking if there's an obstacle ahead. If yes, it follows one branch (maybe checking if there's space to the left). If no, it follows a different branch (maybe continuing forward).

Other common logic patterns include:
- **If-Then-Else statements**: "If condition is true, do action A; otherwise, do action B"
- **Case statements**: "Depending on which of these specific values I detect, do the corresponding action"
- **While loops**: "Keep doing this action as long as this condition remains true"

These logic patterns can be combined to create complex behaviors. For instance, a robot might use a decision tree to decide which room to clean next, while using if-then statements to avoid bumping into furniture within each room.

Decision trees are especially useful for visualizing and planning robot behaviors because they show clearly how different conditions lead to different actions.

### **Real-Time Processing Challenges**

Robots often need to make decisions quickly in changing environments, which creates several challenges:

**Speed** is critical - a self-driving car needs to detect and respond to a child running into the street in a fraction of a second. This requires powerful processors that can analyze sensor data and make decisions almost instantly.

Robots must handle unexpected situations. The real world is messy and unpredictable, so robots need to process information and make reasonable decisions even when they encounter something they weren't specifically programmed for.

Multiple sensors create large amounts of data that must be processed simultaneously. For example, a robot might need to combine information from cameras, distance sensors, and touch sensors all at once to navigate safely.

Limited processing power means robots sometimes have to prioritize which information is most important. A robot might focus first on detecting obstacles that could cause damage, and only then consider less critical factors like optimizing its path.

Engineers address these challenges by using faster processors, more efficient algorithms, and sometimes by dividing processing tasks among multiple specialized systems that work together.

### **Intelligence Levels in Robot Processing**

Robots can be categorized by their level of intelligence, which directly relates to how they process information:

**Reactive robots** are the simplest. They respond directly to sensor inputs without any memory or planning. They follow fixed rules like "if touch sensor is pressed, back up and turn." Most simple toy robots and basic industrial robots are reactive.

**Deliberative robots** can plan ahead and consider the consequences of their actions. They maintain an internal model of their environment and can think several steps ahead. A chess-playing robot is deliberative because it considers many possible moves and their outcomes before deciding.

**Learning robots** can improve their performance over time based on experience. They might start with basic programming but then adapt their behavior based on what works well and what doesn't. A robot vacuum that creates better cleaning paths after mapping your home is showing simple learning behavior.

**Autonomous robots** combine all these capabilities and can operate independently for extended periods with minimal human supervision. Self-driving cars and advanced research robots fall into this category.

The most sophisticated robots today use artificial intelligence techniques like neural networks to process information in ways that mimic aspects of human thinking. These systems can recognize patterns, adapt to new situations, and even demonstrate creativity in problem-solving.

For example, a light sensor in a robot vacuum might detect that it's getting dark, but the robot needs to interpret what that means. Is it entering a shadowy area under furniture, or is it nighttime? A simple reactive robot might just turn on its lights. A more intelligent robot with multiple sensors might check its internal clock, compare readings from other light sensors, and then decide whether it's under furniture (continue cleaning with lights on) or if it's nighttime (return to charging station to avoid disturbing sleeping humans).


## **Activity 2: Decision Tree Design**

Create a simple flowchart showing how a robot would make decisions when navigating a maze. Your decision tree should include at least three decision points where the robot must choose between multiple actions based on sensor inputs. Include conditions like "if path blocked on left" and resulting actions like "turn right." Draw this on paper or use an online flowchart tool.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider how a robot's processing needs might change depending on whether it works in a controlled factory environment versus an unpredictable outdoor setting. What additional processing capabilities would be necessary for the outdoor robot?
---stopandreflectEND---

---checkyourunderstanding---
Which statement best describes the relationship between a robot's programming and its decision-making process?

A. Programming is only needed for advanced robots with artificial intelligence

B. Programming provides the rules and logic for how a robot processes information and makes decisions

C. Programming only affects the output devices and has no impact on decision-making

D. Programming automatically adjusts based on the robot's experiences without human intervention
---answer---
The correct answer is B. Programming provides the rules and logic for how a robot processes information and makes decisions. Programming provides the fundamental rules, logic, and instructions that guide how a robot processes information from its input devices and determines appropriate responses. Without programming, a robot cannot interpret sensor data or decide on actions. If you chose a different answer, remember that all robots require programming for decision-making, not just advanced ones, and programming doesn't automatically self-adjust without human intervention.
---answerEND---
---checkyourunderstandingEND---

## Key Takeaways
- The processing system serves as the robot's 'brain,' interpreting input data and determining appropriate outputs
- Robot processing can range from simple if-then logic to complex artificial intelligence algorithms
- The sophistication of a robot's processing system directly impacts its capabilities, adaptability, and autonomy
[End of Lesson]

## Instructional designer notes of lesson 2.3
**This lesson fits into the the overall module of 2 in the following ways:**
- This lesson covers the central 'processing' component of the input-processing-output model, building on the input systems from Lesson 2
- It prepares students to understand how processing leads to outputs in Lesson 4
- It helps students see how information flows through a complete robot system

**This lesson could be followed by this game:**
Sequencer game: Robot Logic Simulator - Students arrange programming blocks in the correct order to create a functional decision tree for a robot. For example, they must sequence blocks like "Check sensor," "If obstacle detected," "Turn right," "If no obstacle," "Move forward" to successfully navigate a virtual robot through different scenarios.