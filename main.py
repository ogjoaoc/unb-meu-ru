# 100% vibecodado esse front
import streamlit as st
import sessoes as ses
from database.cardapio_db import *
from database.estudante_db import *
from services.autenticacao import run_login
from datetime import datetime

from components.styles import inject

st.set_page_config(
    page_title="UnB Meu RU",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject()

ses.inicia_sessao()

# ── Modais de Acesso ──────────────────────────────────────────────────────────
@st.dialog("🔑 Entrar no sistema", width="small")
def modal_login():
    st.markdown("### Bem-vindo de volta!")
    email_inp = st.text_input("E-mail Institucional", placeholder="seu_email@unb.br")
    pwd_inp = st.text_input("Senha", type="password", placeholder="••••")
    
    col1, col2 = st.columns(2)
    if col1.button("Entrar", type="primary", use_container_width=True):
        if not email_inp or not pwd_inp:
            st.error("Preencha todos os campos.")
        else:
            usuario_encontrado = run_login(email_inp, pwd_inp)
            if usuario_encontrado:
                st.session_state['usuario'] = usuario_encontrado
                st.session_state['cargo'] = usuario_encontrado['papel']
                st.rerun()
            else:
                st.error("E-mail ou senha inválidos.")
                
    if col2.button("Cancelar", use_container_width=True):
        st.rerun()


@st.dialog("📝 Criar conta de Estudante", width="large")
def modal_cadastro():
    st.markdown("Preencha os dados abaixo para criar sua conta estudantil no **UnB Meu RU**.")
    
    col1, col2 = st.columns(2)
    matricula_inp = col1.number_input("Número de Matrícula *", min_value=10000000, max_value=999999999, step=1, value=24100000)
    nome = col2.text_input("Nome completo *")
    
    email = col1.text_input("E-mail institucional *", placeholder="seu_email@aluno.unb.br")
    data_nasc = col2.date_input("Data de nascimento *", min_value=datetime(1950,1,1).date())
    
    curso = col1.text_input("Curso *", placeholder="Ex: Engenharia Mecatrônica")
    
    st.markdown("---")
    col1b, col2b = st.columns(2)
    senha = col1b.text_input("Definir Senha *", type="password")
    confirma = col2b.text_input("Confirmar Senha *", type="password")

    st.markdown("---")
    bc1, bc2 = st.columns(2)
    if bc1.button("Criar minha conta", type="primary", use_container_width=True):
        if not nome or not email or not curso or not senha or not matricula_inp:
            st.error("Por favor, preencha todos os campos obrigatórios.")
        elif senha != confirma:
            st.error("As senhas informadas não coincidem.")
        elif len(senha) < 4:
            st.error("A senha deve conter pelo menos 4 caracteres.")
        else:
            # CORRIGIDO: Apontando para a função correta do seu estudante_db.py
            resultado = adicionar_estudante(
                matricula=matricula_inp,
                nome=nome.strip(), 
                email=email.strip(), 
                senha=senha, 
                data_nascimento=str(data_nasc), 
                curso=curso.strip()
            )
            
            if resultado:
                st.success("✅ Conta criada com sucesso!")
                st.info(f"Matrícula vinculada: `{resultado['matricula']}`. Acesse o sistema utilizando seu e-mail cadastrado.")
                st.balloons()
            else:
                st.error("Erro ao processar cadastro. Certifique-se de que este e-mail ou matrícula já não estão em uso.")
                
    if bc2.button("Cancelar", use_container_width=True):
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  APP LOGADO — Navegação por páginas nativa
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state['usuario'] is not None:
    user = st.session_state['usuario']
    cargo = st.session_state['cargo']

    with st.sidebar:
        st.markdown("### 🍽️ UnB Meu RU")
        st.markdown(f"**{user['nome']}**")
        st.caption(cargo.upper())
        st.markdown("---")

        if cargo in ("nutricionista", "gerente"):
            pg_cardapio = st.Page("pages_admin/cardapio.py",  title="Cardápio",       icon="📅")
            nav = st.navigation([pg_cardapio])
        else:
            pg_home_e  = st.Page("paginas/estudante/home_estudante.py", title="Meu RU",  icon="🏠")
            pg_saldo   = st.Page("paginas/estudante/saldo.py",          title="Saldo",   icon="💳")
            
            # ALTERADO: Inclusão do pg_saldo na lista do st.navigation para permitir a troca de abas!
            nav = st.navigation([pg_home_e, pg_saldo])

        st.markdown("---")
        if st.button("Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    nav.run()
    st.stop()


# ═════════════════════════════════════════════════════════════════════════════
#  HOME PÚBLICA (Não Logado) — Sem a seção de Stats
# ═════════════════════════════════════════════════════════════════════════════

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div style="font-size:3.5rem">🍽️</div>
  <h1>UnB Meu RU</h1>
  <p>Restaurante Universitário da Universidade de Brasília</p>
</div>
""", unsafe_allow_html=True)

# ── Botões de acesso centralizados ────────────────────────────────────────────
bc_esq, b2, b3, bc_dir = st.columns([1.5, 1.2, 1.2, 1.5])
with b2:
    if st.button("🔑  Entrar", type="primary", use_container_width=True):
        modal_login()
with b3:
    if st.button("📝  Cadastrar", use_container_width=True):
        modal_cadastro()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── Feature cards ────────────────────────────────────────────────────────────
st.subheader("O que você encontra aqui")
fc1, fc2, fc3 = st.columns(3)
fc1.markdown("""
<div class="feat-card">
  <div class="feat-icon">📅</div>
  <h3>Cardápio Semanal</h3>
  <p>Consulte o menu completo de Café, Almoço e Jantar de cada dia da semana,
     atualizado pelos nutricionistas do RU.</p>
</div>
""", unsafe_allow_html=True)
fc2.markdown("""
<div class="feat-card">
  <div class="feat-icon">💳</div>
  <h3>Saldo & Transações</h3>
  <p>Acompanhe seu saldo de créditos, histórico de recargas e consumos
     diretamente na plataforma.</p>
</div>
""", unsafe_allow_html=True)
fc3.markdown("""
<div class="feat-card">
  <div class="feat-icon">🎉</div>
  <h3>Mural de Eventos</h3>
  <p>Fique por dentro das feiras, semanas temáticas e atividades culturais
     organizadas no espaço do RU.</p>
</div>
""", unsafe_allow_html=True)

# ── Preview do cardápio atual (público) ───────────────────────────────────────
try:
    ativo = cardapio_ativo()
except Exception:
    ativo = None

if ativo:
    st.markdown("---")
    st.subheader("📋 Cardápio desta semana")
    st.caption(f"{ativo['data_inicio'] if 'data_inicio' in ativo else ativo['Data_inicio']}  →  {ativo['data_fim'] if 'data_fim' in ativo else ativo['Data_fim']}")

    DIAS_PT = {"Segunda":"Seg","Terca":"Ter","Quarta":"Qua",
               "Quinta":"Qui","Sexta":"Sex","Sabado":"Sáb","Domingo":"Dom"}

    itens = itens_do_cardapio(ativo["id_cardapio"] if "id_cardapio" in ativo else ativo["ID_Cardapio"])
    almoco = [i for i in itens if (i["periodo"] if "periodo" in i else i["Periodo"]) == "Almoco"]
    dias_c = list(dict.fromkeys(i["dia_semana"] if "dia_semana" in i else i["Dia_semana"] for i in almoco))

    if dias_c:
        cols = st.columns(len(dias_c))
        for idx, dia in enumerate(dias_c):
            dia_itens = [i for i in almoco if (i["dia_semana"] if "dia_semana" in i else i["Dia_semana"]) == dia]
            with cols[idx]:
                st.markdown(f"**{DIAS_PT.get(dia, dia)}**")
                por_cat: dict = {}
                for it in dia_itens:
                    cat_key = it["categoria"] if "categoria" in it else it["Categoria"]
                    nome_key = it["nome"] if "nome" in it else it["Nome"]
                    por_cat.setdefault(cat_key, []).append(nome_key)
                for cat, nomes in por_cat.items():
                    st.markdown(f"<small style='color:#0a7a14'>{cat}</small>", unsafe_allow_html=True)
                    for n in nomes:
                        st.markdown(f"<small>• {n}</small>", unsafe_allow_html=True)

# ── Preview de eventos (público) ──────────────────────────────────────────────
try:
    eventos = listar_eventos()
except Exception:
    eventos = []

proximos = []
agora = datetime.now()
for ev in eventos:
    try:
        dt = datetime.strptime(ev["Data_inicio"][:16], "%Y-%m-%d %H:%M")
        if dt > agora:
            proximos.append((ev, dt))
    except Exception:
        pass

if proximos:
    st.markdown("---")
    st.subheader("🎉 Próximos Eventos")
    for ev, dt in proximos[:3]:
        with st.container(border=True):
            c1, c2 = st.columns([5,1])
            c1.markdown(f"**{ev['Descricao'][:80]}{'...' if len(ev['Descricao'])>80 else ''}**")
            c2.markdown(f"<span class='notif-badge'>📅 {dt.strftime('%d/%m')}</span>",
                        unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:#aaa;font-size:.78rem'>"
    "UnB Meu RU · Universidade de Brasília · 2026</center>",
    unsafe_allow_html=True,
)