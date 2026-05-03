from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def write_pdf(text_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=LETTER)
    width, height = LETTER

    left = 0.8 * inch
    top = height - 0.8 * inch
    line_height = 12
    max_width = width - 2 * left

    def draw_lines(lines: list[str]) -> None:
        nonlocal top
        for line in lines:
            words = line.split()
            current = []
            while words:
                current.append(words.pop(0))
                test = " ".join(current + words[:1])
                if c.stringWidth(test, "Times-Roman", 11) > max_width:
                    break
            out_line = " ".join(current)
            c.drawString(left, top, out_line)
            top -= line_height
            if top < 0.8 * inch:
                c.showPage()
                top = height - 0.8 * inch

    lines = text_path.read_text(encoding="utf-8").splitlines()
    for raw in lines:
        if raw.strip() == "":
            top -= line_height
            if top < 0.8 * inch:
                c.showPage()
                top = height - 0.8 * inch
            continue
        draw_lines([raw])

    c.save()


def main() -> None:
    base = Path("submission") / "DataScience_Final_GroupA_TeamGamma"
    mapping = {
        base / "1_Data_Collection" / "consent_form.md": base / "1_Data_Collection" / "consent_form.pdf",
        base / "1_Data_Collection" / "questionnaire.md": base / "1_Data_Collection" / "questionnaire.pdf",
        base / "1_Data_Collection" / "data_collection_report.md": base / "1_Data_Collection" / "data_collection_report.pdf",
        base / "2_Data_Cleaning" / "cleaning_report.md": base / "2_Data_Cleaning" / "cleaning_report.pdf",
        base / "3_EDA" / "eda_summary.md": base / "3_EDA" / "eda_summary.pdf",
        base / "3_EDA" / "key_insights.md": base / "3_EDA" / "key_insights.pdf",
        base / "4_Modeling" / "model_comparison_report.md": base / "4_Modeling" / "model_comparison_report.pdf",
        base / "4_Modeling" / "performance_summary.md": base / "4_Modeling" / "performance_summary.pdf",
        base / "5_Interpretation" / "interpretation_report.md": base / "5_Interpretation" / "interpretation_report.pdf",
        base / "5_Interpretation" / "business_recommendations.md": base / "5_Interpretation" / "business_recommendations.pdf",
        base / "5_Interpretation" / "limitations_ethics.md": base / "5_Interpretation" / "limitations_ethics.pdf",
        base / "6_Presentation" / "Presentation_Slides.md": base / "6_Presentation" / "Presentation_Slides.pdf",
        base / "Project_Report.md": base / "Project_Report.pdf",
    }

    for src, dst in mapping.items():
        if src.exists():
            write_pdf(src, dst)


if __name__ == "__main__":
    main()
