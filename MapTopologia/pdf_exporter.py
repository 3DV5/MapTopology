from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configura estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=16,
            spaceAfter=20,
            alignment=1,  # Center
            textColor=colors.HexColor('#2E86AB')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.HexColor('#2E86AB')
        ))
    
    def export_topology_report(self, devices, company_name="", output_path=""):
        """Gera relatório PDF da topologia de rede"""
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"reports/topology_report_{timestamp}.pdf"
            
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Cria documento
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Título
            title = Paragraph("RELATÓRIO DE TOPOLOGIA DE REDE", self.styles['CustomTitle'])
            story.append(title)
            
            # Informações da empresa
            if company_name:
                company_para = Paragraph(f"<b>Empresa:</b> {company_name}", self.styles['Normal'])
                story.append(company_para)
            
            # Data de geração
            date_para = Paragraph(f"<b>Gerado em:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}", 
                                 self.styles['Normal'])
            story.append(date_para)
            
            story.append(Spacer(1, 20))
            
            # Resumo da rede
            summary = Paragraph("RESUMO DA REDE", self.styles['CustomHeading'])
            story.append(summary)
            
            resumo_text = f"""
            <b>Total de dispositivos encontrados:</b> {len(devices)}<br/>
            <b>Rede escaneada:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>
            <b>Status:</b> Documentação gerada automaticamente pelo MapTopologia
            """
            resumo_para = Paragraph(resumo_text, self.styles['Normal'])
            story.append(resumo_para)
            
            story.append(Spacer(1, 15))
            
            # Tabela de dispositivos
            if devices:
                devices_title = Paragraph("DISPOSITIVOS DE REDE", self.styles['CustomHeading'])
                story.append(devices_title)
                
                device_data = [['IP', 'MAC', 'Hostname', 'Fabricante', 'Status']]
                
                for device in devices:
                    device_data.append([
                        device['ip'],
                        device['mac'],
                        device['hostname'][:20],  # Limita tamanho
                        device['vendor'][:15],    # Limita tamanho
                        device.get('status', 'Online')
                    ])
                
                device_table = Table(device_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.2*inch, 0.8*inch])
                device_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DEE2E6'))
                ]))
                
                story.append(device_table)
            
            # Rodapé
            story.append(Spacer(1, 20))
            footer = Paragraph(
                f"<i>Relatório gerado automaticamente por MapTopologia - {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>",
                ParagraphStyle(name='Footer', fontSize=8, textColor=colors.gray)
            )
            story.append(footer)
            
            # Constrói PDF
            doc.build(story)
            return output_path
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            return None