# Admin
Module 6
Lesson 1
Lesson Title: Introduction to Programming Concepts
# Template
[start of lesson]
# 6.1
# Introduction to Programming Concepts
## Learning Objectives
By the end of this session, you'll be able to:
- Define what programming is within the input-processing-output framework
- Explain how programming connects to robotics
- Identify key programming terminology and concepts

## Lesson Podcast Discussion: Programming as Robot Communication
This podcast explores how programming creates a bridge between human intentions and robot actions through precise instructions and logic.

## What is Programming?
Programming is the process of creating a set of instructions that tell a computer or device how to perform specific tasks. Unlike human communication which can be ambiguous, programming requires extreme precision and clarity in the instructions we provide.

### The Language of Machines
Computers and robots don't understand natural languages like English. They operate using very specific instructions written in formats they can interpret. Programming languages serve as translators between human thinking and machine execution, allowing us to write instructions in a more human-readable format that then gets converted into binary code (1s and 0s) that machines understand.

## Programming in the Input-Processing-Output Framework
At its core, programming follows an input-processing-output (IPO) pattern, which is particularly relevant for robotics:

### Inputs
These are the data, signals, or information that enter the robot system:
- Sensor readings (light, distance, touch)
- User commands (button presses, voice commands)
- Environmental data (temperature, location)

### Processing
This is where the "thinking" happens - the program analyzes inputs according to programmed instructions:
- Making decisions based on sensor readings
- Calculating next actions
- Following algorithmic rules

### Outputs
These are the actions or results that occur after processing:
- Physical movements (motors activating)
- Sounds or visual displays
- Data storage or transmission

## Activity 1: Creating Simple Algorithmic Instructions
Choose an everyday task like making a sandwich or tying shoelaces. Write down the exact step-by-step instructions that a robot would need to follow to complete this task. Be extremely precise - remember that a robot will follow your instructions exactly as written!

After writing your instructions, identify the inputs (what information or materials are needed), processing (what decisions or calculations need to be made), and outputs (what actions result) in your algorithm. Was anything challenging about creating these precise instructions? This exercise demonstrates why programming requires breaking down tasks into clear, unambiguous steps.

## Key Programming Concepts
Understanding programming requires familiarity with several fundamental concepts that apply across almost all programming contexts.

### Variables
Variables are containers that store information in a program. They can hold numbers, text, or more complex data that your program needs to remember and use later. For a robot, variables might store sensor readings, current motor speeds, or task states.

### Conditionals
Conditional statements allow programs to make decisions based on whether certain conditions are true or false. The classic form is "if-then-else": If something is true, then do this action; otherwise, do something different. Conditionals let robots respond differently to different situations.

### Loops
Loops allow a program to repeat actions multiple times without writing the same code repeatedly. For example, a robot might need to check a sensor repeatedly while moving, or perform the same action until a certain condition is met.

### Functions
Functions are reusable blocks of code designed to perform specific tasks. They help organize code and reduce repetition. For robots, you might create functions for common behaviors like "turn left" or "check obstacle" that can be used throughout a program.

## Stop and Reflect

**CHECKPOINT:** Consider how programming relates to giving instructions in daily life. Think about a time when someone misunderstood your instructions. How might you have made your instructions more precise, like a programmer would for a robot?

## Introduction to Block-Based Programming
Block-based programming offers a visual approach to creating programs, particularly helpful for beginners learning programming concepts.

### Visual Programming Blocks
Instead of typing code as text, block-based programming environments let you drag and drop visual blocks that represent programming constructs. The blocks connect like puzzle pieces, with shapes that only fit together when the programming logic is valid.

### Benefits for Robotics Learning
Block-based programming is particularly valuable for learning robotics programming:
- Visual representation makes abstract concepts more concrete
- Prevents syntax errors by design (blocks won't connect if the logic is invalid)
- Allows focus on algorithmic thinking rather than code syntax
- Provides immediate visual feedback
- Creates a smoother transition to text-based programming later

### Popular Block Environments
Several platforms use block-based programming for robotics:
- Scratch: Widely used for educational robotics
- Blockly: Powers many robot programming interfaces
- MakeCode: Used with various educational robots
- LEGO Mindstorms: Uses block programming for LEGO robots

### Check your understanding
Which of the following best describes programming in the context of robotics?
A. Writing code in any language
B. Creating art with computers
C. Giving precise instructions that connect inputs to outputs
D. Making websites

Choose your answer and check it below.

The correct answer is C. Giving precise instructions that connect inputs to outputs. Programming in robotics is about creating instructions that tell the robot how to process inputs and create appropriate outputs. If you chose a different answer, remember that while programming can involve writing code in various languages (A), it has specific meaning in robotics as the connection between inputs (sensors) and outputs (actions).

## Key Takeaways
- Programming is giving precise instructions to computers, requiring clarity and detail beyond everyday human communication
- In robotics, programming connects inputs to outputs through a processing framework that determines how a robot responds to its environment
- Block-based programming provides a visual way to create instructions, making programming concepts more accessible to beginners
[End of Lesson]

## Instructional designer notes of lesson 6.1
**This lesson fits into the the overall module of Smarter Robot Instructions (Advanced Programming) in the following ways:**
- It establishes fundamental programming concepts that will be built upon in later lessons
- It introduces the input-processing-output framework that is central to robotics programming
- It prepares students for the block-based programming environment they'll use throughout the module

**This lesson could be followed by this game:**
Sequencing game where students arrange programming blocks in correct order to complete simple tasks. For example, students could be given a set of blocks like "move forward," "turn right," "sense obstacle," and "repeat" which they must arrange in the correct sequence to navigate a virtual robot through a simple maze, reinforcing the concepts of algorithms and sequential instructions.