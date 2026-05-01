<<<<<<< HEAD
# ============================================
# StudyMate AI - Professional PDF Generator
# Clean, formal, academic formatting
# ============================================

import io
import re
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether
)


# ============================================
# COLOUR PALETTE — Minimal, professional
# ============================================

NAVY       = HexColor("#1B2A4A")   # Deep navy — headings
DARK_GRAY  = HexColor("#2C2C2C")   # Body text
MID_GRAY   = HexColor("#555555")   # Secondary text
LIGHT_GRAY = HexColor("#888888")   # Captions / meta
RULE_COLOR = HexColor("#CCCCCC")   # Divider lines
ACCENT     = HexColor("#1B2A4A")   # Same as navy for consistency
PAGE_BG    = HexColor("#F9F9F9")   # Not used in ReportLab but kept for ref
BOX_BG     = HexColor("#F4F6F9")   # Very subtle box background
WHITE      = white


# ============================================
# TYPOGRAPHY STYLES
# ============================================

def get_styles():
    """Return a dictionary of named paragraph styles."""

    base = dict(
        fontName="Helvetica",
        textColor=DARK_GRAY,
        leading=18,
        spaceAfter=6,
        spaceBefore=0,
    )

    styles = {

        # ── Document title on cover strip ──
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=WHITE,
            alignment=TA_CENTER,
            leading=26,
            spaceAfter=4,
            spaceBefore=4,
        ),

        "CoverSub": ParagraphStyle(
            "CoverSub",
            fontName="Helvetica",
            fontSize=11,
            textColor=HexColor("#CCDDEE"),
            alignment=TA_CENTER,
            leading=16,
            spaceAfter=2,
        ),

        # ── Document meta strip (program, name, etc.) ──
        "MetaCell": ParagraphStyle(
            "MetaCell",
            fontName="Helvetica",
            fontSize=8,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            leading=12,
        ),

        # ── Section heading  (## in AI output) ──
        "H1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=NAVY,
            leading=18,
            spaceBefore=18,
            spaceAfter=4,
            alignment=TA_LEFT,
        ),

        # ── Sub-heading  (### in AI output) ──
        "H2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=NAVY,
            leading=16,
            spaceBefore=12,
            spaceAfter=3,
            alignment=TA_LEFT,
        ),

        # ── Label for special blocks ──
        "BlockLabel": ParagraphStyle(
            "BlockLabel",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=NAVY,
            leading=13,
            spaceBefore=8,
            spaceAfter=2,
            alignment=TA_LEFT,
        ),

        # ── Body text — justified ──
        "Body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10,
            textColor=DARK_GRAY,
            leading=16,
            spaceBefore=4,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
        ),

        # ── Body text in a shaded box ──
        "BoxBody": ParagraphStyle(
            "BoxBody",
            fontName="Helvetica",
            fontSize=10,
            textColor=DARK_GRAY,
            leading=16,
            spaceBefore=2,
            spaceAfter=2,
            alignment=TA_JUSTIFY,
            leftIndent=6,
            rightIndent=6,
        ),

        # ── Bullet / numbered list item ──
        "Bullet": ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=10,
            textColor=DARK_GRAY,
            leading=15,
            spaceBefore=2,
            spaceAfter=2,
            leftIndent=16,
            bulletIndent=4,
            alignment=TA_LEFT,
        ),

        # ── Equation / formula (monospace feel) ──
        "Equation": ParagraphStyle(
            "Equation",
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=DARK_GRAY,
            leading=16,
            spaceBefore=4,
            spaceAfter=4,
            alignment=TA_CENTER,
            leftIndent=20,
            rightIndent=20,
        ),

        # ── Footer ──
        "Footer": ParagraphStyle(
            "Footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=LIGHT_GRAY,
            alignment=TA_CENTER,
            leading=11,
        ),

        # ── Question block (for solution mode) ──
        "Question": ParagraphStyle(
            "Question",
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=MID_GRAY,
            leading=16,
            spaceBefore=4,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leftIndent=6,
            rightIndent=6,
        ),
    }

    return styles


# ============================================
# HELPER — shaded box using a 1-cell Table
# ============================================

def shaded_box(content_paragraphs, bg=BOX_BG, border=RULE_COLOR):
    """
    Wrap a list of Paragraph objects in a lightly shaded single-cell table.
    This gives the 'definition box' / 'key note box' appearance without
    garish colours.
    """
    inner = Table(
        [[p] for p in content_paragraphs],
        colWidths=[15.5 * cm],
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("BOX",          (0, 0), (-1, -1), 0.5, border),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [bg]),
    ]))
    return inner


# ============================================
# HEADER — cover strip + meta row
# ============================================

def build_cover_strip(doc_type, subject, topic):
    """Dark navy banner at the top of the document."""
    label = "SMART STUDY NOTES" if doc_type == "notes" else "QUESTION SOLUTION"
    title_text  = f"{label}"
    subject_text = f"{subject}  ·  {topic}"

    styles = get_styles()

    data = [[
        Paragraph(title_text,  styles["CoverTitle"]),
    ], [
        Paragraph(subject_text, styles["CoverSub"]),
    ]]

    t = Table(data, colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ROWBACKGROUNDS",(0, 0),(-1,-1),[NAVY]),
    ]))
    return t


def build_meta_row(student_name, program, year, institution):
    """Single-row table with student details below the cover strip."""
    styles = get_styles()
    cells = [
        Paragraph(f"<b>Student</b><br/>{student_name}", styles["MetaCell"]),
        Paragraph(f"<b>Program</b><br/>{program}",       styles["MetaCell"]),
        Paragraph(f"<b>Year / Semester</b><br/>{year}",  styles["MetaCell"]),
        Paragraph(f"<b>Institution</b><br/>{institution}",styles["MetaCell"]),
        Paragraph(
            f"<b>Date</b><br/>{datetime.now().strftime('%d %b %Y')}",
            styles["MetaCell"]
        ),
    ]
    t = Table([cells], colWidths=[3.4 * cm] * 5)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#EEF2F7")),
        ("BOX",           (0, 0), (-1, -1), 0.5, RULE_COLOR),
        ("INNERGRID",     (0, 0), (-1, -1), 0.3, RULE_COLOR),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


# ============================================
# CONTENT PARSER
# ============================================

def parse_content(ai_text, styles):
    """
    Convert AI-generated markdown-style text into a list of
    ReportLab flowable objects with clean, professional formatting.
    """
    story = []
    lines = ai_text.split("\n")
    i = 0

    def clean(text):
        """Remove markdown bold markers and strip whitespace."""
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"\*(.*?)\*",     r"<i>\1</i>", text)
        return text.strip()

    def rule():
        return HRFlowable(
            width="100%", thickness=0.5,
            color=RULE_COLOR, spaceAfter=4, spaceBefore=4
        )

    while i < len(lines):
        raw  = lines[i]
        line = raw.strip()

        # ── Skip blank / separator lines ──
        if not line or line in ("---", "***", "___"):
            story.append(Spacer(1, 4))
            i += 1
            continue

        # ── Main heading  ## ──
        if line.startswith("## "):
            text = clean(line[3:])
            story.append(Spacer(1, 6))
            story.append(Paragraph(text.upper(), styles["H1"]))
            story.append(rule())

        # ── Sub-heading  ### ──
        elif line.startswith("### "):
            text = clean(line[4:])
            story.append(Spacer(1, 4))
            story.append(Paragraph(text, styles["H2"]))

        # ── Definition ──
        elif re.match(r"\*\*definition[:\s]", line, re.I) or \
             line.lower().startswith("definition:"):
            body = re.sub(
                r"\*\*definition[:\s]*\*\*", "", line, flags=re.I
            ).strip()
            body = clean(body) or clean(line)
            story.append(Spacer(1, 4))
            story.append(Paragraph("Definition", styles["BlockLabel"]))
            story.append(shaded_box([
                Paragraph(body, styles["BoxBody"])
            ]))

        # ── Explanation ──
        elif re.match(r"\*\*explanation[:\s]", line, re.I) or \
             line.lower().startswith("explanation:"):
            body = re.sub(
                r"\*\*explanation[:\s]*\*\*", "", line, flags=re.I
            ).strip()
            body = clean(body) or clean(line)
            story.append(Paragraph(body, styles["Body"]))

        # ── Example ──
        elif re.match(r"\*\*example[:\s]", line, re.I) or \
             line.lower().startswith("example:"):
            body = re.sub(
                r"\*\*example[:\s]*\*\*", "", line, flags=re.I
            ).strip()
            body = clean(body) or clean(line)
            story.append(Spacer(1, 2))
            story.append(Paragraph("Example", styles["BlockLabel"]))
            story.append(Paragraph(body, styles["Body"]))

        # ── Equation / Formula ──
        elif re.match(r"\*\*(equation|formula)[:\s]", line, re.I) or \
             line.lower().startswith("equation:") or \
             line.lower().startswith("formula:"):
            body = re.sub(
                r"\*\*(equation|formula)[:\s]*\*\*", "",
                line, flags=re.I
            ).strip()
            body = clean(body) or clean(line)
            story.append(Spacer(1, 2))
            story.append(Paragraph("Formula / Equation", styles["BlockLabel"]))
            story.append(shaded_box([
                Paragraph(body, styles["Equation"])
            ], bg=HexColor("#F0F0F8")))

        # ── Key Note / Important ──
        elif re.match(r"\*\*(key note|important)[:\s]", line, re.I) or \
             line.lower().startswith("key note:"):
            body = re.sub(
                r"\*\*(key note|important)[:\s]*\*\*", "",
                line, flags=re.I
            ).strip()
            body = clean(body) or clean(line)
            story.append(Spacer(1, 2))
            story.append(Paragraph("Key Note", styles["BlockLabel"]))
            story.append(shaded_box([
                Paragraph(body, styles["BoxBody"])
            ], bg=HexColor("#F4F4F4")))

        # ── Diagram / Sketch / Graph note ──
        elif re.match(r"\*\*(diagram|sketch|graph)[:\s]", line, re.I):
            body = re.sub(
                r"\*\*(diagram|sketch|graph)[:\s]*\*\*", "",
                line, flags=re.I
            ).strip()
            body = clean(body) or clean(line)
            story.append(Spacer(1, 2))
            story.append(Paragraph(
                "Diagram / Sketch Note", styles["BlockLabel"]
            ))
            story.append(Paragraph(
                f"[ {body} ]",
                ParagraphStyle(
                    "DiagNote",
                    parent=styles["BoxBody"],
                    fontName="Helvetica-Oblique",
                    textColor=MID_GRAY,
                    alignment=TA_CENTER,
                )
            ))

        # ── Bullet point  (- or •) ──
        elif re.match(r"^[-•]\s", line):
            text = clean(line[2:])
            story.append(Paragraph(f"•  {text}", styles["Bullet"]))

        # ── Numbered list ──
        elif re.match(r"^\d+[.\)]\s", line):
            num  = re.match(r"^(\d+)", line).group(1)
            text = re.sub(r"^\d+[.\)]\s*", "", line)
            text = clean(text)
            story.append(Paragraph(
                f"<b>{num}.</b>  {text}", styles["Bullet"]
            ))

        # ── Inline bold-only line ──
        elif "**" in line:
            story.append(Paragraph(clean(line), styles["Body"]))

        # ── Plain body text ──
        else:
            if line:
                story.append(Paragraph(clean(line), styles["Body"]))

        i += 1

    return story


# ============================================
# FOOTER CANVAS
# ============================================

class FooterCanvas:
    """
    Mixin to add page numbers and footer text on every page.
    Used via SimpleDocTemplate's onFirstPage / onLaterPages callbacks.
    """
    def __init__(self, student_name, subject, topic):
        self.student_name = student_name
        self.subject      = subject
        self.topic        = topic

    def __call__(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(LIGHT_GRAY)

        footer_left  = f"StudyMate AI  |  {self.student_name}"
        footer_right = f"Page {doc.page}"
        footer_mid   = f"{self.subject} — {self.topic}"

        w = A4[0]
        y = 1.2 * cm

        canvas.drawString(1.8 * cm, y, footer_left)
        canvas.drawCentredString(w / 2, y, footer_mid)
        canvas.drawRightString(w - 1.8 * cm, y, footer_right)

        # thin top rule above footer
        canvas.setStrokeColor(RULE_COLOR)
        canvas.setLineWidth(0.5)
        canvas.line(1.8 * cm, y + 0.45 * cm, w - 1.8 * cm, y + 0.45 * cm)

        canvas.restoreState()


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
    marks=None,
):
    """
    Build a professional A4 PDF document and return its bytes.

    Parameters
    ----------
    content        : str   — AI-generated markdown-style text
    student_name   : str
    subject        : str
    topic          : str
    program        : str
    year           : str
    institution    : str
    doc_type       : 'notes' | 'solution'
    question_text  : str | None — only for solution mode
    marks          : int | None — only for solution mode
    """

    buffer = io.BytesIO()
    styles = get_styles()

    footer_cb = FooterCanvas(student_name, subject, topic)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=2.2 * cm,
        title=f"StudyMate AI — {subject} — {topic}",
        author=f"StudyMate AI | {student_name}",
        subject=f"{program} | {institution}",
    )

    story = []

    # ── 1. Cover strip ──
    story.append(build_cover_strip(doc_type, subject, topic))
    story.append(Spacer(1, 4))

    # ── 2. Meta row ──
    story.append(build_meta_row(student_name, program, year, institution))
    story.append(Spacer(1, 10))

    # ── 3. Question block (solution mode only) ──
    if doc_type == "solution" and question_text:
        story.append(Paragraph("Question", styles["BlockLabel"]))
        story.append(shaded_box([
            Paragraph(question_text, styles["Question"])
        ], bg=HexColor("#F4F6F9")))

        if marks:
            story.append(Paragraph(
                f"Marks Allocated:  <b>{marks}</b>",
                ParagraphStyle(
                    "MarksLine",
                    parent=styles["Body"],
                    spaceBefore=4,
                    spaceAfter=8,
                )
            ))

        story.append(HRFlowable(
            width="100%", thickness=1,
            color=NAVY, spaceBefore=6, spaceAfter=10
        ))

    # ── 4. Main content ──
    content_elements = parse_content(content, styles)
    story.extend(content_elements)

    # ── 5. Footer note ──
    story.append(Spacer(1, 16))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=RULE_COLOR, spaceAfter=6
    ))
    story.append(Paragraph(
        f"Generated by StudyMate AI  ·  {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
        f"  ·  Developer: Aftab Ahmed  ·  © 2025 StudyMate AI",
        styles["Footer"]
    ))

    # ── Build ──
    doc.build(
        story,
        onFirstPage=footer_cb,
        onLaterPages=footer_cb,
    )

    buffer.seek(0)
=======
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
>>>>>>> b09323630fd2f2924f4f0231828396c7cbd43d21
    return buffer.getvalue()