import streamlit as st
from datetime import datetime
from components.styles import inject
from database.evento_db import (
    cancelar_inscricao,
    contagem_inscritos,
    inscricoes_do_estudante,
    inscrever_estudante,
    listar_eventos,
)

inject()

user_sessao = st.session_state.get("usuario", {})
matricula = user_sessao.get("matricula")
if not matricula:
	st.warning("Efetue o login como estudante para acessar o mural.")
	st.stop()

# Busca as inscrições atuais do estudante logado
minhas_inscs = [ins["id_evento"] if isinstance(ins, dict) else ins for ins in inscricoes_do_estudante(matricula)]

st.title("🎉 Mural de Eventos")
st.caption("Participe dos eventos extracurriculares organizados pelo RU da UnB.")

eventos = listar_eventos()
if not eventos:
	st.info("Nenhum evento disponível no momento.")
	st.stop()

agora = datetime.now()
proximos, andamento, passados = [], [], []

for ev in eventos:
	try:
		dt_i = datetime.strptime(str(ev["data_inicio"])[:16], "%Y-%m-%d %H:%M")
		dt_f = datetime.strptime(str(ev["data_fim"])[:16], "%Y-%m-%d %H:%M")
		if dt_i > agora:
			proximos.append((ev, dt_i, dt_f))
		elif dt_i <= agora <= dt_f:
			andamento.append((ev, dt_i, dt_f))
		else:
			passados.append((ev, dt_i, dt_f))
	except Exception:
		pass

def render_ev(ev, dt_i, dt_f, badge_label, badge_color, encerrado=False):
	id_ev = int(ev["id_evento"])
	inscrito = id_ev in minhas_inscs
	inscritos = contagem_inscritos(id_ev)
	descricao = str(ev["descricao"])
	
	with st.container(border=True):
		if ev.get("foto_capa"):
			st.image(bytes(ev["foto_capa"]), use_container_width=True)
			
		h1, h2 = st.columns([5, 1])
		h1.markdown(f"**{descricao[:80]}{'...' if len(descricao) > 80 else ''}**")
		h2.metric("Inscritos", inscritos)
		
		c1, c2, c3 = st.columns(3)
		c1.caption(f"📅 {dt_i.strftime('%d/%m/%Y %H:%M')}")
		c2.caption(f"🏁 {dt_f.strftime('%d/%m/%Y %H:%M')}")
		c3.markdown(f":{badge_color}[{badge_label}]")
		
		if not encerrado:
			if inscrito:
				st.success("✅ Você está inscrito neste evento!")
				if st.button("Cancelar minha inscrição", key=f"canc_{id_ev}", type="secondary"):
					if cancelar_inscricao(id_ev, int(matricula)):
						st.success("Inscrição cancelada.")
						st.rerun()
			else:
				if st.button("🎟️ Realizar Inscrição", key=f"insc_{id_ev}", type="primary"):
					if inscrever_estudante(id_ev, int(matricula)):
						st.success("Sua vaga foi garantida! 🎉")
						st.rerun()
					else:
						st.error("Falha ao processar inscrição.")
		else:
			if inscrito:
				st.info("📜 Você participou deste evento.")

if andamento:
	st.subheader("🔵 Acontecendo agora")
	for ev, i, f in andamento: render_ev(ev, i, f, "🔵 Em andamento", "blue")

if proximos:
	st.subheader("🟢 Próximos eventos")
	for ev, i, f in proximos: render_ev(ev, i, f, "🟢 Próximo", "green")

if passados:
	with st.expander(f"⚫ Eventos encerrados ({len(passados)})"):
		for ev, i, f in passados: render_ev(ev, i, f, "⚫ Encerrado", "grey", encerrado=True)