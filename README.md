# Caixinha de Final de Ano - Caça-Níquel Interativo

Sistema de jogo de caça-níquel interativo para engajar funcionários de condomínios através de uma promoção de final de ano.

## Funcionalidades

- Validação de CPF para acesso
- Interface de caça-níquel com 3 colunas
- Sistema de premiação controlado
- Distribuição de até 122 prêmios
- Geração de QR Code para acesso
- Envio de confirmação por email

## Tecnologias Utilizadas

- Python/Flask
- SQLAlchemy
- JavaScript/jQuery
- Bootstrap
- Font Awesome

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/caixinha-final-ano.git
cd caixinha-final-ano
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (.env):
```
SECRET_KEY=sua-chave-secreta
MAIL_SERVER=seu-servidor-smtp
MAIL_PORT=587
MAIL_USERNAME=seu-email
MAIL_PASSWORD=sua-senha
```

5. Inicialize o banco de dados:
```bash
python init_db.py
```

6. Execute o servidor:
```bash
python run.py
```

## Período da Promoção

- Início: 01/12
- Término: 20/12

## Regras do Jogo

- Cada CPF tem direito a 3 tentativas
- Primeira tentativa nunca é premiada
- Chance de prêmio de R$50,00 a cada 3 jogadas
- Máximo de 122 ganhadores
- Premiação única por CPF
