import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading
import os  # Import necessário para lidar com os caminhos


class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        root.title("Envio de E-mail Marketing")

        # Label e caixa de texto para os e-mails
        self.email_label = tk.Label(
            root, text="Cole os e-mails aqui (um por linha):")
        self.email_label.pack()
        self.email_text = tk.Text(root, height=10, width=50)
        self.email_text.pack()

        # Botão para enviar e-mails
        self.send_button = tk.Button(
            root, text="Enviar E-mails", command=self.start_sending)
        self.send_button.pack(pady=10)

        # Barra de progresso
        self.progress_label = tk.Label(root, text="Progresso:")
        self.progress_label.pack()
        self.progress = ttk.Progressbar(
            root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        # Área de status
        self.status_label = tk.Label(root, text="Status de envio")
        self.status_label.pack()
        self.status_text = tk.Text(root, height=10, width=50, state='disabled')
        self.status_text.pack()

        # Variáveis de configuração
        self.email = 'gabriel.oliveira@coopluiza.com.br'
        self.password_file = os.path.join(
            "senha", "senha.txt")  # Caminho do arquivo senha.txt
        self.images_folder = os.path.join("img")  # Pasta que contém as imagens
        self.images = ['capitalizacao.png',
                       'visao.png', 'educa.png', 'esporte.png']

    def start_sending(self):
        # Iniciar thread para não travar a interface
        threading.Thread(target=self.send_email).start()

    def send_email(self):
        # Obtém a senha do ambiente
        senha_do_email = os.getenv('EMAIL_PASSWORD')
        if not senha_do_email:
            messagebox.showerror("Erro", "A variável de ambiente EMAIL_PASSWORD não foi definida.")
            return

        # Obtém a lista de e-mails do widget de texto
        email_list = self.email_text.get("1.0", "end-1c").splitlines()
        if not email_list:
            messagebox.showerror("Erro", "Por favor, cole pelo menos um e-mail.")
            return

        # Configura o e-mail
        msg = MIMEMultipart('related')
        msg['Subject'] = 'Você já conhece a Coopluiza?'
        msg['From'] = self.email
        link = 'https://wscredcoopluiza.facilinformatica.com.br/facweb/#formulario-de-pessoa-fisica'
        html = f"""
        <html>  <body style="background-color: #007b83; font-family: Arial, sans-serif; margin: 0; padding: 0; text-align: center;">
        <!-- Contêiner centralizado -->
        <div style="max-width: 750px; margin: 0 auto; padding: 20px; padding-top: 70px;">
            <!-- Link com imagem centralizada -->
            <a href="{link}" style="display: block; text-align: center; margin-bottom: 40px;">
                <img src="cid:image1" alt="Imagem Clique Aqui" style="max-width: 85%; height: auto; display: block; margin: 0 auto; margin-bottom: 60px;">
            </a>
            <!-- Texto centralizado -->
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">Já imaginou ter a tranquilidade financeira que sempre sonhou? Fazer parte da</p>
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">Coopluiza é estar mais perto desse objetivo, com o apoio que você precisa para</p>
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">conquistar o que tanto deseja. Não perca mais tempo, dê o próximo passo para</p>
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">transformar seus sonhos em realidade. Faça sua adesão agora mesmo e</p>
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">comece a construir um futuro melhor para você e sua família. Estamos aqui</p>
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">para te ajudar em cada etapa dessa jornada. Cadastre-se hoje e sinta a</p>
            <p style="color: #ffffff; font-weight: bold; font-size: 15px; line-height: 1.9; margin: 0;">diferença!</p>

            <!-- Linha horizontal centralizada -->
            <hr style="border: 0; height: 1px; background: #ffffff; width: 750px; margin: 40px auto;">

            <!-- Bloco de imagens com links em layout de duas linhas e duas colunas -->
            <table style="width: 100%; border-spacing: 20px; margin-bottom: 40px;">
                <tr>
                    <td style="text-align: center;">
                        <a href="{link}" style="display: block;">
                            <img src="cid:capitalizacao.png" alt="Capitalização" style="max-width: 100%; height: auto;">
                        </a>
                    </td>
                    <td style="text-align: center;">
                        <a href="{link}" style="display: block;">
                            <img src="cid:visao.png" alt="Visão" style="max-width: 100%; height: auto;">
                        </a>
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center;">
                        <a href="{link}" style="display: block;">
                            <img src="cid:educa.png" alt="Educação" style="max-width: 100%; height: auto;">
                        </a>
                    </td>
                    <td style="text-align: center;">
                        <a href="{link}" style="display: block;">
                            <img src="cid:esporte.png" alt="Esportes" style="max-width: 100%; height: auto;">

                        </a>
                    </td>
                </tr>
            </table>
                <!-- Linha horizontal centralizada -->
            <hr style="border: 0; height: 1px; background: #ffffff; width: 750px; margin: 40px auto;">
        </div>

    </body>
    </html>"""  # Parte do HTML cortada por brevidade.
        msg.attach(MIMEText(html, 'html'))

        # Adicionar imagens ao e-mail
        self.add_image('coop.png', 'image1', msg)
        for image_file in self.images:
            self.add_image(image_file, image_file, msg)

        # Envio de e-mails por lotes
        total_emails = len(email_list)
        lote_size = 100
        self.progress['maximum'] = (total_emails // lote_size) + 1

        start_time = time.time()

        for i in range(0, total_emails, lote_size):
            lote = email_list[i:i + lote_size]
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.email, senha_do_email)
                    smtp.sendmail(self.email, lote, msg.as_string())
                self.update_status(
                    f"Lote {i // lote_size + 1} enviado com sucesso.", lote)
            except Exception as e:
                self.update_status(f"Erro ao enviar lote {
                                   i // lote_size + 1}: {str(e)}")
            finally:
                # Atualiza a barra de progresso na thread principal
                self.root.after(0, self.update_progress, 1)
                time.sleep(1)  # Apenas para simulação de tempo
                self.root.update_idletasks()

        elapsed_time = time.time() - start_time
        self.update_status(f"Envio concluído em {elapsed_time:.2f} segundos.")

    def add_image(self, filename, cid, msg):
        image_path = os.path.join(
            self.images_folder, filename)  # Caminho da imagem
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data, name=filename)
                image.add_header('Content-ID', f'<{cid}>')
                msg.attach(image)
        except FileNotFoundError:
            self.update_status(f"Imagem não encontrada: {image_path}")

    def update_status(self, message, lote=[]):
        # Atualiza a área de status
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, f"{message}\n")
        if lote:
            self.status_text.insert(tk.END, f"Emails: {', '.join(lote)}\n")
        self.status_text.config(state='disabled')
        self.status_text.see(tk.END)  # Scroll automático para o fim

    def update_progress(self, step):
        self.progress.step(step)


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
