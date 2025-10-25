# MapTopology
MapTopologia - Sistema Completo de Mapeamento de Topologia de Rede
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/GUI-CustomTkinter-green
https://img.shields.io/badge/Network-Scanner-orange
https://img.shields.io/badge/License-MIT-yellow

🌐 Visão Geral
O MapTopologia é uma aplicação desktop avançada desenvolvida em Python para descoberta, mapeamento e documentação completa de redes de computadores. Com uma interface moderna e intuitiva, esta ferramenta permite que administradores de rede, profissionais de TI e entusiastas visualizem e documentem a infraestrutura de rede de maneira eficiente e profissional.

🎯 Destaques Principais
Varredura Inteligente de dispositivos de rede

Visualização Gráfica da topologia da rede

Sistema de Autenticação seguro com múltiplos níveis de acesso

Relatórios Profissionais em PDF

Interface Moderna com CustomTkinter

🚀 Funcionalidades Principais
🔍 Varredura Avançada de Rede
Descoberta Automática de dispositivos ativos na rede

Detecção ARP para identificação precisa de hosts

Coleta de Informações completas:

Endereço IP e MAC

Nome do host (hostname)

Fabricante do equipamento

Status de conectividade

Varredura em Threads sem travar a interface

🌐 Topologia Visual Interativa
Mapa Gráfico Automático da estrutura da rede

Layout Inteligente de dispositivos e conexões

Visualização Hierárquica da infraestrutura

Identificação Visual de diferentes tipos de equipamentos

📊 Sistema de Relatórios Profissionais
Exportação para PDF com layout corporativo

Relatórios Detalhados incluindo:

Lista completa de dispositivos

Informações técnicas detalhadas

Metadados da varredura

Timestamp e informações do usuário

Histórico de Varreduras com persistência em banco de dados

🔐 Sistema de Autenticação Seguro
Multi-nível de Acesso (Admin/Usuário)

Cadastro Seguro de usuários

Gestão de Permissões granular

Sessões Protegidas com logout automático

Criptografia de credenciais

⚙️ Configurações e Personalização
Faixas de Rede Customizáveis

Interface Temática (Light Mode)

Preferências Persistidas

Configurações de Varredura ajustáveis

🛠 Tecnologias Utilizadas
Linguagem e Framework
Python 3.8+ - Linguagem principal

CustomTkinter - Interface gráfica moderna

Tkinter - Base para componentes GUI

Bibliotecas Principais
Scapy - Manipulação de pacotes e varredura ARP

ReportLab - Geração de relatórios PDF

Pillow (PIL) - Processamento de imagens

Threading - Operações assíncronas

Armazenamento e Segurança
SQLite - Banco de dados embutido

SHA-256 - Criptografia de senhas

ARP Protocol - Descoberta de dispositivos

📁 Estrutura do Projeto
text
MapTopologia/
├── 📱 main.py                 # Classe principal da aplicação
├── ⚙️ config.py               # Configurações e constantes
├── 🔍 network_scanner.py      # Módulo de varredura de rede
├── 🌐 topology_builder.py     # Gerador de topologia visual
├── 📄 pdf_exporter.py         # Exportador de relatórios PDF
├── 🔐 auth_manager.py         # Gerenciador de autenticação
├── 🗃️ database.py             # Gerenciador do banco de dados
├── 👤 login_window.py         # Janela de login
├── 📝 register_window.py      # Janela de cadastro
└── 👥 user_manager.py         # Gerenciador de usuários
🖥️ Interface do Usuário
Tela de Login Segura
Interface moderna e limpa

Validação em tempo real

Links para cadastro e recuperação

Dashboard Principal
Barra Lateral Navegacional com ícones intuitivos

Área de Conteúdo Dinâmica que se adapta a cada funcionalidade

Status do Sistema em tempo real

Informações do Usuário logado

Abas Especializadas
🔍 Varredura de Rede

Controles de varredura

Tabela de resultados em tempo real

Status de progresso

🌐 Topologia Visual

Canvas interativo

Botões de geração e exportação

Visualização gráfica da rede

📊 Relatórios

Pré-visualização de relatórios

Controles de exportação PDF

Histórico de documentação

⚙️ Configurações

Personalização de faixas de rede

Configurações de aplicação

Preferências do usuário

🔧 Instalação e Execução
Pré-requisitos
Python 3.8 ou superior

Pip (gerenciador de pacotes do Python)

Acesso administrativo para varreduras de rede

Instalação Passo a Passo
Clone o repositório

bash
git clone https://github.com/3DV5/MapTopology.git
cd MapTopologia
Crie um ambiente virtual (recomendado)

bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
Instale as dependências

bash
pip install -r requirements.txt
Execute a aplicação

bash
python main.py
Dependências Principais
python
customtkinter>=5.2.0
Pillow>=10.0.0
scapy>=2.5.0
reportlab>=4.0.0

🎮 Como Usar
Primeiro Acesso
Execute o aplicativo

Cadastre-se como primeiro usuário (será automaticamente admin)

Faça login com suas credenciais

Realizando uma Varredura
Navegue até 🔍 Varredura de Rede

Insira a faixa de rede (ex: 192.168.1.0/24)

Clique em "Iniciar Varredura"

Aguarde a descoberta dos dispositivos

Gerando Topologia
Após a varredura, vá para 🌐 Topologia

Clique em "Gerar Topologia Visual"

Visualize o mapa gerado da sua rede

Exportando Relatórios
Acesse 📊 Relatórios

Clique em "Exportar Relatório PDF"

O relatório será salvo na pasta reports/

🔒 Segurança e Permissões
Níveis de Acesso
Administrador: Acesso completo + gerenciamento de usuários

Usuário: Funcionalidades básicas de varredura e relatórios

Proteção de Dados
Senhas criptografadas com SHA-256

Sessões com timeout automático

Validação de entrada em todos os campos

📈 Casos de Uso
👨‍💻 Administradores de Rede
Documentação completa da infraestrutura

Identificação de dispositivos não autorizados

Geração de relatórios para auditoria

🏢 Empresas e Corporações
Inventário de ativos de rede

Documentação para compliance

Planejamento de expansão de rede

🎓 Estudantes e Educadores
Aprendizado sobre protocolos de rede

Estudo de topologias de rede

Ferramenta educacional para redes de computadores

🏠 Usuários Domésticos
Mapeamento de dispositivos domésticos

Solução de problemas de conectividade

Gestão de rede local

🐛 Solução de Problemas
Problemas Comuns e Soluções
Varredura não encontra dispositivos

Verifique as permissões administrativas

Confirme a faixa de rede correta

Verifique firewall e antivírus

Erro de permissão no Windows

Execute como administrador

Verifique políticas de execução do PowerShell

Falha na geração de PDF

Verifique se a pasta reports/ existe

Confirme permissões de escrita

🤝 Contribuição
Contribuições são bem-vindas! Areas onde você pode ajudar:

🐛 Reportar bugs

💡 Sugerir novas funcionalidades

📚 Melhorar documentação

🔧 Otimizar código

Guidelines para Contribuição
Fork o projeto

Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

👨‍💻 Desenvolvedor
Eduardo De Vasconcelos Silva
https://img.shields.io/badge/GitHub-Profile-blue
https://img.shields.io/badge/LinkedIn-Profile-blue

🎉 Agradecimentos
À comunidade Python por ferramentas incríveis

Aos desenvolvedores do CustomTkinter pela interface moderna

Aos contribuidores do Scapy pelas capacidades de rede

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!

Última atualização: 25 Outubro 2025
