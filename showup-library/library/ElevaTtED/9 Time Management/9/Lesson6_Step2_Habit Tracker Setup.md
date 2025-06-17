---
module: "9"
lesson: "6"
step_number: "2"
step_title: "Habit Tracker Setup"
template_type: "tutorial"
target_learner: "See separate learner profile document"
generation_date: "2025-06-10 07:22:58"
---

# Habit Tracker Setup

# Habit Tracker Setup in Notion

## Introduction
Building consistent habits is a cornerstone of effective time management and academic success. In this lesson, you'll learn how to create a customized habit tracker in Notion that will help you monitor your daily routines, visualize your progress, and stay accountable to your goals—whether you're balancing coursework, work responsibilities, or personal commitments.

## Learning Objectives
By the end of this lesson, you will be able to:
- Create a personalized habit tracking system in Notion
- Set up properties and formulas to monitor your progress
- Implement a mobile-friendly tracking solution
- Develop strategies for maintaining consistent habits

## Setting Up Your Habit Tracker

### Step 1: Create a New Database
1. Open Notion and click the "+ New Page" button in the sidebar
2. Select "Table - Database" from the options
3. Name your database "Habit Tracker" at the top of the page

![Example of Notion's New Page menu with Table Database highlighted](https://placeholder-image.com/notion-new-database.jpg)

### Step 2: Set Up Properties
Let's customize your database with the right properties to track your habits effectively:

1. Create a "Habit" property (this is your default Title column)
2. Add a "Category" property (Select type) with options like:
   - Academic (for study sessions, assignment completion)
   - Health (for exercise, sleep, nutrition)
   - Productivity (for time management, organization)
   - Personal Development (for reading, skills practice)
3. Add a "Frequency" property (Select type) with options:
   - Daily
   - Weekly
   - Monthly
4. Add a "Completion" property (Formula type) - we'll set this up later
5. Add a "Days Completed" property (Number type)
6. Add a "Target Days" property (Number type)

**Pro Tip:** Consider what habits would most support your academic success at Excel High School. For example, tracking daily study time, assignment completion, or reading progress.

### Step 3: Set Up Formulas
For the "Completion" property, enter this formula:
```
round(prop("Days Completed") / prop("Target Days") * 100) + "%"
```

This will calculate your completion percentage automatically.

### Step 4: Create a Progress Bar
1. Add a "Progress" property (Formula type)
2. Enter this formula:
```
slice("■■■■■■■■■■", 0, floor(prop("Days Completed") / prop("Target Days") * 10)) + slice("□□□□□□□□□□", 0, 10 - floor(prop("Days Completed") / prop("Target Days") * 10))
```
3. This creates a visual progress bar using filled and empty squares

**Troubleshooting Tip:** If you encounter errors with the formula, double-check that you've copied it exactly as shown, including all quotation marks and parentheses.

### Step 5: Add Your Habits
Begin adding habits to your tracker:
1. Click "+ New" to add a habit
2. Name it (e.g., "Complete one Excel High School assignment")
3. Select a category
4. Set frequency
5. Enter target days (e.g., 30 for a monthly goal)
6. Start with 0 for days completed

**Example Habits for Excel High School Students:**
- Complete one course module
- Study for 45 minutes without distractions
- Review feedback on previous assignments
- Prepare questions for my Success Coach
- Check announcements and updates in my Student Portal

## Syncing to Mobile

1. Download the Notion app on your mobile device
2. Log in with the same account credentials
3. Navigate to your workspace
4. Find and bookmark your Habit Tracker for easy access
5. Enable notifications in Notion settings for daily reminders

## Daily Usage Tips

1. Update your tracker daily by increasing the "Days Completed" number
2. Watch your progress bar fill up as you maintain consistency
3. Review weekly to identify patterns and areas for improvement
4. Adjust target days as needed based on your progress
5. Celebrate small wins to build motivation

## Reflection Activity

Take a moment to consider:
1. What three habits would most improve your academic performance?
2. What time of day would be best for you to update your habit tracker?
3. How might you reward yourself for maintaining consistency?

## Conclusion

Your Notion habit tracker serves as both a checkpoint system and a visual nudge to maintain progress on your goals. By documenting your habits and seeing your progress, you're applying effective self-direction techniques that support your time management skills—a critical component for success in Excel High School's asynchronous learning environment.

**Next Steps:** After setting up your habit tracker, consider sharing your academic goals with your Success Coach for additional accountability and support.