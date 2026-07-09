import streamlit as st
from datetime import datetime
from components.styles import inject
from database.evento_db import listar_eventos, contagem_inscritos

inject()
user_sessao = st.session_state.get('usuario', {})
if not user_sessao:
	st.stop()

st.title("🎉 Eventos")
st.caption("Próximas atividades e eventos do RU")

eventos = listar_eventos()
if not eventos:
	st.info("Nenhum evento disponível no momento.")
	st.stop()

agora = datetime.now()
proximos, andamento = [], []
for ev in eventos:
	try:
		dt_i = datetime.strptime(str(ev["data_inicio"])[:16], "%Y-%m-%d %H:%M")
		dt_f = datetime.strptime(str(ev["data_fim"])[:16], "%Y-%m-%d %H:%M")
		if dt_i > agora:
			proximos.append((ev, dt_i, dt_f))
		elif dt_i <= agora <= dt_f:
			andamento.append((ev, dt_i, dt_f))
	except Exception:
		pass

st.subheader("🔵 Acontecendo agora")
if andamento:
	for ev, dt_i, dt_f in andamento:
		with st.container(border=True):
			c1, c2 = st.columns([5, 1])
			with c1:
				if ev.get("foto_capa"):
					st.image(bytes(ev["foto_capa"]), width=200)
				st.markdown(f"**{str(ev['descricao'])[:80]}**")
			c2.metric("Inscritos", contagem_inscritos(ev["id_evento"]))
			st.caption(f"{dt_i.strftime('%d/%m/%Y %H:%M')} → {dt_f.strftime('%d/%m/%Y %H:%M')}")
else:
	st.caption("Sem eventos em andamento.")

st.markdown("---")
st.subheader("🟢 Próximos eventos")
if proximos:
	for ev, dt_i, dt_f in proximos:
		with st.container(border=True):
			c1, c2 = st.columns([5, 1])
			with c1:
				if ev.get("foto_capa"):
					st.image(bytes(ev["foto_capa"]), width=200)
				st.markdown(f"**{str(ev['descricao'])[:80]}**")
			c2.metric("Inscritos", contagem_inscritos(ev["id_evento"]))
			st.caption(f"{dt_i.strftime('%d/%m/%Y %H:%M')} → {dt_f.strftime('%d/%m/%Y %H:%M')}")
else:
	st.caption("Sem eventos futuros.")