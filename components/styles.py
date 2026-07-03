# vibecodado 100% esse front
"""CSS global reutilizável em todas as páginas."""

BASE_CSS = """
<style>
/* ── Variáveis de cor ────────────────────────── */
:root {
    --verde:      #12bd21;
    --verde-esc:  #0a7a14;
    --verde-bg:   #f0faf1;
    --verde-brd:  #b6e8bc;
    --texto:      #1a1a2e;
}

/* ── Layout geral ───────────────────────────── */
.main .block-container { padding-top: 1.2rem; max-width: 1100px; }
[data-testid="stSidebar"] { background: #0a7a14; }
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.25); }
[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 8px; width: 100%; color: white !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,.28);
}

/* ── Metric cards ───────────────────────────── */
div[data-testid="metric-container"] {
    background: var(--verde-bg);
    border: 1px solid var(--verde-brd);
    border-radius: 10px; padding: .8rem 1rem;
}

/* ── Tabela Matriz ──────────────────────────── */
.mru-wrap { overflow-x: auto; width: 100%; }
.mru-table {
    border-collapse: collapse; width: 100%;
    min-width: 860px; font-size: .8rem;
}
.mru-table th, .mru-table td {
    border: 1.5px solid var(--verde-brd);
    vertical-align: middle;
}
.mru-th-day {
    background: var(--verde-esc); color: white;
    text-align: center; font-weight: 700;
    padding: 7px 4px; font-size: .75rem; white-space: nowrap;
}
.mru-th-per {
    background: #095e10; color: white; text-align: center;
    writing-mode: vertical-rl; transform: rotate(180deg);
    width: 26px; min-width: 26px;
    font-size: .7rem; letter-spacing: 1px; padding: 6px 2px;
}
.mru-th-comp {
    background: #1a8c24; color: white; font-weight: 700;
    font-size: .73rem; padding: 5px 8px;
    min-width: 100px; max-width: 100px;
}
.mru-sep td { height: 4px; background: var(--verde-esc); padding: 0; border: none; }
.mru-cell {
    min-height: 44px; padding: 5px 6px;
    cursor: pointer; transition: background .12s; background: #f8fff8;
}
.mru-cell:hover { background: #c8f5cd !important; }
.mru-cell-filled { background: #e8f9eb !important; }
.mru-badge {
    display: inline-block; background: #d4f5d8;
    border: 1px solid #7edd8a; border-radius: 5px;
    padding: 2px 7px; margin: 2px 1px;
    font-size: .72rem; color: #0a5e11;
    white-space: nowrap; max-width: 130px;
    overflow: hidden; text-overflow: ellipsis;
}

/* ── Hero da Home ───────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0a7a14 0%, #12bd21 100%);
    border-radius: 16px; padding: 3rem 2.5rem;
    color: white; text-align: center; margin-bottom: 2rem;
}
.hero h1 { font-size: 2.6rem; font-weight: 800; margin: 0; }
.hero p  { font-size: 1.1rem; opacity: .9; margin: .5rem 0 0; }

/* ── Cards de feature na Home ───────────────── */
.feat-card {
    background: white; border: 1.5px solid var(--verde-brd);
    border-radius: 12px; padding: 1.4rem 1.2rem;
    text-align: center; height: 100%;
    transition: box-shadow .2s, transform .2s;
}
.feat-card:hover { box-shadow: 0 6px 20px rgba(18,189,33,.2); transform: translateY(-2px); }
.feat-icon { font-size: 2.2rem; margin-bottom: .5rem; }
.feat-card h3 { color: var(--verde-esc); margin: .3rem 0; font-size: 1rem; }
.feat-card p  { color: #555; font-size: .85rem; margin: 0; }

/* ── Tag de notificação ─────────────────────── */
.notif-badge {
    background: #fff3b0; border: 1px solid #e6a800;
    border-radius: 20px; padding: 4px 12px;
    font-size: .78rem; color: #7a5800; display: inline-block;
}
</style>
"""

def inject(extra: str = ""):
    import streamlit as st
    st.markdown(BASE_CSS + extra, unsafe_allow_html=True)
