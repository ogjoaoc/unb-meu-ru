import streamlit as st
from components.styles import inject
from database.cardapio_db import listar_cardapios, excluir_cardapio
from database.estudante_db import (
    listar_estudantes_admin,
    definir_saldo_estudante,
    remover_estudante_sistema,
)

inject()

user_sessao = st.session_state.get("usuario", {})
if not user_sessao or st.session_state.get("cargo") != "gerente":
    st.stop()

st.title("🛠️ Dashboard do Gerente")
st.caption("Acesso administrativo para manutenção de cardápios e estudantes.")

# --- Ações de cardápio ---
st.subheader("📅 Deletar cardápios")
cardapios = listar_cardapios(50)

if not cardapios:
    st.info("Nenhum cardápio encontrado para remoção.")
else:
    opcoes_cardapio = {
        (
            f"#{c['id_cardapio']} | {str(c['data_inicio'])} -> {str(c['data_fim'])} | "
            f"{c['status']}"
        ): c["id_cardapio"]
        for c in cardapios
    }

    escolhido = st.selectbox(
        "Selecione o cardápio para excluir",
        options=list(opcoes_cardapio.keys()),
    )

    confirmar_delete = st.checkbox("Confirmo que desejo excluir o cardápio selecionado.")
    if st.button("🗑️ Excluir cardápio", type="primary", use_container_width=True):
        if not confirmar_delete:
            st.warning("Marque a confirmação antes de excluir.")
        else:
            id_cardapio = opcoes_cardapio[escolhido]
            if excluir_cardapio(id_cardapio):
                st.success(f"Cardápio #{id_cardapio} removido com sucesso.")
                st.rerun()
            else:
                st.error("Não foi possível excluir o cardápio.")

st.markdown("---")

# --- Ações de estudantes ---
st.subheader("🎓 Gestão de estudantes")
estudantes = listar_estudantes_admin(300)

if not estudantes:
    st.info("Nenhum estudante cadastrado.")
else:
    opcoes_estudante = {
        (
            f"{e['nome']} | Matrícula {e['matricula']} | "
            f"Saldo R$ {float(e['saldo_ru']):.2f}"
        ): e
        for e in estudantes
    }

    selecionado = st.selectbox(
        "Selecione o estudante",
        options=list(opcoes_estudante.keys()),
    )
    estudante = opcoes_estudante[selecionado]

    c1, c2 = st.columns(2)
    c1.metric("Matrícula", estudante["matricula"])
    c2.metric("Saldo atual", f"R$ {float(estudante['saldo_ru']):.2f}")

    st.markdown("### 💳 Modificar saldo")
    novo_saldo = st.number_input(
        "Novo saldo do estudante",
        min_value=0.0,
        step=1.0,
        value=float(estudante["saldo_ru"]),
        format="%.2f",
    )

    if st.button("Salvar novo saldo", use_container_width=True):
        if definir_saldo_estudante(estudante["matricula"], float(novo_saldo)):
            st.success("Saldo atualizado com sucesso.")
            st.rerun()
        else:
            st.error("Não foi possível atualizar o saldo.")

    st.markdown("### ❌ Remover estudante do sistema")
    confirmar_remocao = st.checkbox(
        "Confirmo a remoção definitiva deste estudante e seus dados vinculados.",
        key="confirmacao_remocao_estudante",
    )

    if st.button("Remover estudante", type="primary", use_container_width=True):
        if not confirmar_remocao:
            st.warning("Marque a confirmação antes de remover.")
        else:
            if remover_estudante_sistema(estudante["matricula"]):
                st.success("Estudante removido com sucesso.")
                st.rerun()
            else:
                st.error("Não foi possível remover o estudante.")
