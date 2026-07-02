# VisionAI Platform 🖥️

A Plataforma Avançada de Visão Computacional & Áudio é um ecossistema completo construído utilizando Clean Architecture. O sistema processa pipelines de visão computacional em tempo real usando OpenCV e realiza transcrições robustas de arquivos de voz utilizando a biblioteca otimizada Faster-Whisper. Todos os dados coletados são salvos diretamente no banco PostgreSQL gerenciado no Neon.tech.

## 🚀 Tecnologias Empregadas

- **Interface Gráfica**: Streamlit (Layout responsivo e dinâmico)
- **Motores Core**: OpenCV (Filtros de matrizes, laplaciano de nitidez e Viola-Jones)
- **Áudio & Voz**: Faster-Whisper (Modelo 'tiny' de Machine Learning para CPU)
- **ORMs e Bancos de Dados**: SQLAlchemy 2.0 & PostgreSQL (Neon.tech Cloud)

## 🏢 Arquitetura do Projeto

A arquitetura adota a separação estrita de responsabilidades:
1. `components/` - Visual puro (UI), isolando o Streamlit da lógica de negócio.
2. `controllers/` - Orquestradores de Casos de Uso.
3. `services/` - Motores matemáticos, computacionais e inteligência artificial.
4. `repositories/` - Isolamento das queries SQL transacionais.
5. `models/` - Declaração de tabelas mapeadas em objetos Pythônicos.

## ⚙️ Instalação e Execução Local

Para rodar o projeto localmente, basta executar os passos abaixo diretamente no terminal do sistema (sem necessidade de criação de ambientes isolados virtuais `venv`):

```bash
# 1. Instalar todas as dependências requeridas de forma nativa e global
pip install -r requirements.txt

# 2. Configurar suas variáveis de ambiente copiando o arquivo base de exemplo
cp .env.example .env
# Certifique-se de preencher a URL de conexão do Neon.tech dentro do arquivo .env recém-criado

# 3. Inicializar e executar o ecossistema web
streamlit run app.py