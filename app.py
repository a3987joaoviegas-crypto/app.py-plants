import tkinter as tk
from tkinter import messagebox, simpledialog

# 🔐 password de admin
ADMIN_PASSWORD = "lucasplant6354"

# ---------------- DADOS ---------------- #

videos = [
    "Como regar plantas corretamente",
    "Como plantar uma semente",
]

info_nova = [
    "As plantas precisam de luz solar ☀️",
    "Regar demasiado pode matar a planta 💧",
]

avisos = [
    "Não partilhar a password 🔒",
    "Cuidado com plantas tóxicas ⚠️",
]

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Plant Videos")
root.geometry("600x400")
root.configure(bg="white")

# --- HEADER ---
header = tk.Frame(root, bg="white", height=60)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🍃 Plant Videos",
    font=("Arial", 20, "bold"),
    bg="white"
)
title.pack(pady=10)

# --- MAIN AREA ---
main = tk.Frame(root, bg="white")
main.pack(fill="both", expand=True)

# --- SIDEBAR ---
sidebar = tk.Frame(main, bg="#e8f5e9", width=150)
sidebar.pack(side="left", fill="y")

content = tk.Frame(main, bg="white")
content.pack(side="right", fill="both", expand=True)

# ---------------- FUNÇÕES ---------------- #

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

def show_videos():
    clear_content()
    tk.Label(content, text="🎥 Vídeos", font=("Arial", 16), bg="white").pack(pady=10)

    for v in videos:
        tk.Label(content, text="▶ " + v, bg="white").pack(anchor="w")

    tk.Button(content, text="➕ Adicionar vídeo", command=add_video).pack(pady=10)

def show_info():
    clear_content()
    tk.Label(content, text="🆕 Informação nova", font=("Arial", 16), bg="white").pack(pady=10)

    for i in info_nova:
        tk.Label(content, text="🌱 " + i, bg="white").pack(anchor="w")

def show_avisos():
    clear_content()
    tk.Label(content, text="⚠️ Avisos", font=("Arial", 16), bg="white").pack(pady=10)

    for a in avisos:
        tk.Label(content, text="❗ " + a, bg="white").pack(anchor="w")

# 🔒 função protegida por password
def add_video():
    password = simpledialog.askstring("Password", "Introduz a password:", show="*")

    if password == ADMIN_PASSWORD:
        new_video = simpledialog.askstring("Novo vídeo", "Nome do vídeo:")
        if new_video:
            videos.append(new_video)
            messagebox.showinfo("Sucesso", "Vídeo adicionado com sucesso!")
            show_videos()
    else:
        messagebox.showerror("Erro", "Password incorreta!")

# ---------------- SIDEBAR ---------------- #

btn1 = tk.Button(sidebar, text="🎥 Vídeos", command=show_videos)
btn1.pack(fill="x", pady=5)

btn2 = tk.Button(sidebar, text="🆕 Informação", command=show_info)
btn2.pack(fill="x", pady=5)

btn3 = tk.Button(sidebar, text="⚠️ Avisos", command=show_avisos)
btn3.pack(fill="x", pady=5)

# ---------------- START ---------------- #

show_videos()
root.mainloop()
