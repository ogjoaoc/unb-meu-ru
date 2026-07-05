# 100% vibecodado
import streamlit as st
from components.styles import inject
from database.cardapio_db import cardapio_ativo, itens_do_cardapio, media_notas_cardapio, registrar_feedback
from database.estudante_db import saldo_atual

inject()

DIAS     = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
DIAS_PT  = {"Segunda":"Segunda-feira","Terca":"Terça-feira","Quarta":"Quarta-feira",
            "Quinta":"Quinta-feira","Sexta":"Sexta-feira","Sabado":"Sábado","Domingo":"Domingo"}
DIAS_ABR = {k: v[:3]+"." for k,v in DIAS_PT.items()}
PERIODOS    = ["Cafe","Almoco","Jantar"]
PERIODOS_PT = {"Cafe":"☕ Café","Almoco":"🍽️ Almoço","Jantar":"🌙 Jantar"}

# ADAPTAÇÃO: Buscando da estrutura real do seu main.py
user_sessao = st.session_state.get('usuario', {})
matricula   = user_sessao.get('matricula')
nome        = user_sessao.get('nome', 'Estudante')
curso       = user_sessao.get('curso', '')

# Busca o saldo em tempo real do banco Postgres
saldo = saldo_atual(matricula) if matricula else 0.0

# ── Cabeçalho (Idêntico ao alvo da image_4b0966.png) ──────────────────────────
h1, h2, h3 = st.columns([3,1,1])
h1.markdown(f"## 🎒 Olá, {nome.split()[0]}!")
if curso: 
    h1.caption(curso)
h2.metric("💰 Saldo RU", f"R$ {saldo:.2f}")
h3.metric("📋 Matrícula", matricula or "—")

if saldo < 5:
    st.warning("⚠️ Saldo baixo! Procure o caixa do RU para recarregar.")

st.markdown("---")

# ── Cardápio ─────────────────────────────────────────────────────────────────
st.subheader("🍽️ Cardápio desta semana")
ativo = cardapio_ativo()
if not ativo:
    st.info("O cardápio ainda não foi publicado. Volte em breve!")
    st.stop()

# ADAPTAÇÃO: lendo as chaves em minúsculo geradas pelo RealDictCursor
cid           = ativo["id_cardapio"]
media, total  = media_notas_cardapio(cid)
m1, m2, m3   = st.columns(3)
m1.metric("Período",      f"{str(ativo['data_inicio'])} → {str(ativo['data_fim'])}")
m2.metric("⭐ Nota média", f"{media}/5" if media else "Sem avaliações")
m3.metric("💬 Feedbacks", total)

itens = itens_do_cardapio(cid)
# ADAPTAÇÃO: i["dia_semana"] em minúsculo vindo do banco
dias_disp = [d for d in DIAS if any(i["dia_semana"] == d for i in itens)]

if not dias_disp:
    st.warning("Cardápio publicado mas sem itens ainda.")
    st.stop()

dia_sel = st.radio("Ver dia:", dias_disp, horizontal=True, format_func=lambda d: DIAS_ABR[d])
st.markdown(f"### 📆 {DIAS_PT[dia_sel]}")

for periodo in PERIODOS:
    # ADAPTAÇÃO: comparando chaves minúsculas do banco
    per_its = [i for i in itens if i["dia_semana"] == dia_sel and i["periodo"] == periodo]
    if not per_its: 
        continue
    with st.expander(PERIODOS_PT[periodo], expanded=(periodo == "Almoco")):
        por_cat: dict = {}
        for it in per_its:
            por_cat.setdefault(it["categoria"], []).append((it["nome"], it.get("composicao", "")))
        cols = st.columns(max(1, len(por_cat)))
        for idx, (cat, nomes) in enumerate(por_cat.items()):
            with cols[idx % len(cols)]:
                st.markdown(f"**{cat}**")
                for n, comp in nomes:
                    detalhe = f" — *{comp}*" if comp else ""
                    st.markdown(f"• {n}{detalhe}")

# ── Feedback ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("💬 Avaliar o Cardápio")
with st.form("form_fb"):
    nota = st.slider("Nota", 1, 5, 4)
    st.write("⭐" * nota + "☆" * (5 - nota))
    comentario = st.text_area("Comentário (opcional)", placeholder="O que achou?")
    if st.form_submit_button("Enviar avaliação", type="primary"):
        ok = registrar_feedback(comentario, nota, cid, matricula)
        if ok: 
            st.success("Obrigado! ⭐")
            st.rerun()
        else:  
            st.warning("Você já avaliou este cardápio.")