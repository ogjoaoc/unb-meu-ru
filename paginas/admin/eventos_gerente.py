import streamlit as st
from datetime import datetime, date, time

from components.styles import inject
from database.evento_db import (
    atualizar_evento,
    criar_evento,
    excluir_evento,
    listar_eventos,
    obter_evento,
)

inject()

user_sessao = st.session_state.get("usuario", {})
if not user_sessao or st.session_state.get("cargo") != "gerente":
    st.stop()

st.title("🎉 Gestão de Eventos")
st.caption("Cadastro, edição e exclusão de eventos do RU.")

eventos = listar_eventos()
eventos_map = {
    f"#{ev['id_evento']} · {str(ev['data_inicio'])} → {str(ev['data_fim'])}": ev
    for ev in eventos
}

tabs = st.tabs(["➕ Criar", "✏️ Editar", "🗑️ Excluir", "📋 Listar"])

with tabs[0]:
    st.subheader("Novo evento")
    with st.form("form_criar_evento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        id_evento = col1.number_input("ID do evento", min_value=1, step=1, value=1000)
        descricao = col2.text_area("Descrição", placeholder="Descreva o evento")

        d1, d2 = st.columns(2)
        data_ini = d1.date_input("Data inicial", value=date.today())
        hora_ini = d2.time_input("Hora inicial", value=time(9, 0))
        d3, d4 = st.columns(2)
        data_fim = d3.date_input("Data final", value=date.today())
        hora_fim = d4.time_input("Hora final", value=time(11, 0))

        submitted = st.form_submit_button("Criar evento", type="primary")
        if submitted:
            if not descricao.strip():
                st.error("Informe a descrição do evento.")
            else:
                dt_ini = datetime.combine(data_ini, hora_ini)
                dt_fim = datetime.combine(data_fim, hora_fim)
                if dt_fim < dt_ini:
                    st.error("A data final precisa ser maior ou igual à inicial.")
                elif obter_evento(int(id_evento)):
                    st.error("Já existe um evento com esse ID.")
                elif criar_evento(int(id_evento), dt_ini, dt_fim, descricao.strip()):
                    st.success("Evento criado com sucesso.")
                    st.rerun()
                else:
                    st.error("Não foi possível criar o evento.")

with tabs[1]:
    st.subheader("Editar evento")
    if not eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        escolhido = st.selectbox("Selecione o evento", list(eventos_map.keys()), key="evento_editar")
        evento = eventos_map[escolhido]
        data_ini_atual = datetime.strptime(str(evento["data_inicio"])[:16], "%Y-%m-%d %H:%M")
        data_fim_atual = datetime.strptime(str(evento["data_fim"])[:16], "%Y-%m-%d %H:%M")

        with st.form("form_editar_evento"):
            st.number_input("ID do evento", value=int(evento["id_evento"]), disabled=True)
            descricao_edit = st.text_area("Descrição", value=str(evento["descricao"]))
            d1, d2 = st.columns(2)
            data_ini_edit = d1.date_input("Data inicial", value=data_ini_atual.date(), key="edi_data_ini")
            hora_ini_edit = d2.time_input("Hora inicial", value=data_ini_atual.time(), key="edi_hora_ini")
            d3, d4 = st.columns(2)
            data_fim_edit = d3.date_input("Data final", value=data_fim_atual.date(), key="edi_data_fim")
            hora_fim_edit = d4.time_input("Hora final", value=data_fim_atual.time(), key="edi_hora_fim")

            submitted = st.form_submit_button("Salvar alterações", type="primary")
            if submitted:
                if not descricao_edit.strip():
                    st.error("Informe a descrição do evento.")
                else:
                    dt_ini = datetime.combine(data_ini_edit, hora_ini_edit)
                    dt_fim = datetime.combine(data_fim_edit, hora_fim_edit)
                    if dt_fim < dt_ini:
                        st.error("A data final precisa ser maior ou igual à inicial.")
                    elif atualizar_evento(int(evento["id_evento"]), dt_ini, dt_fim, descricao_edit.strip()):
                        st.success("Evento atualizado com sucesso.")
                        st.rerun()
                    else:
                        st.error("Não foi possível atualizar o evento.")

with tabs[2]:
    st.subheader("Excluir evento")
    if not eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        escolhido = st.selectbox("Selecione o evento para excluir", list(eventos_map.keys()), key="evento_excluir")
        evento = eventos_map[escolhido]
        st.warning(f"Você está prestes a excluir o evento #{evento['id_evento']}.")
        confirmar = st.checkbox("Confirmo que desejo excluir este evento.", key="confirmar_excluir_evento")
        if st.button("Excluir evento", type="primary", use_container_width=True):
            if not confirmar:
                st.warning("Marque a confirmação antes de excluir.")
            elif excluir_evento(int(evento["id_evento"])):
                st.success("Evento excluído com sucesso.")
                st.rerun()
            else:
                st.error("Não foi possível excluir o evento.")

with tabs[3]:
    st.subheader("Eventos cadastrados")
    if not eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        for ev in eventos:
            with st.container(border=True):
                st.markdown(f"**#{ev['id_evento']}** — {ev['descricao']}")
                st.caption(f"{str(ev['data_inicio'])} → {str(ev['data_fim'])}")
