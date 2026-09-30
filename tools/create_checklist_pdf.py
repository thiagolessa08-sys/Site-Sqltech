from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "sqltech-checklist-primeiro-processo-ia.pdf"
LOGO = ROOT / "assets" / "logo-branco.png"

NAVY = colors.HexColor("#07182D")
BLUE = colors.HexColor("#1668D8")
CYAN = colors.HexColor("#48A7FF")
INK = colors.HexColor("#14243D")
MUTED = colors.HexColor("#607086")
PALE = colors.HexColor("#EEF5FD")
LINE = colors.HexColor("#D8E4F2")
WHITE = colors.white


def register_fonts():
    regular = Path(r"C:\Windows\Fonts\arial.ttf")
    bold = Path(r"C:\Windows\Fonts\arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("SQLTechSans", str(regular)))
        pdfmetrics.registerFont(TTFont("SQLTechSans-Bold", str(bold)))
        return "SQLTechSans", "SQLTechSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


class CheckBox(Flowable):
    def __init__(self, size=4.2 * mm, stroke=BLUE):
        super().__init__()
        self.width = size
        self.height = size
        self.stroke = stroke

    def draw(self):
        self.canv.setStrokeColor(self.stroke)
        self.canv.setLineWidth(1.1)
        self.canv.roundRect(0, 0, self.width, self.height, 1.2 * mm, stroke=1, fill=0)


class WriteLines(Flowable):
    def __init__(self, width, rows=2, spacing=7 * mm):
        super().__init__()
        self.width = width
        self.rows = rows
        self.spacing = spacing
        self.height = rows * spacing

    def draw(self):
        self.canv.setStrokeColor(LINE)
        self.canv.setLineWidth(0.7)
        for i in range(self.rows):
            y = self.height - (i + 0.75) * self.spacing
            self.canv.line(0, y, self.width, y)


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", fontName=FONT_BOLD, fontSize=26, leading=30,
    textColor=WHITE, alignment=TA_LEFT, spaceAfter=8 * mm,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName=FONT, fontSize=12, leading=18,
    textColor=colors.HexColor("#C7DAEF"), alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="Eyebrow", fontName=FONT_BOLD, fontSize=8.5, leading=11,
    textColor=BLUE, spaceAfter=3 * mm, tracking=1.8,
))
styles.add(ParagraphStyle(
    name="H1SQL", fontName=FONT_BOLD, fontSize=22, leading=26,
    textColor=INK, spaceAfter=5 * mm,
))
styles.add(ParagraphStyle(
    name="H2SQL", fontName=FONT_BOLD, fontSize=14, leading=17,
    textColor=INK, spaceBefore=2 * mm, spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name="BodySQL", fontName=FONT, fontSize=9.5, leading=14,
    textColor=MUTED, spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name="BodyStrong", fontName=FONT_BOLD, fontSize=9.5, leading=14,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableHeader", fontName=FONT_BOLD, fontSize=9.5, leading=14,
    textColor=WHITE,
))
styles.add(ParagraphStyle(
    name="Question", fontName=FONT, fontSize=9.4, leading=13.3,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="Small", fontName=FONT, fontSize=7.7, leading=11,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="Callout", fontName=FONT_BOLD, fontSize=11, leading=15,
    textColor=INK,
))


def page_footer(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 10.2 * mm, "SQLTech | Dados, BI, Process Mining e IA aplicada")
    canvas.drawRightString(A4[0] - 18 * mm, 10.2 * mm, f"{page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.circle(A4[0] + 18 * mm, A4[1] - 78 * mm, 76 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.13))
    canvas.setLineWidth(0.5)
    for i in range(9):
        y = 36 * mm + i * 20 * mm
        canvas.line(0, y, A4[0], y + 36 * mm)
    if LOGO.exists():
        canvas.drawImage(str(LOGO), 20 * mm, A4[1] - 40 * mm, width=48 * mm, height=11.5 * mm,
                         preserveAspectRatio=True, mask="auto")
    canvas.setFont(FONT_BOLD, 8.5)
    canvas.setFillColor(CYAN)
    canvas.drawString(20 * mm, A4[1] - 65 * mm, "GUIA PRÁTICO PARA GESTORES")
    canvas.setFont(FONT_BOLD, 27)
    canvas.setFillColor(WHITE)
    title = ["Antes de automatizar:", "12 perguntas para escolher", "seu primeiro processo de IA"]
    y = A4[1] - 84 * mm
    for line in title:
        canvas.drawString(20 * mm, y, line)
        y -= 11.5 * mm
    canvas.setFont(FONT, 11)
    canvas.setFillColor(colors.HexColor("#C7DAEF"))
    canvas.drawString(20 * mm, y - 4 * mm, "Um roteiro para delimitar o problema, preparar os dados")
    canvas.drawString(20 * mm, y - 10 * mm, "e definir como o resultado será medido.")
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.08))
    canvas.roundRect(20 * mm, 33 * mm, 170 * mm, 32 * mm, 4 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FONT_BOLD, 10)
    canvas.drawString(28 * mm, 54 * mm, "Use este material em uma conversa de 30 minutos.")
    canvas.setFont(FONT, 8.5)
    canvas.setFillColor(colors.HexColor("#C7DAEF"))
    canvas.drawString(28 * mm, 46.5 * mm, "Escolha um processo específico e responda com exemplos reais da operação.")
    canvas.drawString(28 * mm, 40 * mm, "O roteiro orienta a avaliação; ele não garante retorno nem substitui validação técnica.")
    canvas.setFont(FONT_BOLD, 8)
    canvas.setFillColor(CYAN)
    canvas.drawString(20 * mm, 20 * mm, "SQLTECH.COM.BR  |  DESDE 1998")
    canvas.restoreState()


def section_header(number, title, subtitle=None):
    items = [Paragraph(f"ETAPA {number}", styles["Eyebrow"]), Paragraph(title, styles["H1SQL"])]
    if subtitle:
        items.append(Paragraph(subtitle, styles["BodySQL"]))
    return items


def question(number, text, note=None):
    body = [Paragraph(f"<b>{number}.</b> {text}", styles["Question"])]
    if note:
        body.append(Spacer(1, 1.4 * mm))
        body.append(Paragraph(note, styles["Small"]))
    table = Table([[CheckBox(), body]], colWidths=[7 * mm, 158 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return KeepTogether([table, Spacer(1, 2.2 * mm)])


def callout(title, text):
    table = Table([
        [Paragraph(title, styles["Callout"])],
        [Paragraph(text, styles["BodySQL"])],
    ], colWidths=[165 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#C9DCF4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6 * mm),
        ("TOPPADDING", (0, 0), (-1, 0), 5 * mm),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 4 * mm),
    ]))
    return table


def field_row(label, lines=1):
    return KeepTogether([
        Paragraph(label, styles["BodyStrong"]),
        WriteLines(165 * mm, rows=lines, spacing=6.7 * mm),
        Spacer(1, 1.8 * mm),
    ])


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=22 * mm, rightMargin=22 * mm,
        topMargin=22 * mm, bottomMargin=22 * mm,
        title="Antes de automatizar: 12 perguntas para escolher seu primeiro processo de IA",
        author="SQLTech Consultoria",
        subject="Checklist para avaliação inicial de processos com IA",
    )

    story = [Spacer(1, 235 * mm), PageBreak()]

    story += section_header("01", "Comece por um processo, não por uma tecnologia",
                            "Escolha uma rotina concreta. Use volume, tempo, erros e exceções para explicar o que acontece hoje.")
    story += [
        callout("Como usar o checklist", "Reúna operação, área de negócio e TI. Responda às perguntas com exemplos. Quando algo não estiver disponível, registre quem pode levantar a informação e qual será o próximo passo."),
        Spacer(1, 7 * mm),
        Paragraph("Três sinais de que vale avançar", styles["H2SQL"]),
    ]
    signals = [
        ("1", "Problema delimitado", "A atividade é repetitiva, relevante e tem um responsável claro."),
        ("2", "Dados acessíveis", "Há sistemas, documentos ou mensagens que representem casos comuns e exceções."),
        ("3", "Resultado mensurável", "A equipe consegue comparar tempo, retrabalho, qualidade ou cumprimento de prazo."),
    ]
    signal_table = Table([
        [Paragraph(f"<b>{n}</b>", styles["H2SQL"]), Paragraph(f"<b>{t}</b><br/>{d}", styles["BodySQL"])]
        for n, t, d in signals
    ], colWidths=[15 * mm, 150 * mm])
    signal_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLUE),
        ("TEXTCOLOR", (0, 0), (0, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5 * mm),
    ]))
    story += [signal_table, Spacer(1, 8 * mm), Paragraph("Processo escolhido para esta avaliação", styles["H2SQL"]), WriteLines(165 * mm, 3), PageBreak()]

    story += section_header("02", "O problema e os dados", "As primeiras seis perguntas ajudam a dimensionar a rotina e localizar a informação necessária.")
    story += [
        Paragraph("O problema", styles["H2SQL"]),
        question(1, "Qual atividade se repete e por que ela é necessária?", "Descreva a tarefa, quem executa e qual resultado ela produz."),
        question(2, "Quantos casos chegam por semana ou por mês?", "Use uma média e registre picos ou sazonalidades conhecidas."),
        question(3, "Quanto tempo de trabalho ativo cada caso exige?", "Separe o tempo de execução da espera entre etapas."),
        Spacer(1, 3 * mm),
        Paragraph("Os dados", styles["H2SQL"]),
        question(4, "Onde estão as informações de entrada: sistema, documento, mensagem ou planilha?"),
        question(5, "Existe uma amostra que inclua casos comuns, incompletos e excepcionais?"),
        question(6, "Quem pode autorizar o acesso e quais informações cada participante deve visualizar?"),
        PageBreak(),
    ]

    story += section_header("03", "Regras, exceções e operação", "O piloto precisa saber quando agir, quando pedir revisão e como registrar o resultado.")
    story += [
        Paragraph("As regras e exceções", styles["H2SQL"]),
        question(7, "Quais regras são objetivas e quais exigem julgamento?"),
        question(8, "O que acontece quando a informação falta, está incorreta ou a resposta é incerta?"),
        question(9, "Quem revisa as exceções e quem assume a decisão final?"),
        Spacer(1, 3 * mm),
        Paragraph("A operação e a medida de sucesso", styles["H2SQL"]),
        question(10, "O resultado precisa apenas ser apresentado ou também registrado em outro sistema?"),
        question(11, "Qual métrica será comparada antes e depois: tempo ativo, tempo total, retrabalho, qualidade ou cumprimento do prazo?"),
        question(12, "Quem acompanha o piloto e decide se ele pode avançar, precisa de ajuste ou deve ser interrompido?"),
        PageBreak(),
    ]

    story += section_header("04", "Interprete o resultado", "O checklist indica qual preparação vem antes de um piloto.")
    interpretation = [
        [Paragraph("Se falta...", styles["TableHeader"]), Paragraph("Próximo passo", styles["TableHeader"])],
        [Paragraph("Problema delimitado, responsável ou métrica", styles["BodySQL"]), Paragraph("Definir o processo e o resultado esperado.", styles["BodySQL"])],
        [Paragraph("Dados, exemplos ou exceções", styles["BodySQL"]), Paragraph("Preparar a amostra e as regras de validação.", styles["BodySQL"])],
        [Paragraph("Integração e responsabilidade operacional", styles["BodySQL"]), Paragraph("Mapear sistemas, acessos e quem revisará o resultado.", styles["BodySQL"])],
        [Paragraph("Nada disso", styles["BodySQL"]), Paragraph("Discutir um piloto de escopo limitado.", styles["BodySQL"])],
    ]
    interp_table = Table(interpretation, colWidths=[72 * mm, 93 * mm], repeatRows=1)
    interp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    story += [
        interp_table,
        Spacer(1, 8 * mm),
        Paragraph("Exercício de dimensionamento", styles["H2SQL"]),
        callout("Volume mensal x minutos de trabalho ativo por caso / 60", "Exemplo ilustrativo: 1.200 casos x 8 minutos / 60 = 160 horas mensais de trabalho ativo. Essa carga atual não é uma economia prevista. A estimativa de ganho precisa considerar revisão humana, exceções, operação e manutenção."),
        Spacer(1, 8 * mm),
        field_row("Volume mensal aproximado"),
        field_row("Minutos de trabalho ativo por caso"),
        field_row("Horas mensais estimadas"),
        field_row("Métrica que será comparada antes e depois", 2),
        PageBreak(),
    ]

    story += section_header("05", "Ficha do primeiro processo", "Leve esta página para a conversa com a equipe responsável pela operação.")
    story += [
        field_row("Processo a avaliar", 2),
        field_row("Área responsável"),
        field_row("Volume aproximado"),
        field_row("Entrada e sistema de origem"),
        field_row("Principal dificuldade", 2),
        field_row("Exceção mais comum", 2),
        field_row("Métrica atual"),
        field_row("Resultado desejado", 2),
        field_row("Pessoas necessárias para validar"),
        field_row("Próximo passo", 2),
        Spacer(1, 4 * mm),
        callout("Quer discutir a viabilidade do seu processo?", "Entre em contato com a SQLTech e informe \"Avaliação de processo com IA\", a área envolvida e a principal dificuldade. www.sqltech.com.br | contato@sqltech.com.br | +55 11 3437-7070"),
    ]

    doc.build(story, onFirstPage=cover_page, onLaterPages=page_footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
