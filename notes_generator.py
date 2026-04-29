# ============================================
# StudyMate AI - Smart Notes & Question Solver
# ============================================

def generate_notes(program, year, institution, subject, topic, difficulty):
    """Generate comprehensive structured notes"""

    prompt = f"""
You are an expert Pakistani curriculum educator and academic writer.

Generate comprehensive, exam-focused study notes for:
- Program     : {program}
- Year        : {year}
- Institution : {institution}
- Subject     : {subject}
- Topic       : {topic}
- Level       : {difficulty}

Structure the notes using EXACTLY this format:

## Introduction
**Definition:** [Clear definition of the topic]
**Explanation:** [Brief overview of what this topic covers]

## [Main Section 1 Title]
### [Subsection 1.1]
**Definition:** [Define this concept clearly]
**Explanation:** [Detailed explanation in simple language]
**Example:** [Real-world or clinical/technical example]
**Equation:** [If applicable — write formula clearly e.g. F = ma]
**Diagram:** [Describe what diagram/sketch a student should draw]
**Key Note:** [Most important exam point to remember]

### [Subsection 1.2]
[Repeat same structure]

## [Main Section 2 Title]
[Continue with same structure]

## Summary of Key Points
- [Key point 1]
- [Key point 2]
- [Key point 3]
- [Key point 4]
- [Key point 5]

## Important Formulas & Equations
**Equation:** [Formula 1 with explanation]
**Equation:** [Formula 2 with explanation]

## Exam Tips
- [Tip 1 specific to {institution} exam style]
- [Tip 2]
- [Tip 3]

## Common Exam Questions on This Topic
- [Likely question 1]
- [Likely question 2]
- [Likely question 3]

---

Rules:
- Write for {program} {year} level students in Pakistan
- Follow HEC and {institution} curriculum
- Use simple, clear language
- Be thorough — this is for exam preparation
- Include all relevant formulas, equations, diagrams where applicable
- Make notes comprehensive enough to score full marks
"""

    from ai_backend import chat
    return chat(prompt)
    return response["message"]["content"]


def solve_question(program, year, institution,
                   subject, topic, question, marks):
    """Generate a full marks answer for a specific question"""

    # Determine detail level based on marks
    if marks <= 2:
        detail = "very concise, 2-3 lines, define and one point"
        length = "2-3 sentences"
    elif marks <= 5:
        detail = "moderate detail with definition, explanation and example"
        length = "1 short paragraph with key points"
    elif marks <= 10:
        detail = "detailed with all sub-headings, examples, diagrams noted"
        length = "2-3 paragraphs with structured sections"
    else:
        detail = "very comprehensive, full essay-style with all sections"
        length = "full structured answer with all headings and sections"

    prompt = f"""
You are an expert Pakistani academic answer writer.

Write a {marks}-mark exam answer for the following question:

Question : {question}
Subject  : {subject}
Topic    : {topic}
Program  : {program}
Year     : {year}
Marks    : {marks}
Institution: {institution}

Write a complete answer that will score FULL MARKS ({marks}/{marks}).
Detail Level: {detail}
Expected Length: {length}

Use this EXACT format:

## Answer

### Introduction
**Definition:** [Define key terms in the question]
**Explanation:** [Brief intro — what you will cover]

### Main Content
[Based on marks ({marks}), provide {'brief' if marks <= 2 else 'detailed'} explanation]

### [Add relevant sub-sections based on question]
**Explanation:** [Core explanation]
**Example:** [Relevant example]
**Equation:** [If mathematical/scientific — show formula and working]
**Diagram:** [Describe diagram to draw if relevant]
**Key Note:** [Critical point examiner looks for]

### Conclusion
[Brief concluding statement — what was discussed]

---

Rules:
- Answer must be worthy of FULL {marks} marks
- Follow {institution} marking scheme style
- Include all points an examiner expects
- For {marks}-mark question: include exactly the right depth
- Use proper academic language for {program} level
- Include equations/formulas if topic requires
"""

    from ai_backend import chat
    return chat(prompt)