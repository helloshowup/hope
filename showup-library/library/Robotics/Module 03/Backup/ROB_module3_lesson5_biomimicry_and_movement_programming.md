# 3.5
# **Biomimicry and Movement Programming**


Imagine watching a gecko climb up a smooth glass wall or a cheetah sprint across the savanna. These amazing animal movements have inspired engineers to create robots that can do similar things! In this podcast, we explore how scientists carefully study the way animals move in nature and then use these observations to design better robots. We'll hear from robotics engineers who spend their days watching high-speed videos of jumping spiders or swimming fish, trying to understand exactly how these creatures achieve such incredible movements. These nature-inspired designs help robots climb walls, run faster, or move more efficiently through water - all by copying what animals have perfected over millions of years of evolution.

## **Understanding Biomimicry in Robotics**
Biomimicry is like being a detective who looks for clues in nature to solve engineering problems. When engineers need to design a robot that can do something challenging - like climb stairs or move through sand - they often look at how animals already solve these problems.

### **Learning from Nature's Solutions**
Animals have had millions of years to develop amazing ways of moving through their environments. Think about how effortlessly a squirrel jumps between tree branches or how a snake can slither over almost any surface. These movement solutions weren't designed overnight - they evolved over countless generations as animals adapted to survive in their environments.

Engineers have realized that instead of starting from scratch, they can study these time-tested designs from nature. For example, by examining how ants coordinate their six legs to walk over uneven terrain, roboticists have created robots that can navigate disaster areas with rubble and obstacles. Similarly, studying how birds adjust their wing shapes during flight has helped create drones that can fly more efficiently and handle windy conditions better.

These natural solutions often solve problems in surprisingly simple and energy-efficient ways that engineers might never have thought of on their own.

### **Benefits of Biomimetic Approaches**
When engineers use biomimicry (copying nature's designs), they gain several important advantages. First, nature's solutions are usually very energy-efficient. Animals can't afford to waste energy when moving - they need to conserve it to survive. This efficiency is extremely valuable for robots, especially those running on batteries.

Second, animal movements are incredibly adaptable. Watch how a cat can adjust its jumping technique depending on the height and distance it needs to cover. This adaptability helps engineers create robots that can work in changing environments rather than just controlled settings.

Third, different animals have specialized movement abilities for specific environments. Robots designed after geckos can climb walls, while those inspired by fish can navigate underwater with amazing precision. By selecting the right animal inspiration, engineers can create robots perfectly suited for particular tasks - whether that's exploring Mars, searching through collapsed buildings, or delivering packages.

## **Activity 1: Animal-Robot Connection**
Match animals to robots inspired by their movement patterns, then identify what features were copied and why. Select from a provided list of animals and robot designs, then explain the biomimetic principles that connect them and the engineering advantages gained.

---pagebreak---

## **Animal-Inspired Robot Designs**
Let's explore some of the fascinating ways that engineers have borrowed movement ideas from different types of animals to create amazing robots.

### **Insect-Inspired Robots**
Insects might be small, but they're movement superstars! With their six or more legs, insects can walk over almost any surface while staying balanced and stable. This has made them perfect inspiration for robots that need to navigate rough or uneven terrain.

The RHex robot, for example, uses six curved legs inspired by cockroaches to move across sand, rocks, and even climb stairs. By copying the way cockroaches coordinate their leg movements, RHex can maintain stability even when climbing over obstacles. Another example is the Harvard Microrobotics Lab's RoboBee, which mimics how bees move their wings to create tiny flying robots smaller than a paperclip!

Engineers particularly value insect designs because they're relatively simple compared to larger animals, yet incredibly effective. Many insect-inspired robots are being developed for search and rescue missions, where they need to crawl through tight spaces in collapsed buildings or navigate disaster areas too dangerous for humans.

### **Mammal and Reptile Movement Adaptations**
Mammals and reptiles offer different movement strategies that have proven valuable for robotics. Boston Dynamics' Spot robot dog uses a four-legged design inspired by how dogs and other quadrupeds walk and run. By carefully studying how these animals shift their weight and coordinate their legs, engineers created a robot that can climb stairs, navigate rough terrain, and even recover its balance when pushed.

Snake robots represent another fascinating area of biomimicry. Real snakes can move without any legs, using a series of specialized movements like side-winding or concertina motion. Engineers have created snake-inspired robots with many connected segments that can squeeze through tight spaces, climb poles, and even swim. These snake robots are especially useful for inspecting pipes, exploring narrow caves, or searching through rubble after earthquakes.

The way lizards use their tails for balance has even inspired robots that can adjust their "tails" to maintain stability when jumping or running at high speeds.

### **Bird and Fish Locomotion in Robotics**
The sky and sea have provided engineers with incredible movement inspiration. Flying and swimming require specialized movement techniques that robots can benefit from copying.

Aerial robots (drones) have borrowed many features from birds. Some drones now have wings that can change shape mid-flight, just like birds do when they transition from cruising to landing. Others use bird-inspired takeoff and landing techniques. The Festo company created a robotic seagull called SmartBird that can take off, fly, and land by flapping its wings just like a real bird, without using propellers.

Underwater, fish-inspired robots show how biomimicry can create smooth, efficient swimmers. MIT's robotic fish copies the way real fish move their bodies in a wave-like motion to push through water. This approach uses less energy than traditional propellers and creates less disturbance in the water, making these robots ideal for studying marine life without scaring it away. Other underwater robots mimic the unique movement of manta rays or the jet propulsion of squids and octopuses.

These bio-inspired designs allow robots to move through air and water with greater efficiency and maneuverability than conventional designs.

---pagebreak---

### **Real-World Success Stories in Biomimicry**

Let's look at some exciting examples of how animal movement has been successfully copied in real robots:

**Gecko-Inspired Climbing Robots**: Scientists at Stanford University created a robot called "Stickybot" that can climb smooth vertical surfaces like glass. The robot uses special adhesive pads inspired by gecko feet, which have millions of tiny hairs that create a molecular attraction to surfaces. These robots could someday help with building inspections or window cleaning on skyscrapers!

**Salamander-Inspired Amphibious Robot**: Researchers in Switzerland built a robot called "Pleurobot" that can both walk on land and swim in water just like a salamander. By carefully studying salamander skeletons and movements, they created a robot that smoothly transitions between environments - perfect for monitoring lakes and shorelines.

**Kangaroo-Inspired Jumping Robot**: Engineers at Festo created "BionicKangaroo," a robot that captures the energy-efficient jumping motion of real kangaroos. The robot stores energy from each landing to power its next jump, just like real kangaroos do. This energy-saving technique could help create more efficient robots for package delivery or exploration.

These examples show how studying nature's solutions can lead to breakthrough technologies that might not have been discovered through traditional engineering approaches.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about an animal that moves in an interesting way. How might its movement strategy solve a robot design challenge? Consider the unique aspects of that animal's locomotion and how those principles could address specific robotic movement problems.
---stopandreflectEND---

## **Basic Movement Programming**
Now that we understand how robots can be designed to move like animals, let's explore how we actually tell robots to move using programming.

### **Movement Commands and Sequences**
Programming a robot to move starts with basic commands - the simple instructions that control individual actions. These are like the building blocks of robot movement. Common movement commands include:

- move_forward(distance)
- turn_left(degrees)
- turn_right(degrees)
- stop()
- set_speed(value)

These commands by themselves only create very simple movements. To make a robot perform useful tasks, we need to combine these commands into sequences - ordered lists of instructions that the robot follows one after another.

For example, to make a robot navigate around a square path, we might create this sequence:
1. move_forward(10)
2. turn_right(90)
3. move_forward(10)
4. turn_right(90)
5. move_forward(10)
6. turn_right(90)
7. move_forward(10)

When the robot follows this sequence, it will trace a square pattern. By changing the order of commands or adding new ones, we can create an endless variety of movement patterns. Think of it like a dance routine - each step must be performed in the right order to create the complete dance.

---pagebreak---

### **Loops and Conditions in Movement**
Writing out long sequences of commands can get tedious, especially when there are repeated patterns. This is where loops come in handy. A loop is a programming structure that repeats a set of commands multiple times.

Using our square path example, instead of writing out the same commands repeatedly, we could use a loop:

```
Repeat 4 times:
    move_forward(10)
    turn_right(90)
```

This loop accomplishes the same square path but with much less code. Loops are especially useful for repetitive movements like walking (where leg motions repeat) or for tasks that need to be done multiple times.

Conditions add another level of intelligence to robot movement. A condition is a programming structure that makes decisions based on certain criteria, usually written as "if-then" statements:

```
if (obstacle_detected) then
    turn_right(90)
else
    move_forward(5)
```

With conditions, robots can adapt their movements based on what's happening around them. This is crucial for creating robots that can navigate real-world environments where unexpected obstacles or situations might arise.

By combining basic commands with loops and conditions, we can create surprisingly complex and adaptive movement behaviors - from simple line-following robots to machines that can navigate mazes or avoid obstacles.

## **Activity 2: Movement Algorithm Design**
Design a basic step-by-step movement algorithm for a robot to navigate a simple obstacle course. Create a flowchart or pseudocode that includes movement commands, decision points based on potential obstacles, and repeat instructions where appropriate.

## **Connecting Sensors to Movement**
For robots to move intelligently in the real world, they need to sense their environment and adjust their movements accordingly.

### **Responsive Movement Behaviors**
Responsive movement means a robot can change what it's doing based on what it senses around it. This is what makes the difference between a robot that blindly follows commands and one that can adapt to its environment.

For example, a line-following robot uses light sensors to detect a dark line on a light surface. When the sensor detects it's moving off the line, the robot adjusts its direction to stay on track. This creates a responsive behavior where the robot continuously corrects its path based on sensor input.

Another example is a robot vacuum that uses bump sensors to detect walls and furniture. When it bumps into something, it changes direction to avoid the obstacle and continue cleaning. Some advanced models even use distance sensors to slow down before they hit obstacles.

These responsive behaviors make robots much more useful in unpredictable environments. Instead of needing perfect instructions for every possible situation, the robot can make decisions on its own based on what it senses.

---pagebreak---

### **Programming Decision Trees**
To create responsive behaviors, we use decision trees in our programming. A decision tree is like a flowchart that helps the robot decide what to do next based on sensor information.

Here's a simple example of a decision tree for a robot navigating a room:

```
Check front distance sensor
If distance < 20 cm:
    Check left distance sensor
    If left distance > 30 cm:
        Turn left
    Else:
        Check right distance sensor
        If right distance > 30 cm:
            Turn right
        Else:
            Turn around
Else:
    Move forward
```

This decision tree helps the robot avoid obstacles by checking sensors and making movement decisions based on what it detects. The robot first checks if there's an obstacle directly ahead. If there is, it looks for clear space to the left or right. If there's no clear path in any direction, it turns around.

More complex decision trees can handle many different sensor inputs and situations. For example, a search and rescue robot might use temperature sensors, cameras, microphones, and distance sensors together to find people in a disaster area, with a decision tree that prioritizes investigating areas with signs of human presence.

By combining sensors with well-designed decision trees, robots can navigate complex environments and respond appropriately to changing conditions - much like animals do in nature.

### **Sensors in Action: Real-World Examples**

Let's look at how different sensors help robots move in the real world:

**Robot Vacuum Cleaners**: These popular home robots use several sensors working together. Bump sensors tell the robot when it hits something, cliff sensors prevent it from falling down stairs, and some models use cameras to map your home. All these sensors feed information to the robot's program, which decides how to move next - just like you might navigate around furniture in a dark room by feeling your way.

**Line-Following Robots**: Many beginner robots use simple light sensors to follow a dark line on a light background. When the sensor detects the robot moving off the line, it signals the wheels to adjust - turning left if the robot drifts right, or turning right if it drifts left. This creates a zigzag pattern that keeps the robot following the line, similar to how you might follow a trail in the woods.

**Drone Obstacle Avoidance**: Modern drones use distance sensors (like sonar or infrared) to detect obstacles in their path. When flying toward a tree, the sensors detect the obstacle and automatically adjust the drone's flight path to avoid collision. Some advanced drones can navigate through forests without hitting branches - similar to how birds fly through dense trees.

These examples show how sensors act like robot "senses" - providing the information needed to make smart movement decisions, just like your eyes, ears, and sense of touch help you move through the world.

---stopandreflect---
**CHECKPOINT:** Consider a robot that needs to navigate around obstacles. What decision process would it need to follow? How would you program this? Think about the sensors the robot would need and the logical steps in its decision-making process.
---stopandreflectEND---

---checkyourunderstanding---
A robotics team is designing a robot to climb vertical surfaces. Which animal would provide the MOST useful biomimicry inspiration?

A. Kangaroo

B. Gecko

C. Dolphin

D. Ostrich
---answer---
The correct answer is B. Gecko. Geckos can climb virtually any surface thanks to millions of microscopic hairs on their feet that create molecular attraction. Gecko-inspired adhesion has been successfully used in climbing robots, making them the most useful inspiration for vertical climbing capabilities. If you chose a different answer, consider why the animal's movement specialization might not be suited for vertical climbing - kangaroos excel at jumping, dolphins at swimming, and ostriches at running.
---answerEND---
---checkyourunderstandingEND---

---pagebreak---

**This lesson could be followed by this game:**
Programming Simulation: Robot Path Planner where students create a sequence of movement commands to navigate a virtual robot through an obstacle course. For example, students could be given a grid-based environment with obstacles and a target location, then must use directional commands, loops, and conditionals to guide their robot successfully to the goal while avoiding obstacles.
