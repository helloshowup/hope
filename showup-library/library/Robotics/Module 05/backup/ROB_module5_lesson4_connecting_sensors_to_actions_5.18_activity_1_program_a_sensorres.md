# 5.18
## **Activity 1: Program a Sensor-Responsive Robot**

Using our virtual robot simulator, create a program that makes the robot respond to different sensor inputs. Your robot should stop when its distance sensor detects an object within 15cm, turn left when a touch sensor on its right side is pressed, and turn right when a touch sensor on its left side is pressed. Test your program with different obstacles to see how effectively your robot navigates around them. This activity demonstrates how sensor inputs directly influence robot behavior.

## **Testing Sensor-Based Programs**

Creating a sensor-based program is only the first step. Testing and refining these programs ensures reliable robot behavior.

### **Systematic Testing Approaches**

To effectively test sensor-based programs:

1. **Start with controlled inputs**: Begin by manually activating sensors to verify basic functionality
2. **Test edge cases**: Check behavior at the boundaries of your threshold values
3. **Create realistic test scenarios**: Test your robot in conditions similar to its intended environment
4. **Incremental development**: Start with simple behaviors and build complexity gradually

When testing a robot with a distance sensor, for example, you might first place an object exactly at your threshold distance (like 15cm) to see if the robot responds correctly. Then try moving the object slightly closer and slightly farther to test the boundaries of your program's decision-making.

It's also important to test in different lighting conditions if you're using light sensors, or on different surfaces if you're using touch sensors. The more thoroughly you test, the more reliable your robot will be when faced with real-world situations.

A good testing plan might look like this:
- Test each sensor individually before combining them
- Test on different surfaces (carpet, tile, wood)
- Test in different lighting conditions (bright, dim, natural light)
- Test with different obstacles (soft objects, hard objects, different shapes)
- Test with multiple obstacles at once

Remember that testing isn't just about finding problems—it's about making your robot smarter and more reliable. Each test helps you refine your program and improve your robot's performance.

---stopandreflect---
## Stop and reflect

**CHECKPOINT:** Consider how a robot that follows pre-programmed instructions differs from one that responds to sensor inputs. How does the addition of sensors transform what the robot can accomplish and how it interacts with the world around it?
---stopandreflectEND---