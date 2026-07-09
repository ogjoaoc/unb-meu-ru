import streamlit as st
from datetime import datetime, date, time
from components.styles import inject
from database.evento_db import (
    atualizar_evento,
    criar_evento,
    excluir_evento,
    listar_eventos,
    obter_evento,
    listar_inscritos_evento,
    cancelar_inscricao,
)

inject()

user_sessao = st.session_state.get("usuario", {})
if not user_sessao or st.session_state.get("cargo") != "gerente":
    st.error("Acesso restrito a Gerentes.")
    st.stop()

st.title("🎉 Gestão de Eventos e Inscrições")
st.caption("Controle administrativo de eventos, capas e listagem de alunos inscritos.")

eventos = listar_eventos()
eventos_map = {
    f"#{ev['id_evento']} · {ev['descricao'][:40]}...": ev
    for ev in eventos
}

# ADICIONADO: Aba "Inscrições" para o gerenciamento completo do Gerente
tabs = st.tabs(["➕ Criar", "✏️ Editar", "🗑️ Excluir", "📋 Listar", "🎟️ Inscrições"])

# --- ABAS EXISTENTES (CRIAR, EDITAR, EXCLUIR, LISTAR) ---
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
        foto_upload = st.file_uploader("🖼️ Foto de Capa (Opcional)", type=["png", "jpg", "jpeg"], key="upload_criar")

        if st.form_submit_button("Criar evento", type="primary"):
            if not descricao.strip(): st.error("Informe a descrição.")
            else:
                dt_ini = datetime.combine(data_ini, hora_ini)
                dt_fim = datetime.combine(data_fim, hora_fim)
                bytes_foto = foto_upload.read() if foto_upload is not None else None
                if dt_fim < dt_ini: st.error("A data final precisa ser maior que a inicial.")
                elif obter_evento(int(id_evento)): st.error("Já existe um evento com esse ID.")
                elif criar_evento(int(id_evento), dt_ini, dt_fim, descricao.strip(), bytes_foto):
                    st.success("Evento criado com sucesso.")
                    st.rerun()

with tabs[1]:
    st.subheader("Editar evento")
    if not eventos: st.info("Nenhum evento cadastrado.")
    else:
        escolhido = st.selectbox("Selecione o evento", list(eventos_map.keys()), key="evento_editar")
        evento = eventos_map[escolhido]
        data_ini_atual = datetime.strptime(str(evento["data_inicio"])[:16], "%Y-%m-%d %H:%M")
        data_fim_atual = datetime.strptime(str(evento["data_fim"])[:16], "%Y-%m-%d %H:%M")

        with st.form("form_editar_evento"):
            descricao_edit = st.text_area("Descrição", value=str(evento["descricao"]))
            d1, d2 = st.columns(2)
            data_ini_edit = d1.date_input("Data inicial", value=data_ini_atual.date())
            hora_ini_edit = d2.time_input("Hora inicial", value=data_ini_atual.time())
            d3, d4 = st.columns(2)
            data_fim_edit = d3.date_input("Data final", value=data_fim_atual.date())
            hora_fim_edit = d4.time_input("Hora final", value=data_fim_atual.time())
            foto_edit_upload = st.file_uploader("🖼️ Alterar Foto de Capa", type=["png", "jpg", "jpeg"])

            if st.form_submit_button("Salvar alterações", type="primary"):
                dt_ini = datetime.combine(data_ini_edit, hora_ini_edit)
                dt_fim = datetime.combine(data_fim_edit, hora_fim_edit)
                bytes_foto_edit = foto_edit_upload.read() if foto_edit_upload is not None else None
                if atualizar_evento(int(evento["id_evento"]), dt_ini, dt_fim, descricao_edit.strip(), bytes_foto_edit):
                    st.success("Evento atualizado.")
                    st.rerun()

with tabs[2]:
    st.subheader("Excluir evento")
    if not eventos: st.info("Nenhum evento cadastrado.")
    else:
        escolhido = st.selectbox("Selecione o evento para excluir", list(eventos_map.keys()), key="evento_excluir")
        evento = eventos_map[escolhido]
        st.warning(f"Você está deletando o evento #{evento['id_evento']}. Isso removerá as inscrições associadas via CASCADE.")
        confirmar = st.checkbox("Confirmo a exclusão definitiva.")
        if st.button("Excluir evento", type="primary"):
            if confirmar and excluir_evento(int(evento["id_evento"])):
                st.success("Evento removido.")
                st.rerun()

with tabs[3]:
    st.subheader("Eventos cadastrados")
    for ev in eventos:
        with st.container(border=True):
            if ev.get("foto_capa"): st.image(bytes(ev["foto_capa"]), width=180)
            st.markdown(f"**#{ev['id_evento']}** — {ev['descricao']}")

# --- NOVA ABA ADICIONADA: GERENCIAMENTO DE INSCRIÇÕES ---
with tabs[4]:
    st.subheader("Gerenciamento de Alunos Inscritos")
    if not eventos:
        st.info("Nenhum evento cadastrado para gerenciar inscrições.")
    else:
        evento_selecionado = st.selectbox(
            "Selecione um evento para listar os inscritos:", 
            list(eventos_map.keys()), 
            key="evento_inscricoes_gerente"
        )
        ev_id = eventos_map[evento_selecionado]["id_evento"]
        
        inscritos = listar_inscritos_evento(ev_id)
        
        if not inscritos:
            st.info("Nenhum estudante inscrito neste evento até o momento.")
        else:
            st.write(f"📊 **Total de Inscritos:** {len(inscritos)}")
            
            for aluno in inscritos:
                with st.container(border=True):
                    col_info, col_btn = st.columns([4, 1])
                    with col_info:
                        st.markdown(f"👤 **{aluno['nome']}** — Matrícula: `{aluno['matricula']}`")
                        st.caption(f"📧 {aluno['email']} | 🎓 Curso: {aluno['curso']}")
                        # Tratamento simples para exibição da data de inscrição
                        data_insc = str(aluno['data_inscricao'])[:16]
                        st.caption(f"⏱️ Inscrito em: {data_insc}")
                    with col_btn:
                        st.write("") # Espaçador visual
                        if st.button("❌ Remover", key=f"rem_{ev_id}_{aluno['matricula']}", type="secondary", use_container_width=True):
                            if cancelar_inscricao(ev_id, int(aluno['matricula'])):
                                st.success(f"Inscrição de {aluno['nome']} removida!")
                                st.rerun()