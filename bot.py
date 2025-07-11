from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def confere_data(dt_expiracao):
    dt_verificada = datetime.strptime(dt_expiracao, "%d/%m/%Y")
    dt_atual = datetime.now()

    if dt_atual <= dt_verificada <= dt_atual + timedelta(days=5):
        return True
    else:
        return False

def leCSV():
    with open("./resources/solucoes.csv", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip().replace('\r', '').replace('\n', '')

            if "dt_expiracao:" in linha:
                dt_expiracao = linha.split("dt_expiracao:")[1].split(",")[0]
                solucao = linha.split("solucao:")[1].split(",")[0]
                local = linha.split("local:")[1].split(",")[0]

                if confere_data(dt_expiracao):
                    enviar_email(dt_expiracao, solucao, local)

def enviar_email(dt_expiracao, solucao, local):
    servidor_smtp = "smtp.hostinger.com"
    porta = 587
    email_remetente = "noreply@cisolutions.com.br"
    senha_remetente = "Ymr#2Z*HE4nSB74J4#CI$o&2018"

    # Configuração do e-mail
    emails_destinatarios = [
        "diego.castro@copymaq.com.br",
        "alvaro.santos@copymaq.com.br",
        "katlen.souza@copymaq.com.br"
    ]

    assunto = "Solução prestes a expirar"

    # Montando a mensagem
    mensagem = f"""
    Prezado(a),

    Favor verificar a solução: {solucao}
    Local: {local}
    Data de expiração: {dt_expiracao}

    Atenciosamente,
    Equipe CI Solutions
    """

    try:
        # Criação do e-mail com MIME
        email = MIMEMultipart()
        email["From"] = email_remetente
        email["To"] = ", ".join(emails_destinatarios)
        email["Subject"] = assunto
        email.attach(MIMEText(mensagem, "plain"))

        # Conexão com o servidor SMTP
        with smtplib.SMTP(servidor_smtp, porta) as servidor:
            servidor.starttls()  # Inicia criptografia TLS
            servidor.login(email_remetente, senha_remetente)  # Faz login
            servidor.sendmail(email_remetente, emails_destinatarios, email.as_string())

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def main():
    leCSV()

main()