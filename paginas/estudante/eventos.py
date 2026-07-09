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
	st.stop()

minhas_inscs = inscricoes_do_estudante(matricula)

st.title("🎉 Mural de Eventos")
st.caption("Eventos culturais e extracurriculares organizados pelo RU da UnB.")

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
	inscrito = ev["id_evento"] in minhas_inscs
	inscritos = contagem_inscritos(ev["id_evento"])
	descricao = str(ev["descricao"])
	with st.container(border=True):
		h1, h2 = st.columns([5, 1])
		h1.markdown(f"**{descricao[:80]}{'...' if len(descricao) > 80 else ''}**")
		h2.metric("Inscritos", inscritos)
		c1, c2, c3 = st.columns(3)
		c1.caption(f"📅 {dt_i.strftime('%d/%m/%Y %H:%M')}")
		c2.caption(f"🏁 {dt_f.strftime('%d/%m/%Y %H:%M')}")
		c3.markdown(f":{badge_color}[{badge_label}]")
		if not encerrado:
			if inscrito:
				st.success("✅ Você está inscrito!")
				if st.button("Cancelar inscrição", key=f"canc_{ev['id_evento']}"):
					cancelar_inscricao(ev["id_evento"], matricula)
					st.rerun()
			else:
				if st.button("🎟️ Inscrever-se", key=f"insc_{ev['id_evento']}", type="primary"):
					ok = inscrever_estudante(ev["id_evento"], matricula)
					if ok:
						st.success("Inscrito! 🎉")
						st.rerun()
					else:
						st.warning("Já inscrito ou indisponível no momento.")
		else:
			if inscrito:
				st.info("📜 Você participou deste evento.")


if andamento:
	st.subheader("🔵 Acontecendo agora")
	for ev, i, f in andamento:
		render_ev(ev, i, f, "🔵 Em andamento", "blue")
	st.markdown("---")

if proximos:
	st.subheader("🟢 Próximos eventos")
	for ev, i, f in proximos:
		render_ev(ev, i, f, "🟢 Próximo", "green")
	st.markdown("---")

if passados:
	with st.expander(f"⚫ Eventos encerrados ({len(passados)})"):
		for ev, i, f in passados:
			render_ev(ev, i, f, "⚫ Encerrado", "grey", encerrado=True)

if minhas_inscs:
	st.markdown("---")
	st.subheader(f"🎟️ Minhas inscrições ({len(minhas_inscs)})")
	todos = {ev["id_evento"]: ev for ev in eventos}
	for eid in minhas_inscs:
		ev = todos.get(eid)
		if ev:
			st.markdown(f"• **#{eid}** – {str(ev['descricao'])[:70]}")