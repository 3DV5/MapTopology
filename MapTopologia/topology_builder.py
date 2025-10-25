import matplotlib
# Backend não-interativo - DEVE vir primeiro
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import networkx as nx
from PIL import Image, ImageDraw, ImageTk, ImageFont
import io
import math

class TopologyBuilder:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_topology(self, devices):
        """Gera visualização da topologia de rede (thread-safe)"""
        try:
            # Limpa grafo anterior
            self.graph.clear()
            
            # Adiciona dispositivos como nós
            for device in devices:
                node_label = f"{device['ip']}\n{device['hostname']}"
                self.graph.add_node(
                    device['ip'],
                    label=node_label,
                    mac=device['mac'],
                    vendor=device['vendor']
                )
            
            # Simula conexões
            self._create_connections(devices)
            
            # Gera imagem
            return self._generate_topology_image()
            
        except Exception as e:
            print(f"Erro ao gerar topologia matplotlib: {e}")
            # Fallback para método simples
            return self.build_simple_topology(devices)
    
    def _create_connections(self, devices):
        """Cria conexões entre dispositivos"""
        if len(devices) > 1:
            for i in range(len(devices) - 1):
                self.graph.add_edge(devices[i]['ip'], devices[i + 1]['ip'])
    
    def _generate_topology_image(self):
        """Gera imagem da topologia usando matplotlib"""
        if len(self.graph.nodes) == 0:
            return None
            
        try:
            # Cria figura
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Layout do grafo
            pos = nx.spring_layout(self.graph, k=3, iterations=50)
            
            # Desenha nós e arestas
            nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                                  node_size=1500, alpha=0.9, edgecolors='black')
            nx.draw_networkx_edges(self.graph, pos, alpha=0.6, width=2, edge_color='gray')
            
            # Labels
            labels = {node: data.get('label', node) for node, data in self.graph.nodes(data=True)}
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, font_weight='bold')
            
            ax.set_title("Topologia de Rede - MapTopologia", fontsize=14, pad=20)
            ax.axis('off')
            plt.tight_layout()
            
            # Converte para ImageTk
            return self._figure_to_tk_image(fig)
            
        except Exception as e:
            print(f"Erro ao gerar imagem matplotlib: {e}")
            return None
    
    def _figure_to_tk_image(self, fig):
        """Converte figura matplotlib para ImageTk"""
        try:
            canvas = FigureCanvasAgg(fig)
            buf = io.BytesIO()
            canvas.print_png(buf)
            buf.seek(0)
            pil_image = Image.open(buf)
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Fecha a figura
            plt.close(fig)
            
            return tk_image
        except Exception as e:
            print(f"Erro ao converter imagem: {e}")
            plt.close(fig)
            return None

    def build_simple_topology(self, devices):
        """Método alternativo simples sem matplotlib"""
        try:
            if not devices:
                return None
            
            # Cria imagem com Pillow
            width, height = 800, 500
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Tenta carregar fontes
            try:
                font_large = ImageFont.truetype("arial.ttf", 20)
                font_small = ImageFont.truetype("arial.ttf", 10)
            except:
                # Fallback para fonte padrão
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Título
            draw.text((width//2 - 100, 20), "Topologia de Rede - MapTopologia", 
                     fill='black', font=font_large)
            
            # Calcula layout
            positions = self._calculate_layout(devices, width, height)
            
            # Desenha conexões
            self._draw_connections(draw, positions)
            
            # Desenha dispositivos
            self._draw_devices(draw, positions, font_small)
            
            # Converte para ImageTk
            return ImageTk.PhotoImage(image)
            
        except Exception as e:
            print(f"Erro ao gerar topologia simples: {e}")
            return self._create_fallback_image()
    
    def _calculate_layout(self, devices, width, height):
        """Calcula posições dos dispositivos"""
        positions = []
        num_devices = len(devices)
        
        if num_devices == 0:
            return positions
            
        # Calcula grid
        cols = min(3, num_devices)
        rows = (num_devices + cols - 1) // cols
        
        for i, device in enumerate(devices):
            row = i // cols
            col = i % cols
            
            # Calcula posição com margens
            margin_x = 100
            margin_y = 80
            spacing_x = (width - 2 * margin_x) // max(1, cols - 1)
            spacing_y = (height - 2 * margin_y) // max(1, rows - 1)
            
            x = margin_x + col * spacing_x
            y = margin_y + row * spacing_y
            
            positions.append((x, y, device))
        
        return positions
    
    def _draw_connections(self, draw, positions):
        """Desenha conexões entre dispositivos"""
        for i in range(len(positions) - 1):
            x1, y1, device1 = positions[i]
            x2, y2, device2 = positions[i + 1]
            
            # Linha
            draw.line([x1 + 40, y1, x2 - 40, y2], fill='#666666', width=2)
    
    def _draw_devices(self, draw, positions, font):
        """Desenha os dispositivos"""
        for x, y, device in positions:
            # Retângulo do dispositivo
            draw.rectangle([x-40, y-25, x+40, y+25], 
                          fill='#E3F2FD', outline='#1976D2', width=2)
            
            # IP
            ip_text = device['ip']
            if len(ip_text) > 15:
                ip_text = device['ip'][:12] + "..."
            draw.text((x-38, y-20), ip_text, fill='#000000', font=font)
            
            # Hostname
            hostname = device['hostname']
            if len(hostname) > 12:
                hostname = hostname[:9] + "..."
            draw.text((x-38, y-5), hostname, fill='#666666', font=font)
            
            # Fabricante
            vendor = device['vendor'][:10] + "..." if len(device['vendor']) > 10 else device['vendor']
            draw.text((x-38, y+10), vendor, fill='#666666', font=font)
    
    def _create_fallback_image(self):
        """Cria imagem de fallback em caso de erro"""
        try:
            image = Image.new('RGB', (400, 200), color='white')
            draw = ImageDraw.Draw(image)
            draw.text((50, 80), "Erro ao gerar topologia", fill='red')
            draw.text((50, 100), "Use os dados da tabela", fill='black')
            return ImageTk.PhotoImage(image)
        except:
            return None