# Visual Hierarchy Across Platforms Toolkit

## Downloadable Resources

### 1. Platform Comparison Matrix

Use this matrix to systematically analyse how visual hierarchy elements must adapt across different platforms while maintaining brand consistency.

| Hierarchy Element | Print | Digital/Web | Mobile | Environmental |
|-------------------|-------|-------------|--------|---------------|
| **Typography** | Fixed sizes, sophisticated typographic systems, physical texture | Responsive sizing, limited font options, screen rendering | Extreme size constraints, legibility at small sizes, thumb-zone priorities | Viewing distance considerations, physical materials, environmental lighting |
| **Colour** | CMYK limitations, paper stock affects appearance, special finishes | RGB spectrum, backlit display, interactive states | Screen brightness variation, outdoor visibility concerns, battery impact | Lighting conditions, material interactions, weathering considerations |
| **White Space** | Fixed canvas, physical margins, tactile page turns | Responsive containers, scrolling interactions, device-specific margins | Critical for touch targets, limited screen real estate, orientation changes | Physical space constraints, viewing angles, movement pathways |
| **Visual Weight** | Physical weight of materials, embossing, paper stock | Contrast ratios, animation, interactive states | Thumb zone prioritisation, portrait/landscape adaptation | Scale relative to human body, distance hierarchy, environmental context |
| **Contrast** | Ink density, paper texture, physical finishes | Screen resolution, brightness settings, hover states | High contrast for outdoor use, accessibility in varied lighting | Viewing distance, environmental lighting, weather conditions |

#### Example: Completed Matrix for Nike

| Hierarchy Element | Print (Catalogue) | Digital/Web (Homepage) | Mobile (App) | Environmental (Store) |
|-------------------|-------|-------------|--------|---------------|
| **Typography** | Bold Nike Sans headlines at 32pt+, product details in 9-10pt | Dynamic headline scaling (36-72px), Nike Sans for all text with 16px minimum body text | Product names in 18px bold, stats/prices in 14px, system fonts as fallback | Large dimensional letterforms for category markers, readable product info at 5ft distance |
| **Colour** | Rich black on white backgrounds, "Volt" yellow-green as accent (10-15% coverage) | White backgrounds, black text, interactive elements in Nike "Volt" with hover states | Dark mode option with light text, "Volt" for CTAs within thumb zone | Matte black fixtures, targeted lighting on product, "Volt" as wayfinding accents |
| **White Space** | Generous margins (1.5-2cm), product isolation on white | Content blocks with 40px minimum padding, scrolling sections with clear visual breaks | 16px minimum padding, expanded spacing (24px) around purchase buttons | Clear pathways minimum 4ft wide, product displays with 2ft minimum separation |

## Cross-Platform Conflict Resolution Framework

When hierarchy requirements conflict between platforms, follow this decision-making process:

### Step 1: Identify the Core Purpose
- What is the primary user need or business goal for this element?
- Which platform is most critical for this particular interaction?

### Step 2: Evaluate Constraints
- Which constraints are immovable (technical limitations, accessibility requirements)?
- Which constraints are flexible (stylistic preferences, secondary information)?

### Step 3: Prioritise Solutions
1. **Adapt the execution, maintain the principle** - Keep the same hierarchy principle but implement differently per platform
2. **Create platform-specific alternatives** - Develop different approaches that achieve the same goal
3. **Simplify across all platforms** - Reduce complexity to find a solution that works everywhere
4. **Progressive enhancement** - Create a base version that works everywhere, then enhance for platforms that allow it

### Step 4: Document Decisions
- Record which approach was selected and why
- Create a pattern library showing how each element adapts across platforms

### Documentation Template for Cross-Platform Decisions

| Element | Core Purpose | Platform Variations | Solution Approach | Rationale |
|---------|--------------|---------------------|-------------------|-----------|
| Primary CTA | Drive conversions | Web: Full button<br>Mobile: Floating button<br>Print: QR code with CTA | Adapt execution (#1) | Maintains prominence while respecting platform constraints |
| Navigation | Content discovery | Web: Horizontal menu<br>Mobile: Hamburger menu<br>Print: Table of contents | Platform-specific (#2) | Different space constraints require different approaches |

## Distinguishing Foundational Principles vs. Implementation Techniques

### Foundational Principles (Platform-Independent)
These core principles transfer across all platforms:
- **Visual Contrast** between important and secondary elements
- **Proximity** of related items
- **Alignment** to create order and relationships
- **Repetition** to establish patterns and recognition
- **Direction** of user attention through visual flow

### Implementation Techniques (Platform-Specific)
These techniques vary based on platform constraints:
- **Specific font sizes** (16px web vs. 9pt print)
- **Interaction methods** (hover states on web, touch targets on mobile)
- **Colour values** (RGB for digital, CMYK for print)
- **Space allocation** (fixed in print, responsive in digital)
- **Animation** (possible in digital, static in print)

## Testing Methodologies for Cross-Platform Hierarchy

When validating your hierarchy effectiveness across platforms, consider these proven testing approaches:

### 1. Five-Second Tests
- **Method**: Show users your design for 5 seconds, then ask what they remember.
- **Application**: Run separate tests for each platform to compare if the same key elements are being remembered.
- **Tools**: UsabilityHub, Maze, or simple screen sharing with a timer.

### 2. First-Click Testing
- **Method**: Ask users where they would click first to complete a specific task.
- **Application**: Compare first-click patterns across platforms to ensure primary actions maintain prominence.
- **Tools**: Optimal Workshop, UserZoom, or manual observation.

### 3. Squint Test
- **Method**: Look at your design while squinting to blur the details.
- **Application**: Elements that remain visible indicate effective hierarchy; compare results across platforms.
- **Tools**: No special tools required; alternatively use blur filters in design software.

### 4. A/B Testing with Heat Maps
- **Method**: Create variations of your hierarchy and track user engagement with heat maps.
- **Application**: Compare which hierarchy approach performs best on each platform.
- **Tools**: Hotjar, Crazy Egg, or platform-specific analytics.

## Future-Proofing Questions

Answer these questions to ensure your hierarchy approaches remain effective as technology evolves:

1. **Foundation vs. Implementation:** Which aspects of your hierarchy strategy are foundational principles (that will transfer to any platform) versus implementation techniques (that are platform-specific)?

2. **Responsive Planning:** How can your hierarchy system accommodate unknown future screen sizes, interaction methods, or environmental contexts?

3. **Technological Independence:** Which hierarchy techniques rely on specific current technologies that might become obsolete?

4. **Core Experience:** What is the essential user journey or content prioritisation that must be preserved regardless of platform?

5. **Adaptation Triggers:** What metrics or observations would signal that your hierarchy approach needs to be updated for new platforms?