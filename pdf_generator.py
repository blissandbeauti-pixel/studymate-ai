# ============================================
# StudyMate AI - Professional PDF Generator
# Uses ReportLab for formatted output
# ============================================

import io
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import (
    HexColor, white, black
)
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# ============================================
# COLOR PALETTE
# ============================================

PRIMARY       = HexColor("#1565C0")   # Dark blue
SECONDARY     = HexColor("#1976D2")   # Medium blue
ACCENT        = HexColor("#42A5F5")   # Light blue
GREEN         = HexColor("#2E7D32")   # Dark green
LIGHT_GREEN   = HexColor("#E8F5E9")   # Light green bg
PURPLE        = HexColor("#6A1B9A")   # Purple
LIGHT_PURPLE  = HexColor("#F3E5F5")   # Light purple bg
ORANGE        = HexColor("#E65100")   # Orange
LIGHT_ORANGE  = HexColor("#FFF3E0")   # Light orange bg
LIGHT_BLUE    = HexColor("#E3F2FD")   # Light blue bg
DARK_TEXT     = HexColor("#1A1A2E")   # Dark text
GRAY          = HexColor("#757575")   # Gray
LIGHT_GRAY    = HexColor("#F5F5F5")   # Light gray bg
HEADER_BG     = HexColor("#1565C0")   # Header background
DIVIDER       = HexColor("#BBDEFB")   # Divider color


# ============================================
# CUSTOM STYLES
# ============================================

def get_styles():
    styles = getSampleStyleSheet()

    custom = {

        # Document title
        "DocTitle": ParagraphStyle(
            "DocTitle",
            fontSize=22, fontName="Helvetica-Bold",
            textColor=white, alignment=TA_CENTER,
            spaceAfter=4, spaceBefore=4
        ),

        # Document subtitle
        "DocSubtitle": ParagraphStyle(
            "DocSubtitle",
            fontSize=11, fontName="Helvetica",
            textColor=HexColor("#BBDEFB"), alignment=TA_CENTER,
            spaceAfter=2
        ),

        # Meta info (program, subject etc.)
        "MetaText": ParagraphStyle(
            "MetaText",
            fontSize=9, fontName="Helvetica",
            textColor=GRAY, alignment=TA_CENTER,
            spaceAfter=2
        ),

        # Main heading (##)
        "Heading1": ParagraphStyle(
            "H1",
            fontSize=14, fontName="Helvetica-Bold",
            textColor=white, spaceAfter=6,
            spaceBefore=14, leftIndent=0,
            backColor=PRIMARY, borderPadding=(6, 10, 6, 10),
            borderRadius=4
        ),

        # Sub heading (###)
        "Heading2": ParagraphStyle(
            "H2",
            fontSize=12, fontName="Helvetica-Bold",
            textColor=SECONDARY, spaceAfter=4,
            spaceBefore=10, leftIndent=0,
            borderPadding=(4, 0, 4, 0),
        ),

        # Definition box
        "Definition": ParagraphStyle(
            "Def",
            fontSize=10, fontName="Helvetica",
            textColor=HexColor("#1A237E"),
            backColor=LIGHT_BLUE,
            leftIndent=10, rightIndent=10,
            spaceAfter=6, spaceBefore=4,
            borderPadding=(8, 10, 8, 10),
            leading=16
        ),

        # Explanation
        "Explanation": ParagraphStyle(
            "Expl",
            fontSize=10, fontName="Helvetica",
            textColor=DARK_TEXT,
            leftIndent=12, rightIndent=5,
            spaceAfter=5, spaceBefore=3,
            leading=16, alignment=TA_JUSTIFY
        ),

        # Example box
        "Example": ParagraphStyle(
            "Ex",
            fontSize=10, fontName="Helvetica",
            textColor=HexColor("#1B5E20"),
            backColor=LIGHT_GREEN,
            leftIndent=10, rightIndent=10,
            spaceAfter=6, spaceBefore=4,
            borderPadding=(8, 10, 8, 10),
            leading=16
        ),

        # Equation / Math
        "Equation": ParagraphStyle(
            "Eq",
            fontSize=11, fontName="Helvetica-Bold",
            textColor=HexColor("#4A148C"),
            backColor=LIGHT_PURPLE,
            leftIndent=10, rightIndent=10,
            spaceAfter=6, spaceBefore=4,
            borderPadding=(8, 10, 8, 10),
            alignment=TA_CENTER, leading=18
        ),

        # Key Note
        "KeyNote": ParagraphStyle(
            "KN",
            fontSize=10, fontName="Helvetica-Bold",
            textColor=HexColor("#BF360C"),
            backColor=LIGHT_ORANGE,
            leftIndent=10, rightIndent=10,
            spaceAfter=6, spaceBefore=4,
            borderPadding=(8, 10, 8, 10),
            leading=16
        ),

        # Diagram note
        "DiagramNote": ParagraphStyle(
            "DN",
            fontSize=9, fontName="Helvetica-Oblique",
            textColor=HexColor("#37474F"),
            backColor=HexColor("#ECEFF1"),
            leftIndent=10, rightIndent=10,
            spaceAfter=6, spaceBefore=4,
            borderPadding=(6, 10, 6, 10),
            leading=14
        ),

        # Bullet point
        "BulletPoint": ParagraphStyle(
            "BP",
            fontSize=10, fontName="Helvetica",
            textColor=DARK_TEXT,
            leftIndent=20, rightIndent=5,
            spaceAfter=3, spaceBefore=2,
            leading=15, bulletIndent=8,
        ),

        # Normal body text
        "Body": ParagraphStyle(
            "Body",
            fontSize=10, fontName="Helvetica",
            textColor=DARK_TEXT,
            spaceAfter=5, spaceBefore=2,
            leading=16, alignment=TA_JUSTIFY
        ),

        # Footer text
        "Footer": ParagraphStyle(
            "Footer",
            fontSize=8, fontName="Helvetica",
            textColor=GRAY, alignment=TA_CENTER
        ),

        # Section label
        "Label": ParagraphStyle(
            "Label",
            fontSize=9, fontName="Helvetica-Bold",
            textColor=SECONDARY, spaceAfter=2,
            spaceBefore=6
        ),
    }

    return custom


# ============================================
# HEADER & FOOTER
# ============================================

def build_header(student_name, subject, topic, doc_type):
    """Build professional header table"""
    styles = get_styles()

    title_text = f"{'📝 Smart Notes' if doc_type == 'notes' else '✏️ Question Solution'}"
    subject_line = f"{subject} — {topic}"

    header_data = [[
        Paragraph(title_text, styles["DocTitle"]),
    ]]

    header_table = Table(header_data, colWidths=[17 * cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HEADER_BG),
        ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING", (0, 0), (-1, -1), 15),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
    ]))

    return header_table


def build_meta_table(meta):
    """Build metadata info table below header"""
    data = [[
        f"👤 {meta.get('student_name', 'Student')}",
        f"🎓 {meta.get('program', '')}",
        f"📅 {meta.get('year', '')}",
        f"🏫 {meta.get('institution', '')}",
    ]]

    table = Table(data, colWidths=[4.25 * cm] * 4)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), PRIMARY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, DIVIDER),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return table


# ============================================
# CONTENT PARSER
# ============================================

def parse_and_build_content(ai_text, styles):
    """Parse AI-generated text into styled PDF elements"""
    story = []
    lines = ai_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line or line == "---":
            story.append(Spacer(1, 4))
            i += 1
            continue

        # === MAIN HEADING (##)
        if line.startswith("## "):
            text = line[3:].strip()
            story.append(Spacer(1, 8))
            story.append(Paragraph(f"  {text}", styles["Heading1"]))
            story.append(Spacer(1, 4))

        # === SUB HEADING (###)
        elif line.startswith("### "):
            text = line[4:].strip()
            story.append(Spacer(1, 6))
            # Underline effect with colored text
            story.append(Paragraph(
                f'<font color="#1976D2"><b>▶ {text}</b></font>',
                styles["Heading2"]
            ))
            story.append(HRFlowable(
                width="100%", thickness=1,
                color=ACCENT, spaceAfter=4
            ))

        # === DEFINITION
        elif line.lower().startswith("**definition"):
            text = re.sub(r'\*\*definition[:\s]*\*\*', '', line,
                          flags=re.IGNORECASE).strip()
            if not text:
                text = line
            story.append(Paragraph(
                f'<b>📖 Definition:</b> {text}',
                styles["Definition"]
            ))

        # === EXPLANATION
        elif line.lower().startswith("**explanation"):
            text = re.sub(r'\*\*explanation[:\s]*\*\*', '', line,
                          flags=re.IGNORECASE).strip()
            if not text:
                text = line
            story.append(Paragraph(
                f'<b>💡 Explanation:</b> {text}',
                styles["Explanation"]
            ))

        # === EXAMPLE
        elif line.lower().startswith("**example"):
            text = re.sub(r'\*\*example[:\s]*\*\*', '', line,
                          flags=re.IGNORECASE).strip()
            if not text:
                text = line
            story.append(Paragraph(
                f'<b>✏️ Example:</b> {text}',
                styles["Example"]
            ))

        # === EQUATION / FORMULA
        elif (line.lower().startswith("**equation") or
              line.lower().startswith("**formula")):
            text = re.sub(
                r'\*\*(equation|formula)[:\s]*\*\*', '',
                line, flags=re.IGNORECASE
            ).strip()
            if not text:
                text = line
            story.append(Paragraph(
                f'<b>⚗️ Formula/Equation:</b>  {text}',
                styles["Equation"]
            ))

        # === KEY NOTE
        elif line.lower().startswith("**key note") or \
                line.lower().startswith("**important"):
            text = re.sub(
                r'\*\*(key note|important)[:\s]*\*\*', '',
                line, flags=re.IGNORECASE
            ).strip()
            if not text:
                text = line
            story.append(Paragraph(
                f'<b>🔑 Key Note:</b> {text}',
                styles["KeyNote"]
            ))

        # === DIAGRAM / SKETCH NOTE
        elif (line.lower().startswith("**diagram") or
              line.lower().startswith("**sketch") or
              line.lower().startswith("**graph")):
            text = re.sub(
                r'\*\*(diagram|sketch|graph)[:\s]*\*\*', '',
                line, flags=re.IGNORECASE
            ).strip()
            if not text:
                text = line
            story.append(Paragraph(
                f'📊 Diagram/Graph Note: {text}',
                styles["DiagramNote"]
            ))

        # === BULLET POINTS (- or •)
        elif line.startswith("- ") or line.startswith("• "):
            text = line[2:].strip()
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            story.append(Paragraph(
                f'• {text}',
                styles["BulletPoint"]
            ))

        # === NUMBERED POINTS
        elif re.match(r'^\d+[\.\)]\s', line):
            text = re.sub(r'^\d+[\.\)]\s', '', line)
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            num = re.match(r'^(\d+)', line).group(1)
            story.append(Paragraph(
                f'<b>{num}.</b> {text}',
                styles["BulletPoint"]
            ))

        # === BOLD TEXT
        elif "**" in line:
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            story.append(Paragraph(text, styles["Body"]))

        # === REGULAR TEXT
        else:
            if line:
                story.append(Paragraph(line, styles["Body"]))

        i += 1

    return story


# ============================================
# MAIN PDF BUILDER
# ============================================

def generate_pdf(
    content,
    student_name,
    subject,
    topic,
    program,
    year,
    institution,
    doc_type="notes",
    question_text=None,
    marks=None
):
    """Generate a professional PDF and return as bytes"""

    buffer = io.BytesIO()
    styles = get_styles()

    # Page setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.5 * cm,
        title=f"StudyMate AI — {subject} — {topic}",
        author=f"StudyMate AI | {student_name}",
        subject=f"{program} | {institution}"
    )

    story = []
    meta = {
        "student_name": student_name,
        "program": program,
        "year": year,
        "institution": institution
    }

    # ── Header ──
    story.append(build_header(student_name, subject, topic, doc_type))
    story.append(Spacer(1, 6))
    story.append(build_meta_table(meta))
    story.append(Spacer(1, 6))

    # ── Document Title ──
    story.append(Paragraph(
        f'<font color="#1565C0"><b>{"📝 SMART NOTES" if doc_type == "notes" else "✏️ QUESTION SOLUTION"}: {subject.upper()} — {topic.upper()}</b></font>',
        ParagraphStyle(
            "MainTitle", fontSize=13,
            fontName="Helvetica-Bold",
            textColor=PRIMARY, alignment=TA_CENTER,
            spaceAfter=4, spaceBefore=8
        )
    ))

    # ── For question solver — show question ──
    if doc_type == "solution" and question_text:
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "<b>📋 Question:</b>",
            styles["Label"]
        ))
        story.append(Paragraph(
            question_text,
            ParagraphStyle(
                "QText", fontSize=10,
                fontName="Helvetica-Oblique",
                textColor=DARK_TEXT,
                backColor=LIGHT_ORANGE,
                leftIndent=10, rightIndent=10,
                borderPadding=(8, 10, 8, 10),
                spaceAfter=6, leading=16
            )
        ))
        if marks:
            story.append(Paragraph(
                f'<b>📊 Marks Allocated:</b> '
                f'<font color="#1565C0"><b>[{marks} Marks]</b></font>',
                styles["Label"]
            ))

    story.append(HRFlowable(
        width="100%", thickness=1.5,
        color=PRIMARY, spaceAfter=8, spaceBefore=4
    ))

    # ── Main Content ──
    content_elements = parse_and_build_content(content, styles)
    story.extend(content_elements)

    # ── Footer ──
    story.append(Spacer(1, 20))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=DIVIDER, spaceAfter=6
    ))
    story.append(Paragraph(
        f"📚 StudyMate AI  |  Generated for: {student_name}  |  "
        f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}  |  "
        f"Developer: Aftab Ahmed  |  © 2025 StudyMate AI",
        styles["Footer"]
    ))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()