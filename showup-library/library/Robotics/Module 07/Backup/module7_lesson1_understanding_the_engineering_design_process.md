# 7.1
# **Understanding the Engineering Design Process**

## **Learning Objectives**

By the end of this session, you'll be able to:
- Explain the five steps of the engineering design process and their purpose in robotics
- Distinguish between systematic design approaches and trial-and-error methods
- Connect the design process to the input-processing-output framework previously learned

## **Lesson Podcast Discussion: The Engineering Design Process in Modern Robotics**

This podcast will explore how the systematic engineering design process has led to breakthroughs in robotics and why structured approaches produce better results than trial-and-error methods.

## **Introduction to Engineering Design**

This section introduces the concept of engineering design as a structured approach to solving problems in robotics.

### **What is Engineering Design?**

Engineering design is a creative and organized way to solve problems and create solutions. Unlike random guessing or trying things without a plan, engineering design follows specific steps to find the best solution. Think of it like following a recipe when cooking instead of just throwing ingredients together and hoping for the best!

In robotics, engineering design helps us create robots that can successfully complete tasks, whether it's a robot that can navigate a maze, pick up objects, or even explore other planets. Engineers use this process to turn ideas into real, working robots that solve specific problems.

When we use engineering design, we're thinking like real engineers – carefully planning, testing, and improving our ideas until we have something that works well.

### **Why a Systematic Approach Matters**

Using a systematic approach to design is like using a map when traveling to a new place – it helps you reach your destination more efficiently and with fewer wrong turns. When building robots, a systematic approach helps in several important ways:

First, it saves time and resources. By planning before building, you avoid wasting materials on ideas that won't work. Second, it helps you consider multiple solutions instead of getting stuck on your first idea. Third, it makes troubleshooting easier because you can track what you've tried and what changes you've made.

For example, imagine trying to build a robot that can follow a line. Without a systematic approach, you might keep changing different parts randomly when it doesn't work. With a systematic approach, you'd carefully test each component (sensors, motors, programming) to identify exactly what needs improvement.

### **Engineering Design in Robotics**

In robotics, the engineering design process is especially important because robots are complex systems with many interacting parts. When designing robots, engineers must consider mechanical components (like wheels or arms), electronic systems (like sensors and motors), and programming (the instructions that tell the robot what to do).

For example, when engineers at NASA designed the Mars rovers, they had to solve problems like how to land safely on Mars, how to move across rough terrain, how to gather scientific data, and how to communicate that information back to Earth. Each of these challenges required careful application of the engineering design process.

Even simpler robots, like a basic line-following robot you might build in class, benefit from this process. You'll need to decide what sensors to use, how to mount them, how to program the robot to respond to sensor readings, and how to adjust the robot's speed for accurate line following. The engineering design process gives you a framework to tackle each of these decisions in a logical order.

---pagebreak---

## **Activity 1: Design Process Mapping**

Create a visual flow chart of the engineering design process with specific robotics examples for each step. Draw connections between each step, identifying key questions that should be asked at each phase and potential robotics applications that demonstrate that step in action.

## **The Five-Step Engineering Design Process**

This section explores each step of the engineering design process in detail.

### **Define the Problem**

The first step in the engineering design process is clearly defining the problem you're trying to solve. This means identifying exactly what your robot needs to accomplish and any constraints or limitations you need to work within.

A well-defined problem statement answers questions like: What specific task should the robot perform? What are the conditions under which it must operate? What resources (time, materials, budget) are available? What are the size, weight, or power limitations?

For example, instead of saying "I want to build a robot that helps people," a better problem definition would be "I want to build a robot that can detect and pick up small objects from the floor to assist elderly people who have difficulty bending down." This specific definition gives clear direction for the design process.

Writing down your problem definition helps keep your project focused and makes it easier to determine if your final solution actually solves the original problem. It's like creating a target to aim for before you start building.

### **Research and Ideate**

Once you've defined the problem, the next step is to gather information and generate ideas. This involves researching existing solutions, learning about relevant technologies, and brainstorming new approaches.

During research, you might:
- Look at how others have solved similar problems
- Learn about sensors, motors, or materials that could be useful
- Study the environment where your robot will operate
- Talk to potential users to understand their needs better

After gathering information, it's time to brainstorm ideas. This is where creativity comes in! Generate as many different solutions as possible without judging them yet. Sketch your ideas, discuss them with teammates, and consider unusual approaches. For a line-following robot, you might brainstorm different sensor arrangements, various wheel configurations, or alternative programming strategies.

Remember that this stage is about quantity of ideas, not quality yet. Even seemingly "wild" ideas might contain elements that could be useful or inspire better solutions.

### **Design Solutions**

In this step, you evaluate your ideas and develop detailed plans for the most promising solutions. This is where you move from general concepts to specific designs that can actually be built.

Start by comparing your brainstormed ideas against criteria like:
- How well does each solution address the original problem?
- Is it feasible with available technology and resources?
- What are the potential challenges or weaknesses?

Once you've selected the best approach, create detailed plans. For a robot, this typically includes:
- Mechanical designs (drawings or 3D models showing the physical structure)
- Electrical schematics (diagrams of circuits and connections)
- Programming flowcharts (outlines of the code logic)
- Parts lists (inventory of all components needed)

For example, if you're designing a robot to navigate around obstacles, your design plans would include details about sensor placement, motor specifications, chassis dimensions, and the logic for how the robot will detect and respond to obstacles.

### **Build and Test**

Now comes the exciting part – bringing your design to life! In this step, you construct a prototype based on your plans and then test it to see how well it works.

Building involves:
- Gathering all necessary materials and components
- Assembling the mechanical structure
- Connecting the electronic components
- Programming the robot's behavior
- Documenting the construction process

Once built, it's time to test your robot. Create specific tests that will show whether your robot meets the requirements defined in step one. For a maze-solving robot, you might test how accurately it detects walls, how smoothly it turns, and whether it can successfully navigate through different maze configurations.

During testing, carefully observe what works well and what doesn't. Take notes, measurements, and even videos to help you analyze the robot's performance. Remember that problems are not failures – they're valuable information that will help you improve your design!

### **Improve and Iterate**

The final step in the engineering design process is perhaps the most important: using what you learned from testing to improve your design. Very few designs work perfectly the first time, and iteration is a normal part of the engineering process.

Based on your test results, identify specific aspects of your robot that need improvement. Maybe the sensors aren't detecting obstacles reliably, or perhaps the robot moves too quickly to make accurate turns. For each problem, brainstorm potential solutions and decide which changes to implement.

Make one change at a time and test again to see if it helped. This methodical approach makes it easier to understand which changes are effective. Keep track of all modifications and their results – this documentation is valuable for future projects.

Iteration might involve small adjustments (like repositioning a sensor) or major redesigns (like changing the type of wheels). The process continues until your robot successfully meets all the requirements or until you've reached the limits of your available time and resources.

Remember that even professional engineers go through multiple iterations. The Mars rover Perseverance, for example, went through countless design improvements before its successful mission to Mars.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about a time you solved a problem by trial-and-error. How might using the engineering design process have changed your approach? Consider what specific steps might have made your solution more effective or efficient.
---stopandreflectEND---

---pagebreak---

## **Design Process vs. Trial-and-Error**

This section compares structured design approaches with less formal methods.

### **Limitations of Trial-and-Error**

While trial-and-error can sometimes lead to solutions, it has significant drawbacks when working on complex projects like robotics. First, it's often inefficient and time-consuming. Without a plan, you might make the same mistakes repeatedly or miss obvious solutions because you're changing things randomly.

Second, trial-and-error makes it difficult to track what you've tried and what worked. Imagine changing five different things on your robot at once – if performance improves, you won't know which change actually helped! This makes learning from the process nearly impossible.

Third, trial-and-error typically focuses on fixing immediate problems rather than understanding the underlying causes. For example, if your robot keeps veering left, a trial-and-error approach might involve adjusting the right wheel speed without investigating why the imbalance exists in the first place.

Finally, with limited resources (time, materials, budget), trial-and-error can be wasteful. Building multiple versions without planning might use up all your materials before you find a working solution.

### **Benefits of Systematic Design**

A systematic design approach offers numerous advantages over trial-and-error. First, it provides a clear roadmap that helps you stay organized and focused throughout the project. This structure is especially helpful when working on complex robots with many interacting systems.

Second, systematic design encourages thorough research and consideration of multiple solutions before building. This broader perspective often leads to more innovative and effective designs than simply trying the first idea that comes to mind.

Third, the testing phase in systematic design is deliberate and controlled. You create specific tests to evaluate how well your robot meets the requirements, which gives you reliable data about performance. This makes it easier to identify exactly what needs improvement.

Fourth, systematic design creates documentation throughout the process – problem definitions, research findings, design plans, test results, and improvement notes. This documentation is valuable for current troubleshooting and for future projects.

Finally, the systematic approach mirrors how professional engineers work in the real world. Learning this process now prepares you for more advanced projects and potential careers in engineering and robotics.

### **When Each Approach Is Appropriate**

While systematic design is generally superior for robotics projects, there are situations where elements of trial-and-error can be useful. Understanding when to use each approach is an important skill.

Systematic design works best for:
- Complex projects with multiple components
- Situations with limited resources or time
- Team projects where communication is essential
- Problems where safety or reliability is critical
- Projects that will be documented or shared with others

Elements of trial-and-error might be appropriate for:
- Quick explorations during the ideation phase
- Simple adjustments during fine-tuning (like calibrating a sensor)
- Learning about an unfamiliar component to see how it works
- Situations where the cost of failure is very low

In practice, many successful robotics projects use a hybrid approach – following the systematic design process overall while incorporating small, controlled experiments when appropriate. The key is being intentional about when you're exploring freely versus when you're following a structured plan.

### **Balancing Structure and Creativity**

While the engineering design process provides structure, it's important to remember that creativity is still a vital part of engineering! The best robot designs come from combining systematic approaches with creative thinking.

During the "Research and Ideate" phase especially, try these techniques to boost creativity while staying organized:

- Brainstorming sessions where you generate ideas without judging them first
- "What if" questions that challenge assumptions (What if the robot moved differently? What if we used a different sensor?)
- Looking at nature for inspiration (How do animals solve similar problems?)
- Combining different ideas to create new solutions

For example, when engineers designed the Mars rover Curiosity, they needed a creative solution for landing the large rover safely. They came up with the "sky crane" system - a completely new approach where the descent vehicle hovered above the surface and lowered the rover down on cables. This creative solution came from a structured design process that identified the specific problem (traditional landing methods wouldn't work for a rover this size) and encouraged innovative thinking.

Remember that the engineering design process isn't meant to limit your creativity - it's meant to channel it effectively!

## **Activity 2: Robot Case Study Analysis**

Analyze the design process behind a well-known robot (e.g., Mars Rover, Roomba) using provided resources. Identify how each of the five engineering design steps was implemented in the development of this robot and what challenges were addressed during each phase.

---pagebreak---

## **Connecting to Input-Processing-Output**

This section links the design process to the input-processing-output framework.

### **Inputs in the Design Process**

When designing robots, the input components are crucial because they determine how your robot will gather information about its environment. During the engineering design process, you'll make important decisions about what types of inputs your robot needs and how they should function.

In the "Define the Problem" step, you identify what information your robot needs to collect. For example, if you're designing a line-following robot, you need inputs that can detect the line. During the "Research and Ideate" phase, you'll explore different input options like infrared sensors, color sensors, or cameras.

By the "Design Solutions" step, you'll select specific input components and plan their placement on the robot. For instance, you might decide to use three infrared sensors positioned at the front of your robot to detect the line with greater accuracy. During "Build and Test," you'll install these sensors and evaluate how well they detect the line under different conditions.

The "Improve and Iterate" phase often involves refining your input systems. You might adjust sensor positions, add additional sensors, or modify the sensitivity settings to improve how your robot gathers information.

### **Processing in the Design Process**

The processing elements of your robot are where the "thinking" happens – how your robot will make decisions based on the inputs it receives. Throughout the engineering design process, you'll develop and refine this critical component.

During the "Define the Problem" step, you determine what decisions your robot needs to make. For a maze-solving robot, the processing must handle navigation decisions at intersections. In the "Research and Ideate" phase, you might explore different algorithms like wall-following or mapping approaches.

The "Design Solutions" step involves creating detailed plans for your processing system, including programming flowcharts that show how your robot will respond to different input scenarios. For example, you might design logic that says "If the right sensor detects a wall, turn left."

When you reach "Build and Test," you'll implement your processing design through programming and test how well your robot makes decisions. This often reveals the need for adjustments in your logic or algorithm.

The "Improve and Iterate" phase frequently focuses on refining the processing elements. You might add more sophisticated decision-making capabilities, optimize your code for faster response times, or create more robust error-handling routines.

### **Outputs in the Design Process**

The output components determine how your robot will act on its decisions and interact with the world. Throughout the engineering design process, you'll select and refine these action systems.

In the "Define the Problem" step, you identify what actions your robot needs to perform. For a robot that sorts objects, outputs might include movement and a mechanism to pick up and place items. During "Research and Ideate," you'll explore different motor types, grippers, or other mechanisms that could perform these actions.

The "Design Solutions" phase involves creating detailed plans for your output systems, including mechanical designs for moving parts and specifications for motors or servos. For example, you might design a robotic arm with specific dimensions and movement capabilities.

During "Build and Test," you'll construct these output systems and evaluate their performance. You might test how accurately your robot can place objects or how smoothly it navigates around obstacles.

The "Improve and Iterate" phase often focuses on refining output systems for better performance. You might adjust motor speeds, redesign mechanical components for greater precision, or add feedback systems that help the robot correct its movements.

### **Input-Processing-Output in Weather Station Robots**

Let's look at how the input-processing-output framework applies to a real-world example: a weather station robot that collects environmental data and responds to changing conditions.

**Inputs:** A weather station robot might include:
- Temperature sensors to measure air temperature
- Humidity sensors to detect moisture in the air
- Wind speed sensors to measure how fast the wind is blowing
- Rain sensors to detect precipitation
- Light sensors to measure sunlight levels

**Processing:** The robot's processing system would:
- Collect data from all sensors regularly
- Compare readings to normal ranges
- Identify patterns or sudden changes
- Make decisions about when to take protective actions
- Store data for later analysis

**Outputs:** Based on its processing, the robot might:
- Close protective covers when rain is detected
- Rotate solar panels to follow the sun
- Send alert messages when extreme conditions are detected
- Display current weather information on a screen
- Adjust its position to get better readings

During the engineering design process, the team would need to carefully consider each of these elements. In the "Define the Problem" step, they would determine what weather conditions to monitor and what actions the robot should take. In "Research and Ideate," they would explore different sensor options and protection mechanisms. The "Design Solutions" phase would involve creating detailed plans for how all these components would work together. During "Build and Test," they would construct the weather station and test it under various conditions. Finally, in "Improve and Iterate," they would refine the system based on performance in real weather situations.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider how the input-processing-output framework aligns with the steps of the design process. Where do you see connections? Identify which steps of the design process focus most heavily on inputs, processing, and outputs.
---stopandreflectEND---

---checkyourunderstanding---
Which of the following best describes the relationship between the engineering design process and the input-processing-output framework?

A. They are completely separate approaches that cannot be used together

B. The engineering design process replaces the need for the input-processing-output framework

C. The input-processing-output framework helps organize the components selected during the design process

D. The engineering design process only applies to the programming aspects of robotics
---answer---
The correct answer is C. The input-processing-output framework helps organize the components selected during the design process. The engineering design process provides the overall methodology for solving problems, while the input-processing-output framework helps specifically with organizing how a robot will gather information (inputs), process that information, and respond (outputs) when designing robot solutions. If you chose a different answer, remember that these frameworks complement each other rather than competing or replacing one another.
---answerEND---
---checkyourunderstandingEND---

## **Key Takeaways**

- The engineering design process is a systematic approach with five key steps: define, research, design, build/test, and improve
- Systematic design approaches provide better results than trial-and-error by considering multiple solutions and testing thoroughly
- The input-processing-output framework integrates with the design process, particularly when selecting components and planning functionality