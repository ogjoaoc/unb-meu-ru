# 100% vibecodado
import streamlit as st
from datetime import date, timedelta
import random
from components.styles import inject
from database.cardapio_db import (
    listar_itens_cardapio, listar_categorias,
    cardapio_ativo, listar_cardapios, itens_do_cardapio,
    cardapio_no_periodo, criar_cardapio, adicionar_item_ao_cardapio, remover_item_do_cardapio,
    publicar_cardapio, adicionar_item_catalogo, excluir_item_catalogo,
    feedbacks_do_cardapio, media_notas_cardapio, relatorio_desempenho_cardapios
)

inject()

DIAS     = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
DIAS_PT  = {"Segunda":"2ª FEIRA","Terca":"3ª FEIRA","Quarta":"4ª FEIRA",
            "Quinta":"5ª FEIRA","Sexta":"6ª FEIRA","Sabado":"SÁBADO","Domingo":"DOMINGO"}
PERIODOS    = ["Cafe","Almoco","Jantar"]
PERIODOS_PT = {"Cafe":"☕ Café da Manhã","Almoco":"🍽️ Almoço","Jantar":"🌙 Jantar"}
CATS_DEFAULT = {
    "Cafe":   ["Bebida","Panificação","Complemento","Fruta"],
    "Almoco": ["Prato Principal","Guarnição","Salada","Bebida","Sobremesa"],
    "Jantar": ["Prato Principal","Guarnição","Salada","Bebida"],
}


def v(reg, key):
    return reg.get(key)


def titulo_resumido(nome):
    return f"{nome[:17]}…" if len(nome) > 17 else nome

# Pegar ID do nutricionista logado
user_sessao = st.session_state.get('usuario', {})
id_nutricionista_logado = user_sessao.get('id_nutricionista')

if not user_sessao or st.session_state.get('cargo') not in ("nutricionista", "gerente"):
    st.stop()

# ── Modal de edição de célula ─────────────────────────────────────────────────
@st.dialog("✏️ Editar célula", width="large")
def modal_celula(cid: int, dia: str, periodo: str, cat: str):
    st.markdown(
        f"<div style='background:#e8f9eb;border-left:4px solid #12bd21;"
        f"border-radius:6px;padding:.6rem 1rem;margin-bottom:1rem'>"
        f"<b style='color:#0a7a14'>{DIAS_PT.get(dia,dia)}</b>"
        f" &nbsp;·&nbsp; {PERIODOS_PT.get(periodo,periodo)}"
        f" &nbsp;·&nbsp; <b>{cat}</b></div>",
        unsafe_allow_html=True,
    )
    todos        = listar_itens_cardapio()
    opcoes_cat   = [i for i in todos if i["categoria"] == cat]
    itens_celula = [
        i for i in itens_do_cardapio(cid)
        if i["dia_semana"] == dia and i["periodo"] == periodo and i["categoria"] == cat
    ]
    ja = {it["nome"] for it in itens_celula}

    col_add, col_rem = st.columns([3, 2])
    with col_add:
        st.markdown("**Adicionar**")
        if not opcoes_cat:
            st.warning(f"Nenhum item cadastrado em **{cat}**.")
        else:
            disp = [i["nome"] for i in opcoes_cat if i["nome"] not in ja]
            if disp:
                escolha = st.selectbox(f"Escolher {cat}:", disp)
                composicao = st.text_input("Composição (Ex: Prato principal, Opção vegana)", value=cat)
                if st.button("➕ Adicionar", type="primary", use_container_width=True):
                    obj = next(i for i in opcoes_cat if i["nome"] == escolha)
                    adicionar_item_ao_cardapio(cid, obj["id_itemcardapio"], periodo, dia, composicao)
                    st.rerun()
            else:
                st.success("Todos os itens já adicionados nesta célula.")

    with col_rem:
        st.markdown("**Itens na célula**")
        if not itens_celula:
            st.info("Célula vazia.")
        else:
            for it in itens_celula:
                c1, c2 = st.columns([5,1])
                c1.markdown(f"• **{it['nome']}** <small>({it['composicao']})</small>", unsafe_allow_html=True)
                
                # 🛠️ CORREÇÃO DA CHAVE: Removido o random.randint para estabilizar o clique do botão
                chave_estatica = f"rm_{cid}_{it['id_itemcardapio']}_{dia}_{periodo}_{it['composicao'].replace(' ', '_')}"
                if c2.button("🗑️", key=chave_estatica):
                    remover_item_do_cardapio(cid, it["id_itemcardapio"], periodo, dia, it["composicao"])
                    st.rerun()


# ── Modal de novo cardápio ────────────────────────────────────────────────────
@st.dialog("➕ Novo cardápio", width="small")
def modal_novo_cardapio():
    st.markdown("Defina o período do novo cardápio.")
    n1, n2 = st.columns(2)
    dt_ini = n1.date_input("Início", value=date.today())
    dt_fim = n2.date_input("Fim",    value=date.today() + timedelta(days=6))
    if st.button("Criar", type="primary", use_container_width=True):
        if not id_nutricionista_logado:
            st.error("Este cadastro exige um nutricionista logado para vincular o cardápio.")
            return
        if cardapio_no_periodo(str(dt_ini), str(dt_fim)):
            st.warning("Já existe um cardápio nesse período. Edite o existente em vez de criar outro.")
            return
        cid = random.randint(1000, 9999)
        if criar_cardapio(cid, str(dt_ini), str(dt_fim), id_nutricionista_logado):
            st.success(f"Cardápio #{cid} criado!")
            st.rerun()


# ── Modal adicionar item ao catálogo ─────────────────────────────────────────
@st.dialog("📦 Novo item no catálogo", width="small")
def modal_novo_item():
    ca1, ca2 = st.columns(2)
    nome_item = ca1.text_input("Nome do item")
    cats_ex   = listar_categorias()
    cat_sel   = ca2.selectbox("Categoria", cats_ex + ["(Nova categoria...)"])
    cat_nova  = ""
    if cat_sel == "(Nova categoria...)":
        cat_nova = st.text_input("Nome da nova categoria")
    if st.button("Adicionar", type="primary", use_container_width=True):
        cat_f = cat_nova.strip() if cat_sel == "(Nova categoria...)" else cat_sel
        if nome_item.strip() and cat_f:
            if not id_nutricionista_logado:
                st.error("Este cadastro exige um nutricionista logado para vincular o item ao catálogo.")
                return
            id_item = random.randint(10000, 99999)
            if adicionar_item_catalogo(id_item, cat_f, nome_item.strip(), id_nutricionista_logado):
                st.success(f"'{nome_item}' adicionado!")
                st.rerun()
        else:
            st.error("Preencha nome e categoria.")


# ─────────────────────────────────────────────────────────────────────────────
st.title("📅 Painel do Nutricionista")

tabs = st.tabs(["🗓️ Matriz de Edição","📋 Visualizar Publicado","📦 Catálogo Geral","💬 Feedbacks"])

# ════════ TAB 1 — MATRIZ ═════════════════════════════════════════════════════
with tabs[0]:
    cardapios  = listar_cardapios(8)
    opcoes_map = {
        f"#{c['id_cardapio']} · {str(c['data_inicio'])} → {str(c['data_fim'])}  "
        f"{'✅' if c['status'] == 'Publicado' else '📝'}": c["id_cardapio"]
        for c in cardapios
    }

    if not opcoes_map:
        st.info("Nenhum cardápio registrado no banco ainda.")
        if st.button("➕ Criar Primeiro Cardápio", type="primary"):
            modal_novo_cardapio()
        st.stop()

    tb1, tb2, tb3 = st.columns([4, 1, 1])
    escolha = tb1.selectbox("Selecionar cardápio:", list(opcoes_map.keys()), label_visibility="collapsed")

    if tb2.button("➕ Novo", use_container_width=True):
        modal_novo_cardapio()

    cid_sel      = opcoes_map[escolha]
    info_card    = next(c for c in cardapios if c["id_cardapio"] == cid_sel)
    itens_atuais = itens_do_cardapio(cid_sel)
    dias_almoco  = {i["dia_semana"] for i in itens_atuais if i["periodo"] == "Almoco"}

    with tb3:
        if info_card["status"] != "Publicado":
            if st.button("🚀 Publicar", type="primary", use_container_width=True):
                publicar_cardapio(cid_sel)
                st.success("Publicado!")
                st.rerun()
        else:
            st.success("✅ Publicado")

        st.caption("💡 Clique em uma célula para adicionar ou remover itens.")

    grade: dict = {}
    for item in itens_atuais:
        key = (item["periodo"], item["dia_semana"], item["categoria"])
        grade.setdefault(key, []).append(item["nome"])

    cats_por_periodo: dict = {}
    for p in PERIODOS:
        extras = sorted({i["categoria"] for i in itens_atuais if i["periodo"] == p})
        cats_por_periodo[p] = list(dict.fromkeys(CATS_DEFAULT.get(p,[]) + extras))

    def badge(nome):
        return f'<span class="mru-badge" title="{nome}">{titulo_resumido(nome)}</span>'

    header = (
        "<tr>"
        "<th style='border:none;background:white;min-width:26px'></th>"
        "<th class='mru-th-day' style='min-width:100px;text-align:left;padding-left:8px'>COMPOSIÇÃO</th>"
        + "".join(f"<th class='mru-th-day'>{DIAS_PT[d]}</th>" for d in DIAS)
        + "</tr>"
    )

    body = []
    for periodo in PERIODOS:
        cats   = cats_por_periodo[periodo]
        n_cats = len(cats)
        for idx, cat in enumerate(cats):
            row = "<tr>"
            if idx == 0:
                row += f'<td class="mru-th-per" rowspan="{n_cats}">{PERIODOS_PT[periodo]}</td>'
            row += f'<td class="mru-th-comp">{cat.upper()}</td>'
            for dia in DIAS:
                items_c = grade.get((periodo, dia, cat), [])
                filled  = "mru-cell-filled" if items_c else ""
                content = ("".join(badge(n) for n in items_c)
                           if items_c
                           else '<span style="color:#ccc;font-size:.7rem">—</span>')
                row += f'<td class="mru-cell {filled}">{content}</td>'
            row += "</tr>"
            body.append(row)
        body.append(f'<tr class="mru-sep"><td colspan="{2+len(DIAS)}"></td></tr>')

    st.markdown(
        f'<div class="mru-wrap"><table class="mru-table">'
        f'{header}{"".join(body)}</table></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    for periodo in PERIODOS:
        cats = cats_por_periodo[periodo]
        st.markdown(
            f"<div style='background:#0a7a14;color:white;padding:3px 12px;"
            f"border-radius:5px;font-size:.78rem;font-weight:700;"
            f"margin:8px 0 4px;display:inline-block'>"
            f"{PERIODOS_PT[periodo]}</div>",
            unsafe_allow_html=True,
        )
        h = st.columns([1.15] + [1]*len(DIAS))
        h[0].markdown("<div style='font-size:.7rem;font-weight:700;color:#555;padding:2px 4px'>COMPOSIÇÃO</div>",
                      unsafe_allow_html=True)
        for i, dia in enumerate(DIAS):
            h[i+1].markdown(
                f"<center style='font-size:.68rem;font-weight:700;color:#0a7a14'>{DIAS_PT[dia]}</center>",
                unsafe_allow_html=True,
            )

        for cat in cats:
            rc = st.columns([1.15] + [1]*len(DIAS))
            rc[0].markdown(
                f"<div style='font-size:.72rem;font-weight:600;color:#0a5e11;padding:3px 4px'>{cat}</div>",
                unsafe_allow_html=True,
            )
            for i, dia in enumerate(DIAS):
                items_c = grade.get((periodo, dia, cat), [])
                label   = "✅" if items_c else "＋"
                if rc[i+1].button(
                    label,
                    key=f"btn_{periodo}_{dia}_{cat}",
                    use_container_width=True,
                    type="primary" if items_c else "secondary",
                    help=(", ".join(items_c) if items_c else f"Adicionar {cat} — {DIAS_PT[dia]}"),
                ):
                    modal_celula(cid_sel, dia, periodo, cat)
        st.markdown("---")


with tabs[1]:
    ativo = cardapio_ativo()
    if not ativo:
        st.info("Nenhum cardápio publicado no momento.")
    else:
        cid = ativo["id_cardapio"]
        media, total = media_notas_cardapio(cid)
        c1,c2,c3 = st.columns(3)
        c1.metric("Período", f"{str(ativo['data_inicio'])} → {str(ativo['data_fim'])}")
        c2.metric("⭐ Nota média",  f"{media}/5" if media else "—")
        c3.metric("💬 Feedbacks", total)
        
        itens_pub = itens_do_cardapio(cid)
        for dia in DIAS:
            d_its = [i for i in itens_pub if i["dia_semana"] == dia]
            if not d_its: continue
            st.subheader(f"📆 {DIAS_PT[dia]}")
            for per in PERIODOS:
                p_its = [i for i in d_its if i["periodo"] == per]
                if not p_its: continue
                with st.expander(PERIODOS_PT[per], expanded=(per=="Almoco")):
                    por_cat: dict = {}
                    for it in p_its:
                        por_cat.setdefault(it["categoria"],[]).append(it["nome"])
                    cols = st.columns(max(1,len(por_cat)))
                    for idx,(cat,nomes) in enumerate(por_cat.items()):
                        with cols[idx%len(cols)]:
                            st.markdown(f"**{cat}**")
                            for n in nomes: st.markdown(f"• {n}")

# ════════ TAB 2 — CATÁLOGO GERAL ═════════════════════════════════════════════
with tabs[2]:
    col_title, col_btn = st.columns([4,1])
    col_title.subheader("Catálogo de Itens do Sistema")
    if col_btn.button("➕ Novo item no Catálogo", type="primary", use_container_width=True):
        modal_novo_item()

    st.markdown("---")
    for cat in listar_categorias():
        itens_c = [i for i in listar_itens_cardapio() if i["categoria"] == cat]
        with st.expander(f"**{cat}** ({len(itens_c)} itens)"):
            for i in itens_c:
                # ➕ ADICIONADO: Divisão em colunas para comportar o botão de deletar o item do catálogo
                c1, c2 = st.columns([6, 1])
                c1.markdown(f"• {i['nome']}")
                
                # Botão de lixeira acionando o CASCADE do banco de dados
                if c2.button("🗑️", key=f"del_catalogo_{i['id_itemcardapio']}", help=f"Remover '{i['nome']}' permanentemente"):
                    if excluir_item_catalogo(i['id_itemcardapio']):
                        st.success(f"'{i['nome']}' removido do catálogo e dos cardápios com sucesso!")
                        st.rerun()
                    else:
                        st.error("Não foi possível excluir o item do catálogo.")

with tabs[3]:
    st.subheader("Feedbacks Coletados")
    ativo2 = cardapio_ativo()
    if not ativo2:
        st.info("Nenhum cardápio ativo para listar avaliações.")
    else:
        fbs = feedbacks_do_cardapio(ativo2["id_cardapio"])
        m2, t2 = media_notas_cardapio(ativo2["id_cardapio"])
        fc1,fc2 = st.columns(2)
        fc1.metric("⭐ Nota Média Atual", f"{m2}/5" if m2 else "–")
        fc2.metric("Total feedbacks", t2)
        st.markdown("---")
        if not fbs:
            st.info("Nenhum feedback registrado para esta semana.")
        else:
            for fb in fbs:
                stars = "⭐"*fb["nota"] + "☆"*(5-fb["nota"])
                st.markdown(f"**Estudante (Matrícula: {fb['matricula']})** – {stars}")
                st.caption(fb["descricao"] or "*(sem comentário)*")
                st.markdown("---")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Painel Histórico de Desempenho")
        st.caption("Métricas gerenciais consolidadas diretamente da **VIEW nativa** (`vw_desempenho_cardapio`).")

        dados_view = relatorio_desempenho_cardapios()
        
        if not dados_view:
            st.info("Nenhum histórico de desempenho gerado pela View até o momento.")
        else:
            import pandas as pd
            df_view = pd.DataFrame(dados_view)
            
            df_view.columns = [
                "ID Cardápio", "Data Início", "Data Fim", "Status", 
                "Nutricionista Responsável", "Total Avaliações", "Nota Média"
            ]
            
            st.dataframe(df_view, use_container_width=True, hide_index=True)