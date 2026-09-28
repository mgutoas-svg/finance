from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
from typing import Dict, List, Any
import tempfile
import os


class ReportGenerator:
    """Gera relatórios em PDF"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()

    def _add_custom_styles(self):
        """Adiciona estilos customizados"""

        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=1  # center
        ))

        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12
        ))

        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.white,
            alignment=0,
            bold=True
        ))

    def generate_report(
        self,
        user_name: str,
        period_start: datetime,
        period_end: datetime,
        total_income: float,
        total_expense: float,
        net_result: float,
        category_totals: Dict[int, float],
        category_map: Dict[int, str],
        goals: List[Any],
        include_recommendations: bool = True
    ) -> str:
        """Gera relatório PDF"""

        # Criar arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()

        # Criar documento
        doc = SimpleDocTemplate(temp_path, pagesize=A4)
        story = []

        # Título
        title = Paragraph(
            f"Relatório Financeiro Pessoal",
            self.styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 0.2*inch))

        # Informações do período
        period_text = f"Período: {period_start.strftime('%d/%m/%Y')} a {period_end.strftime('%d/%m/%Y')}"
        story.append(Paragraph(period_text, self.styles['Normal']))
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # Resumo Financeiro
        story.append(Paragraph("Resumo Financeiro", self.styles['SectionTitle']))

        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de Receitas', f'R$ {total_income:,.2f}'],
            ['Total de Despesas', f'R$ {total_expense:,.2f}'],
            ['Resultado Líquido', f'R$ {net_result:,.2f}'],
        ]

        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ]))

        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))

        # Análise por Categoria
        if category_totals:
            story.append(Paragraph("Análise por Categoria", self.styles['SectionTitle']))

            category_data = [['Categoria', 'Total', 'Percentual']]
            total_expenses = sum(category_totals.values())

            for cat_id, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                category_name = category_map.get(cat_id, "Sem categoria")
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                category_data.append([
                    category_name,
                    f'R$ {amount:,.2f}',
                    f'{percentage:.1f}%'
                ])

            category_table = Table(category_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            category_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
            ]))

            story.append(category_table)
            story.append(Spacer(1, 0.3*inch))

        # Metas
        if goals:
            story.append(Paragraph("Metas Financeiras", self.styles['SectionTitle']))

            goals_data = [['Meta', 'Alvo', 'Progresso', 'Status']]

            for goal in goals:
                progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
                goals_data.append([
                    goal.title[:20],
                    f'R$ {goal.target_amount:,.2f}',
                    f'{progress:.1f}%',
                    goal.status
                ])

            goals_table = Table(goals_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            goals_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
            ]))

            story.append(goals_table)
            story.append(Spacer(1, 0.3*inch))

        # Recomendações
        if include_recommendations:
            story.append(Paragraph("Recomendações", self.styles['SectionTitle']))

            # Gerar recomendações simples
            recommendations_text = """
            <b>• Controlar categorias com maior gasto:</b> Revise categorias que ultrapassaram 20% do total de despesas.<br/><br/>
            <b>• Manter foco nas metas:</b> Acompanhe regularmente o progresso de suas metas financeiras.<br/><br/>
            <b>• Diversificar receitas:</b> Considere novas formas de aumentar sua renda.<br/><br/>
            <b>• Revisar mensalmente:</b> Analise seu relatório financeiro mensalmente para manter controle.
            """

            story.append(Paragraph(recommendations_text, self.styles['Normal']))

        # Rodapé
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "Este relatório contém informações financeiras consolidadas e não contém dados pessoais sensíveis.",
            self.styles['Normal']
        ))

        # Gerar PDF
        doc.build(story)

        return temp_path
