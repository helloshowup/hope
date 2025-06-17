# 8.1
# Introduction to Programming Concepts

## Learning Objectives
By the end of this session, you'll be able to:
- Define what programming is within the input-processing-output framework
- Explain how programming connects to robotics
- Identify key programming terminology and concepts

## Lesson Podcast Discussion: The Bridge Between Human Instructions and Robot Actions
This podcast explores how programming serves as the translator that converts our human intentions into precise actions that robots can understand and execute.

## What is Programming?
**Programming** is the process of giving precise instructions to a computer or robot to perform specific tasks. Unlike humans who can interpret vague directions, computers and robots need extremely clear, step-by-step instructions to function properly.

Think of programming as writing a very detailed recipe. If you tell a person to "bake cookies," they can fill in many details on their own. But a robot would need explicit instructions about ingredients, measurements, mixing procedures, oven temperature, and cooking time.

### The Language of Machines
**Programming languages** are specially designed systems of communication that allow humans to "speak" to machines. These languages range from complex text-based languages (like Python or Java) to visual block-based systems that are easier for beginners to understand.

Just as humans use words to build sentences and express ideas, programmers use programming elements to build instructions that computers and robots can follow.

## Programming in the Input-Processing-Output Framework
One of the clearest ways to understand programming is through the **Input-Processing-Output (IPO)** framework:

### Input
**Inputs** are the information that flows into the system. For robots, inputs often come from:
- Sensors (light, touch, sound, distance)
- User commands (buttons, voice, app controls)
- Stored data (maps, images, pre-programmed rules)

### Processing
**Processing** is where programming truly shines - it's the "thinking" part of the system that determines what to do with the inputs:
- Decision making (if-then statements)
- Calculations and comparisons
- Following algorithms (step-by-step procedures)
- Triggering actions based on conditions

### Output
**Outputs** are the visible results of the processing:
- Physical movements (motors, wheels, arms)
- Sounds or lights
- Screen displays
- Data recording

### Real-World Example: Smart Home Thermostat
Let's look at how the IPO framework works in a smart home thermostat:
- **Inputs**: Temperature sensors detect it's 75°F in the room; the user has set the desired temperature to 70°F
- **Processing**: The program compares current temperature to desired temperature and decides cooling is needed
- **Outputs**: The thermostat turns on the air conditioning system

This same framework applies to assistive robots that help people. For example, a medicine reminder robot:
- **Inputs**: Internal clock shows it's medication time; sensors detect a person is nearby
- **Processing**: The program determines which medication is needed and that the person should be alerted
- **Outputs**: The robot moves toward the person, plays a gentle sound, and displays which medication to take

---pagebreak---

## Activity 1: Creating Everyday Algorithms

In this activity, pick a simple daily task like making a sandwich or brushing your teeth. Write down every single step needed to complete this task as if you were instructing someone who has never done it before. Be as precise and detailed as possible, leaving nothing to interpretation.

For example, instead of "spread peanut butter," you might write:
1. Open the peanut butter jar by twisting the lid counterclockwise
2. Take a knife from the drawer
3. Insert knife into the jar
4. Lift out approximately 1 tablespoon of peanut butter on the knife
5. Place the knife on the bread
6. Move the knife in a back-and-forth motion to spread peanut butter evenly across the entire surface

After completing your instructions, try to identify any steps that might still be unclear or open to interpretation.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about a time when you gave someone directions and they misunderstood what you meant. How does this experience relate to the precision needed in programming instructions for robots?
---stopandreflectEND---

## Key Programming Concepts
To become effective at programming robots, you'll need to understand several fundamental concepts:

### Variables
**Variables** are containers that store information your program needs to remember. Think of them like labeled boxes where you can place values:
- A variable might store a robot's current speed (5 cm/second)
- Another variable might track a sensor reading (25 cm distance)
- Variables can change during program execution (hence the name "variable")

### Algorithms
**Algorithms** are step-by-step procedures for solving problems or accomplishing tasks. They're like detailed recipes that specify exactly what needs to happen and in what order:
- They break complex problems into manageable steps
- They can be reused for similar problems
- Well-designed algorithms are efficient and reliable

### Control Structures
**Control structures** determine the flow of program execution:
- Sequential execution (do A, then B, then C)
- Conditional execution (IF temperature > 30 THEN turn on fan)
- Loops (REPEAT moving forward UNTIL obstacle detected)
- Functions (reusable blocks of code that perform specific tasks)

### Logical Operators
**Logical operators** help make decisions:
- AND: Both conditions must be true
- OR: At least one condition must be true
- NOT: Inverts a condition (true becomes false)

---pagebreak---

## Introduction to Block-Based Programming
**Block-based programming** provides a visual approach to coding that's perfect for beginners:

### What Are Programming Blocks?
Programming blocks are visual elements that represent programming commands. Instead of typing code, you drag and connect these blocks like puzzle pieces to create programs.

### Benefits for Beginners
- Eliminates syntax errors (no typos or missing punctuation)
- Visually represents program structure
- Provides immediate visual feedback
- Focuses on logic rather than language rules

### Common Block Types
- Event blocks: Start programs when something happens (button press, program start)
- Motion blocks: Control movement (forward, backward, turn)
- Control blocks: Manage program flow (if-then, loops, wait)
- Sensor blocks: Read information from the environment
- Operator blocks: Perform calculations and comparisons

### Examples in Robotics
Block-based programming is widely used in educational robotics:
- LEGO MINDSTORMS
- Scratch-based robot programming
- VEX Robotics platforms
- Many Arduino-based educational robots

## From Requirements to Code: How Assistive Robots Are Programmed

When creating robots that help people, programmers start with human needs and translate them into specific programming elements:

1. **Identify the need**: "A person with limited mobility needs help picking up objects from the floor"

2. **Define requirements**: 
   - The robot must detect objects on the floor
   - It must be able to grasp different sized objects
   - It must safely deliver objects to the person
   - It must respond to voice commands

3. **Translate to programming elements**:
   - **Variables**: objectDetected, objectSize, robotPosition, batteryLevel
   - **Algorithms**: objectDetection, pathPlanning, graspingSequence
   - **Control structures**: IF objectDetected THEN initiate pickup sequence
   - **Sensor integration**: Camera input to identify objects, touch sensors for safe grasping

This translation process is how programmers turn real human needs into working robot behaviors.

---pagebreak---

## Case Study: Programming a Medicine Reminder Robot

Let's look at how programming enables a robot to help someone remember to take their medication:

**The Challenge**: Many people forget to take medications on time, which can affect their health.

**The Solution**: A small robot that:
- Keeps track of medication schedules
- Alerts the person when it's time for medication
- Can answer simple questions about the medication

**Programming Elements**:
- **Inputs**: Internal clock, voice recognition, medication database
- **Processing**: Comparing current time to scheduled times, identifying voice commands
- **Outputs**: Lights, sounds, spoken reminders, display screen information

**Sample Program Logic**:
```
WHEN current time equals medication time
    Turn on reminder light
    Play gentle alert sound
    IF person approaches robot
        Say "Time to take your [medication name]"
        Display medication information
    IF 5 minutes pass with no response
        Increase alert volume
        Send notification to caregiver's phone
```

This example shows how programming connects inputs (time, presence detection) to helpful outputs (reminders, information) through logical processing steps.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider a robot that needs to navigate a maze. What kinds of inputs would it need? How would the program process those inputs? What outputs would result from the processing?
---stopandreflectEND---

---checkyourunderstanding---
Which of the following best describes programming in the context of robotics?

A. Writing code in any language

B. Creating art with computers

C. Giving precise instructions that connect inputs to outputs

D. Making websites
---answer---
The correct answer is C. Giving precise instructions that connect inputs to outputs. Programming in robotics is about creating instructions that tell the robot how to process inputs and create appropriate outputs. If you chose A, while programming does involve writing code, the purpose in robotics specifically is to connect inputs to outputs. If you chose B or D, these are other applications of programming but don't specifically address the robotics context.
---answerEND---
---checkyourunderstandingEND---

## Key Takeaways
- **Programming** is giving precise instructions to computers or robots, requiring clarity and specificity that humans may not need in everyday communication
- In robotics, programming connects inputs (from sensors and users) to outputs (actions and responses) through logical processing steps
- **Block-based programming** provides a visual, beginner-friendly way to create instructions for robots without dealing with complex syntax

## Instructional designer notes of lesson
**This lesson fits into the the overall module of Robots Helping People in the following ways:**
- It establishes the fundamental programming concepts students need before they can design robots that assist humans
- It introduces the input-processing-output framework that will be essential for understanding how robots perceive and respond to human needs
- It prepares students for the more advanced programming concepts that will be covered in subsequent lessons of this module

**This lesson could be followed by this game:**
Sequencer game: Students would be presented with a series of block-based programming commands (like "Move Forward," "Check Sensor," "If-Then Statement," "Turn Right") that they must arrange in the correct order to accomplish a task such as "Help a robot navigate around an obstacle to deliver medicine to a patient." This tests their understanding of programming logic and the input-processing-output framework while reinforcing the module's theme of robots helping people.