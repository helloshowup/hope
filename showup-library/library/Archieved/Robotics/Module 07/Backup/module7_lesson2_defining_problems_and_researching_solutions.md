# 7.2
# **Defining Problems and Researching Solutions**
## **Learning Objectives**

By the end of this session, you'll be able to:
- Create clear problem statements using structured templates
- Apply research and brainstorming techniques to generate multiple solution ideas
- Evaluate potential solutions against constraints and criteria

## **Lesson Podcast Discussion: Crafting Effective Problem Statements**

In today's podcast, we explore how well-defined problem statements lead to better robotics solutions. When engineers clearly understand what they're trying to solve, they're much more likely to create effective solutions.

For example, compare these two problem statements:
- Poor: "We need a robot that does stuff in the classroom."
- Good: "We need a robot that can safely navigate around classroom furniture to deliver materials to student groups while operating for at least 2 hours on a single battery charge."

The first statement is vague and provides almost no guidance. The second clearly defines what the robot needs to do, where it will operate, and a specific performance requirement. Teams working with the second statement will have a much clearer direction and can evaluate whether their solutions actually solve the problem.

Well-defined problems save time, reduce frustration, and lead to more successful robotics projects. Throughout this lesson, we'll learn how to craft these clear problem statements and use them to guide our solution development.

## **Defining the Problem**

Before we can build a robot to solve a problem, we need to understand exactly what that problem is. Imagine trying to build a bridge without knowing what river it needs to cross or what kind of traffic it needs to support! The same applies to robotics - we need a clear picture of the problem before we can design an effective solution.

In robotics, a well-defined problem helps us determine what sensors our robot might need, what actions it should perform, and what success looks like. Without this clarity, we might build something that doesn't actually solve the real issue or misses important requirements.

### **Elements of a Strong Problem Statement**

A strong problem statement is like a roadmap for your robotics project. It should include several key elements that guide your design process:

First, it needs a clear description of the issue - what's happening that shouldn't be, or what isn't happening that should be? For example, "Students with mobility challenges cannot easily access books from the top shelves in our library."

Second, it should define the scope - what parts of the problem will your solution address, and what parts won't it address? For instance, "Our solution will focus on retrieving books from shelves, not on cataloging or reshelving them."

Third, include measurable success criteria - how will you know if your solution works? For example, "The robot should be able to retrieve a requested book within 2 minutes and deliver it safely to the student."

When these elements come together, they create a clear target for your design efforts and help everyone understand exactly what you're trying to accomplish.

### **Problem Statement Template**

Here's a simple template you can use to create your own problem statements:

"The problem is that [describe the issue] affecting [who is affected]. A successful solution would [measurable outcome] while [important constraints]."

For example:
"The problem is that students waste time walking to the recycling bins during class, affecting learning time. A successful solution would reduce classroom interruptions by 50% while keeping recycling properly sorted."

This template helps you organize your thoughts and ensures you cover all the important parts of a good problem statement.

---pagebreak---

### **Identifying Stakeholders and Needs**

Stakeholders are all the people who will be affected by your robotics solution. They might include users who will directly interact with your robot, people who will benefit from its work, and even those who might be concerned about its operation.

To identify stakeholders, ask questions like:
- Who will use the robot?
- Who will benefit from the robot's actions?
- Who might be concerned about the robot operating in their space?
- Who will maintain or repair the robot?

For example, if you're designing a robot to help in a school cafeteria, stakeholders might include students, cafeteria staff, custodians, and school administrators.

Once you've identified stakeholders, you need to understand their specific needs. This might involve:
- Interviewing potential users
- Observing the current situation
- Conducting surveys
- Creating user personas (fictional characters that represent different user types)

Understanding these needs helps ensure your robot will actually be useful and accepted by the people it's designed to help.

### **Setting Constraints and Requirements**

**Constraints** are the limitations your solution must work within. They might include:

- Physical constraints: size, weight, or the environment where the robot will operate
- Technical constraints: available power sources, materials, or technology
- Time constraints: deadlines for completion or how quickly the robot must perform tasks
- Budget constraints: how much money is available for building and maintaining the robot
- Safety constraints: ensuring the robot won't harm people or property

**Requirements** are the specific things your solution must do or have. For example:
- The robot must be able to climb stairs
- The robot must operate for at least 3 hours on a single charge
- The robot must be controllable by someone with limited hand mobility

Clearly defining these constraints and requirements early helps prevent wasted effort on solutions that won't work in the real world. They act as guardrails for your creativity, ensuring your ideas remain practical and feasible.

## **Activity 1: Problem Definition Workshop**

Practice writing problem statements for given robotics scenarios using a structured template. For each scenario, identify the affected stakeholders, list the constraints, and define success criteria. Complete at least two scenario exercises to build your problem definition skills.

## **Problem Analysis Techniques**

Once you've identified a problem, it's important to dig deeper to fully understand it. Just like a doctor doesn't prescribe medicine without first diagnosing the illness, we shouldn't jump to solutions without thoroughly analyzing the problem.

### **Root Cause Analysis**

Root cause analysis helps us look beyond the symptoms of a problem to find what's really causing it. Two popular techniques for this are:

The **"5 Whys"** technique involves asking "why" repeatedly to dig deeper into a problem. For example:
- Why is the hallway delivery robot stopping unexpectedly? Because its sensors detect obstacles.
- Why are sensors detecting obstacles when none are visible? Because reflections from the floor tiles are confusing the sensors.
- Why are reflections causing confusion? Because the sensor algorithm can't distinguish between real obstacles and reflections.
- Why can't the algorithm distinguish these? Because it was programmed for matte surfaces, not shiny floors.
- Why was it programmed this way? Because the original testing environment had different flooring.

By the fifth "why," we've found a root cause we can address - the sensor algorithm needs updating for shiny floors.

**Fishbone diagrams** (also called Ishikawa diagrams) help visualize multiple potential causes. You draw a "fish skeleton" with the problem as the head, and different categories of causes (like People, Methods, Materials, Environment) as the bones. This helps you consider all possible factors contributing to the problem.

Using these techniques helps ensure you're solving the real problem, not just treating symptoms.

---pagebreak---

### **Needs Assessment**

A needs assessment helps you understand and prioritize what your solution must address. This involves:

1. Gathering information about what stakeholders need through interviews, surveys, or observation
2. Distinguishing between "needs" (must-haves) and "wants" (nice-to-haves)
3. Prioritizing needs based on importance and impact

For example, if designing a robot to help in a classroom, you might discover that:
- Must-have: The robot needs to be quiet so it doesn't disrupt lessons
- Must-have: The robot must be safe around children
- Nice-to-have: The robot could have a friendly appearance
- Nice-to-have: The robot could respond to voice commands

Prioritizing needs helps you focus your design efforts on the most important aspects first, ensuring your solution addresses what matters most.

### **Constraint Mapping**

Constraint mapping is a visual way to understand the limitations affecting your problem. It helps you see how different constraints interact and where your solution space lies.

To create a constraint map:
1. List all constraints (budget, time, technology, space, etc.)
2. Draw connections between related constraints
3. Identify which constraints are fixed and which might be flexible
4. Look for the "solution space" where all constraints can be satisfied

For example, if designing a robot arm for a classroom, your constraints might include cost (under $200), weight (light enough for students to move), safety (no pinch points), and functionality (able to pick up small objects). Your constraint map would show how these factors relate - perhaps a very lightweight arm might limit functionality, or increased functionality might raise costs.

This visual approach helps you understand the boundaries of your solution space and identify potential conflicts before you start designing.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Think about a problem you've encountered recently. How would you frame it as a clear problem statement using what you've learned? Try writing it down using the template discussed in class.
---stopandreflectEND---

## **Research Methods for Robotics Solutions**

Once you've defined your problem, the next step is researching potential solutions. Good research prevents you from "reinventing the wheel" and helps you build on existing knowledge.

### **Finding Existing Solutions**

Before creating something new, it's smart to see if similar problems have already been solved. This can save time and provide valuable insights.

Start by searching for existing robotics solutions that address similar problems. Look at:
- Commercial products that might solve or partially solve your problem
- Open-source robotics projects on platforms like GitHub or Instructables
- Academic research papers (even just reading the abstracts can be helpful)
- Robotics competition entries that tackled similar challenges

For example, if you're designing a robot to help sort recyclables, you might find that industrial sorting robots already use certain sensor types or gripper designs that could inspire your solution.

When examining existing solutions, ask:
- What works well about this solution?
- What limitations does it have?
- How could it be adapted to better fit my specific problem?
- What components or techniques could I borrow or learn from?

Remember, research isn't about copying - it's about learning from others and building upon their work.

### **Real-World Example: Weather Station Robot**

Let's look at how a real-world project used problem definition and research. A school wanted to create a weather station robot that could collect data around their campus and respond to changing conditions.

First, they defined their problem: "Our school needs accurate weather data from different locations on campus to support science classes, but manual collection is inconsistent and time-consuming."

They researched existing solutions by:
1. Looking at commercial weather stations (too expensive and fixed in one location)
2. Studying DIY weather station projects online (good sensor ideas but not mobile)
3. Examining agricultural robots that monitor field conditions (good mobility concepts)

By combining ideas from these existing solutions, they designed a mobile robot with temperature, humidity, and light sensors that could travel to different campus locations on a programmed schedule and upload data to the school's science website.

This example shows how good problem definition and research led to a unique solution that combined elements from different existing technologies.

### **Expert Consultation**

Experts can provide valuable insights that might take you weeks or months to discover on your own. They can help identify potential pitfalls, suggest approaches you hadn't considered, and provide feedback on your ideas.

Potential experts to consult might include:
- Teachers with robotics experience
- Local engineers or programmers
- College students studying robotics or engineering
- Members of robotics clubs or teams
- Professionals working in fields related to your problem

When consulting experts:
- Prepare specific questions in advance
- Clearly explain your problem and constraints
- Be open to suggestions that might challenge your assumptions
- Take good notes or record the conversation (with permission)
- Follow up with a thank-you and share your progress

Even a 15-minute conversation with someone knowledgeable can provide insights that significantly improve your solution.

### **Literature and Resource Review**

A literature review involves gathering and analyzing information from various sources to inform your solution design. For robotics projects, useful resources include:

- Textbooks and educational websites about robotics principles
- Online tutorials and how-to guides
- Manufacturer documentation for components you might use
- Videos of similar robots in action
- Forums where robotics enthusiasts discuss challenges and solutions

When conducting your review:
1. Start with broad searches, then narrow down to more specific topics
2. Keep track of your sources so you can refer back to them
3. Look for patterns or common approaches across multiple sources
4. Pay attention to both successes and failures described in the literature
5. Consider how the information applies to your specific problem and constraints

A thorough literature review helps you understand the current state of knowledge about your problem and builds a foundation for your own solution development.

---pagebreak---

## **Brainstorming and Ideation**

After researching existing solutions, it's time to generate your own ideas. Brainstorming is a creative process that helps you come up with multiple possible approaches to solving your problem.

### **Structured Brainstorming Techniques**

Structured brainstorming techniques provide frameworks that help guide your creative thinking. Here are some effective methods:

**Mind mapping** starts with your central problem in the middle of a page, then branches out with related ideas, creating a visual web of possibilities. For example, if your central problem is "robot navigation in a crowded space," branches might include "sensor types," "movement patterns," "obstacle detection," and "communication methods."

**SCAMPER** is an acronym that prompts different ways to modify existing ideas:
- Substitute: What could you swap out for something else?
- Combine: What could you merge with another element?
- Adapt: How could you adjust for another purpose?
- Modify: What could you change or magnify?
- Put to other uses: How else could this be used?
- Eliminate: What could you remove?
- Reverse/Rearrange: What if you did things in a different order?

For example, applying SCAMPER to a line-following robot might lead you to substitute different sensors, combine line-following with obstacle detection, adapt the design for different surfaces, etc.

**Rapid ideation** involves setting a timer (often 3-5 minutes) and challenging yourself to generate as many ideas as possible, focusing on quantity over quality. After the time is up, you can evaluate and refine the most promising ideas.

These structured approaches help overcome the blank page problem and push your thinking in new directions.

### **Balancing Structure and Creativity**

While structured techniques are helpful, it's also important to allow room for creative exploration. Here are some ways to balance structure with creativity:

1. **Start with wild ideas**: Begin your brainstorming session with a "no limits" period where you imagine solutions without worrying about constraints. This helps generate innovative approaches before narrowing down to practical solutions.

2. **Mix different techniques**: Alternate between structured methods and free-form brainstorming to get the benefits of both approaches.

3. **Use visual thinking**: Draw your ideas instead of just writing them. Sketches can help you think differently and communicate complex concepts quickly.

4. **Take inspiration breaks**: When you feel stuck, take a short break to look at something completely unrelated to your problem. Nature, art, or even everyday objects can spark new ideas.

5. **Build on "bad" ideas**: Sometimes a seemingly impractical idea contains the seed of a brilliant solution. Instead of dismissing unusual ideas, ask "What's good about this?" and build from there.

Remember, the engineering design process isn't meant to limit creativity—it's meant to channel it toward effective solutions. The most innovative robots often come from teams that successfully balance creative thinking with structured approaches.

### **Creative Thinking Methods**

Creative thinking methods help you break out of conventional thought patterns to discover innovative solutions.

**Analogical thinking** involves drawing inspiration from nature or unrelated fields. For example, robot grippers might be inspired by how an octopus tentacle or human hand works. Ask yourself: "What in nature or other fields solves a similar problem?"

**Reverse thinking** flips the problem on its head. Instead of asking "How can we make a robot navigate obstacles?" ask "How can we design a course that's easy for robots to navigate?" This perspective shift often reveals new approaches.

**Assumption challenging** involves identifying and questioning your assumptions. List everything you're assuming about the problem, then ask "What if this wasn't true?" For example, if you assume a robot needs wheels to move, challenging this might lead to walking, hopping, or rolling designs.

These methods help you think "outside the box" and can lead to breakthrough ideas that wouldn't emerge from conventional thinking.

### **Collaborative Ideation**

Robotics is rarely a solo endeavor - working with others can dramatically improve your ideation process.

Effective group brainstorming techniques include:

**Round-robin brainstorming**, where each team member takes turns sharing one idea at a time, ensuring everyone contributes equally.

**Brainwriting**, where team members write down ideas independently before sharing, which prevents dominant voices from controlling the conversation and gives quieter members equal input.

**"Yes, and..." building**, borrowed from improvisational theater, where each person builds on the previous idea rather than criticizing it. This creates a positive atmosphere where wild ideas are welcome.

When collaborating:
- Establish ground rules that encourage participation and respect
- Defer judgment during the ideation phase - no criticizing ideas yet
- Build on each other's ideas rather than competing
- Document all ideas, even ones that seem impractical at first
- Consider diverse perspectives, especially from team members with different backgrounds

Collaborative ideation often produces more creative and robust solutions than individual brainstorming, as different perspectives combine to create ideas no single person would have developed alone.

## **Activity 2: Solution Matrix Creation**

Develop a decision matrix for a robotics problem scenario. Identify at least three potential solutions and evaluate them against 4-5 specific criteria with weighted importance. Calculate final scores and determine which solution rates highest according to your analysis.

## **Evaluating Potential Solutions**

After generating multiple possible solutions, you need a systematic way to evaluate them and select the best option to develop further.

### **Developing Evaluation Criteria**

Evaluation criteria are the standards you'll use to judge potential solutions. Good criteria should be:

- Specific: Clear enough that different people would interpret them the same way
- Measurable: Able to be assessed objectively
- Relevant: Directly related to solving your problem
- Comprehensive: Covering all important aspects of the solution

Common criteria categories for robotics solutions include:

**Technical feasibility**: Can we actually build this with our skills and available technology?
Example criteria: "Can be built using components we have access to" or "Requires programming skills our team possesses"

**Performance**: How well will it solve the problem?
Example criteria: "Can complete the task in under 2 minutes" or "Works correctly at least 90% of the time"

**Resource requirements**: What will it take to build and maintain?
Example criteria: "Costs less than $200 to build" or "Can be assembled in less than 10 hours"

**User-friendliness**: How easy will it be to use?
Example criteria: "Can be operated after 5 minutes of training" or "Provides clear feedback to the user"

**Durability/reliability**: How robust is the solution?
Example criteria: "Functions for at least 3 hours continuously" or "Can withstand occasional bumps and drops"

For your specific problem, you might develop additional criteria based on unique requirements or constraints. The key is to create criteria that will help you objectively compare different solutions.

### **Using Decision Matrices**

A decision matrix (also called a Pugh matrix or selection matrix) is a powerful tool for objectively comparing multiple solutions. Here's how to create one:

1. List your potential solutions across the top of a table
2. List your evaluation criteria down the left side
3. Assign a weight to each criterion based on its importance (typically 1-5, where 5 is most important)
4. Rate how well each solution meets each criterion (typically 1-5, where 5 is excellent)
5. Multiply each rating by the criterion weight to get a weighted score
6. Add up the weighted scores for each solution
7. The solution with the highest total score is theoretically the best option

For example, if evaluating three different robot navigation systems:

| Criterion (weight) | Solution A | Solution B | Solution C |
|-------------------|-----------|-----------|-----------|
| Accuracy (5) | 4 (20) | 5 (25) | 3 (15) |
| Battery life (4) | 3 (12) | 2 (8) | 5 (20) |
| Cost (3) | 2 (6) | 1 (3) | 4 (12) |
| Ease of programming (3) | 5 (15) | 3 (9) | 2 (6) |
| **TOTAL** | **53** | **45** | **53** |

In this example, Solutions A and C tied with the highest score. When this happens, you might need to:
- Add more criteria to break the tie
- Give more weight to the most important criteria
- Build simple prototypes of both solutions to test them
- Combine the best elements of both solutions

### **Prioritizing Improvements Using Impact/Effort Analysis**

When evaluating potential solutions or improvements, it's helpful to consider both the impact (how much benefit it provides) and the effort required (time, resources, difficulty). This approach helps you focus on changes that give you the most value for your work.

To create an impact/effort matrix:
1. Draw a simple grid with four quadrants
2. Label the horizontal axis "Effort" (low to high)
3. Label the vertical axis "Impact" (low to high)
4. Place each potential solution or improvement in the appropriate quadrant

This creates four categories:
- High Impact, Low Effort: "Quick Wins" (do these first!)
- High Impact, High Effort: "Major Projects" (plan these carefully)
- Low Impact, Low Effort: "Fill-Ins" (do these when you have extra time)
- Low Impact, High Effort: "Time Wasters" (avoid these)

For example, if you're designing a delivery robot for your school:
- Quick Win: Adding reflective tape to make the robot more visible (high impact on safety, low effort)
- Major Project: Creating a mapping system so the robot can navigate independently (high impact on functionality, high effort)
- Fill-In: Painting the robot in school colors (low impact on function, low effort)
- Time Waster: Building a complex voice recognition system when a simple button interface would work (low impact on usability, high effort)

This approach helps you make smart decisions about where to focus your time and resources, especially when you have multiple possible improvements to consider.