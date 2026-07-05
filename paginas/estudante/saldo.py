# 100% vibecodado
import streamlit as st
from components.styles import inject
from database.estudante_db import historico_transacoes, recarregar_saldo, saldo_atual

inject()

# ADAPTAÇÃO: Buscando as variáveis corretas da sessão mapeada no main
user_sessao = st.session_state.get('usuario', {})
matricula   = user_sessao.get('matricula')

saldo = saldo_atual(matricula) if matricula else 0.0

st.title("💳 Saldo & Transações")

# ── Cards de saldo (image_4b5b5d.png) ─────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.metric("💰 Saldo Atual",         f"R$ {saldo:.2f}")
c2.metric("🎓 Matrícula",           matricula or "—")
c3.metric("🍽️ Refeições estimadas", f"~{int(saldo//3.50)}" if saldo > 0 else "0",
          help="Estimativa com R$ 3,50 por refeição")

if saldo <= 5:
    st.warning("⚠️ Saldo baixo! Procure o caixa do RU para recarregar.")

st.markdown("---")

# ── Histórico ────────────────────────────────────────────────────────────────
st.subheader("📊 Histórico de Transações")
transacoes = historico_transacoes(matricula, 30) if matricula else []

if not transacoes:
    st.info("Nenhuma transação registrada ainda.")
else:
    # ADAPTAÇÃO: Lendo chaves em minúsculas vindas do cursor Postgres ('valor_transacao')
    total_rec = sum(float(t["valor_transacao"]) for t in transacoes if float(t["valor_transacao"]) > 0)
    total_con = sum(float(t["valor_transacao"]) for t in transacoes if float(t["valor_transacao"]) < 0)
    
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Total recarregado", f"R$ {total_rec:.2f}")
    mc2.metric("Total consumido",   f"R$ {abs(total_con):.2f}")
    mc3.metric("Nº transações",     len(transacoes))
    st.markdown("---")

    for t in transacoes:
        # ADAPTAÇÃO: chaves tratadas em minúsculo para evitar KeyError
        v    = float(t["valor_transacao"])
        data = str(t["data_hora"])[:16]
        if v > 0:
            st.markdown(f"🟢 **+R$ {v:.2f}** &nbsp; Recarga &nbsp; `{data}`")
        else:
            st.markdown(f"🔴 **−R$ {abs(v):.2f}** &nbsp; Consumo &nbsp; `{data}`")

st.markdown("---")

# ── Simular recarga ───────────────────────────────────────────────────────────
with st.expander("💳 Simular recarga de saldo"):
    st.caption("Em produção, recargas são feitas pelos funcionários do caixa. Isso é apenas para demonstração.")
    with st.form("form_recarga"):
        valor = st.select_slider("Valor", options=[10.0, 20.0, 30.0, 50.0, 100.0],
                                 format_func=lambda v: f"R$ {v:.2f}")
        if st.form_submit_button("Recarregar", type="primary"):
            if recarregar_saldo(matricula, valor):
                st.success(f"R$ {valor:.2f} adicionados!")
                st.rerun()