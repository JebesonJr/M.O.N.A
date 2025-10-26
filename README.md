# M.O.N.A

Projeto M.O.N.A — Mente Operacional Neural Autônoma

## Como rodar localmente

1. Criar ambiente virtual (opcional)
2. Instalar dependências: `pip install -r requirements.txt`
3. Rodar: `python3 mona3.py`
4. Abra: http://127.0.0.1:5000/

## Deploy no Render
1. Crie repositório GitHub com esses arquivos
2. No Render: New -> Web Service -> conecte ao repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn mona3:app`

## Admin
Usuário admin padrão: `Lord Over`
Senha padrão: `@Brasil1248`

Ao aprovar uma conta a mensagem automática é: "Bem vindo ao sistema da Mente Operacional Neural Autônoma"