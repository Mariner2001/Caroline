#!/usr/bin/env python3
"""
Análisis cuantitativo — caso Sabadell 2015.
Genera todos los resultados numéricos y figuras del paper.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
from scipy import stats

rng = np.random.default_rng(20150315)

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "figure.dpi": 150, "savefig.bbox": "tight", "axes.grid": True,
    "grid.alpha": 0.25, "axes.axisbelow": True,
})

OUT = {}

# =====================================================================
# GEOMETRÍA REAL
# =====================================================================
LAT0 = 41.5336445
MPERDEG_LAT = 111_320.0
MPERDEG_LON = 111_320.0 * np.cos(np.radians(LAT0))

def to_xy(lat, lon):
    return (np.array([(lon - 2.0998452) * MPERDEG_LON,
                      (lat - LAT0) * MPERDEG_LAT]))

P_ZH   = to_xy(41.5336445, 2.0998452)   # Zona Hermética (origen)
P_SUD  = to_xy(41.5287051, 2.1054052)   # estación Sabadell Sud
P_FEU  = to_xy(41.5393237, 2.0936818)   # Castell de Can Feu
P_CEN  = to_xy(41.5464246, 2.1156055)   # estación Sabadell Centre

d_ZH_SUD = np.linalg.norm(P_SUD - P_ZH)
d_ZH_FEU = np.linalg.norm(P_FEU - P_ZH)
d_FEU_SUD = np.linalg.norm(P_SUD - P_FEU)
d_ZH_CEN = np.linalg.norm(P_CEN - P_ZH)

OUT["geom"] = dict(d_ZH_SUD=d_ZH_SUD, d_ZH_FEU=d_ZH_FEU,
                   d_FEU_SUD=d_FEU_SUD, d_ZH_CEN=d_ZH_CEN)

print("=" * 62)
print("GEOMETRÍA (metros, distancia euclídea)")
print("=" * 62)
print(f"  Zona Hermética -> Sabadell Sud   : {d_ZH_SUD:8.1f}")
print(f"  Zona Hermética -> Castell Can Feu: {d_ZH_FEU:8.1f}")
print(f"  Castell Can Feu -> Sabadell Sud  : {d_FEU_SUD:8.1f}")
print(f"  Zona Hermética -> Sabadell Centre: {d_ZH_CEN:8.1f}")

# =====================================================================
# 1. MONTE CARLO TEMPORAL — holgura no explicada
# =====================================================================
N = 400_000

# t3: dispersión policial. Soporte 04:30-05:15, moda 05:00 (triangular)
t3 = rng.triangular(4.50, 5.00, 5.25, N)          # horas decimales
# t4: llamada saliente. Dos valores publicados (05:45 / 05:55) + jitter
pick = rng.random(N) < 0.5
t4 = np.where(pick, 5.75, 5.9167) + rng.normal(0, 0.0139, N)   # sd 50 s
dt_h = t4 - t3
dt_min = dt_h * 60.0

# marcha: log-normal media 1.35 m/s, sd 0.22
sigma_ln = np.sqrt(np.log(1 + (0.22 / 1.35) ** 2))
mu_ln = np.log(1.35) - 0.5 * sigma_ln ** 2
V = rng.lognormal(mu_ln, sigma_ln, N)
kappa = rng.uniform(1.15, 1.45, N)

t_walk_min = (kappa * d_ZH_SUD / V) / 60.0
slack = dt_min - t_walk_min
v_req = kappa * d_ZH_SUD / (dt_min * 60.0)

OUT["mc_time"] = dict(
    dt_med=np.median(dt_min), dt_q=np.percentile(dt_min, [5, 95]),
    walk_med=np.median(t_walk_min), walk_q=np.percentile(t_walk_min, [5, 95]),
    slack_med=np.median(slack), slack_q=np.percentile(slack, [5, 95]),
    p_slack_20=(slack > 20).mean(), p_slack_30=(slack > 30).mean(),
    p_slack_45=(slack > 45).mean(),
    vreq_med=np.median(v_req), vreq_q=np.percentile(v_req, [5, 95]),
    p_infeasible=(v_req > V).mean(),
)
m = OUT["mc_time"]
print("\n" + "=" * 62)
print("1. MONTE CARLO TEMPORAL  (N = %d)" % N)
print("=" * 62)
print(f"  Tiempo disponible dt   : mediana {m['dt_med']:5.1f} min   "
      f"IC90 [{m['dt_q'][0]:.1f}, {m['dt_q'][1]:.1f}]")
print(f"  Tiempo de marcha       : mediana {m['walk_med']:5.1f} min   "
      f"IC90 [{m['walk_q'][0]:.1f}, {m['walk_q'][1]:.1f}]")
print(f"  HOLGURA                : mediana {m['slack_med']:5.1f} min   "
      f"IC90 [{m['slack_q'][0]:.1f}, {m['slack_q'][1]:.1f}]")
print(f"  P(holgura > 20 min)    : {m['p_slack_20']:.4f}")
print(f"  P(holgura > 30 min)    : {m['p_slack_30']:.4f}")
print(f"  P(holgura > 45 min)    : {m['p_slack_45']:.4f}")
print(f"  Velocidad requerida    : mediana {m['vreq_med']:.3f} m/s  "
      f"IC90 [{m['vreq_q'][0]:.3f}, {m['vreq_q'][1]:.3f}]")
print(f"  P(trayecto INVIABLE a pie) : {m['p_infeasible']:.5f}")

# ---- Figura 1
fig, ax = plt.subplots(1, 3, figsize=(10.6, 2.9))
ax[0].hist(dt_min, bins=120, color="#3d6ea8", alpha=.85, density=True)
ax[0].set_xlabel("tiempo disponible $\\Delta t$ (min)")
ax[0].set_ylabel("densidad"); ax[0].set_title("(a) Ventana temporal")
ax[1].hist(t_walk_min, bins=120, color="#2f8f5b", alpha=.85, density=True)
ax[1].set_xlabel("tiempo de marcha requerido (min)")
ax[1].set_title("(b) Trayecto a pie, 720 m")
ax[2].hist(slack, bins=140, color="#c2521a", alpha=.85, density=True)
ax[2].axvline(0, color="k", lw=1, ls="--")
ax[2].axvline(np.median(slack), color="darkred", lw=1.4)
ax[2].set_xlabel("holgura no explicada (min)")
ax[2].set_title("(c) Residuo temporal")
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("fig1_tiempo.pdf"); plt.close()

# =====================================================================
# 2. SIMULACIÓN DE RED CELULAR — velocidad aparente de un móvil casi quieto
# =====================================================================
def hex_sites(isd, extent=6000.0):
    """Retícula hexagonal de emplazamientos."""
    dy = isd * np.sqrt(3) / 2
    pts = []
    ny = int(extent / dy) + 2
    nx = int(extent / isd) + 2
    for j in range(-ny, ny + 1):
        off = (isd / 2) if (j % 2) else 0.0
        for i in range(-nx, nx + 1):
            pts.append((i * isd + off, j * dy))
    p = np.array(pts)
    return p[np.linalg.norm(p, axis=1) < extent]

def sector_gain(dx, dy, az_deg):
    """Patrón 3GPP de sector: 3 sectores de 120 grados."""
    ang = np.degrees(np.arctan2(dy, dx))
    d = (ang - az_deg + 180) % 360 - 180
    return -np.minimum(12 * (d / 65.0) ** 2, 20.0)

def simulate_apparent_velocity(isd, move_radius, n_runs=6000,
                               n_events=6, sigma_sh=8.0, hyst_db=3.0,
                               dcorr=25.0, dt_mean_s=180.0):
    """
    Móvil CASI ESTÁTICO. Devuelve las velocidades aparentes que un analista
    inferiría al dividir la separación entre emplazamientos por el intervalo.
    """
    sites = hex_sites(isd)
    az = np.array([0.0, 120.0, 240.0])
    app_v, true_v = [], []

    for _ in range(n_runs):
        # posición base aleatoria dentro de la retícula
        c = rng.uniform(-isd, isd, 2)
        # sombra fija por (sitio, sector) en la posición base
        base_shadow = rng.normal(0, sigma_sh, (len(sites), 3))

        # trayectoria: paseo aleatorio corto (persona parada / deambulando)
        steps = rng.normal(0, move_radius / np.sqrt(n_events), (n_events, 2))
        pos = c + np.cumsum(steps, axis=0)

        # instantes de registro
        gaps = rng.exponential(dt_mean_s, n_events - 1)
        gaps = np.clip(gaps, 20.0, 1800.0)
        times = np.concatenate([[0.0], np.cumsum(gaps)])

        serving = []
        for k in range(n_events):
            dx = pos[k, 0] - sites[:, 0]
            dy = pos[k, 1] - sites[:, 1]
            d = np.maximum(np.hypot(dx, dy), 25.0)
            pl = 128.1 + 37.6 * np.log10(d / 1000.0)
            # decorrelación de sombra por desplazamiento
            drift = np.linalg.norm(pos[k] - c)
            rho = np.exp(-drift / dcorr)
            sh = (rho * base_shadow +
                  np.sqrt(max(1 - rho ** 2, 0)) *
                  rng.normal(0, sigma_sh, base_shadow.shape))
            g = np.stack([sector_gain(dx, dy, a) for a in az], axis=1)
            prx = (43.0 + g - pl[:, None] - sh)
            idx = np.unravel_index(np.argmax(prx), prx.shape)
            best = (idx[0], idx[1]); bestval = prx[idx]
            if serving:
                pi, si = serving[-1]
                if prx[pi, si] > bestval - hyst_db:
                    best = (pi, si)
            serving.append(best)

        for k in range(1, n_events):
            a, b = serving[k - 1][0], serving[k][0]
            if a != b:
                sep = np.linalg.norm(sites[a] - sites[b])
                dt = times[k] - times[k - 1]
                app_v.append(sep / dt * 3.6)
                true_v.append(np.linalg.norm(pos[k] - pos[k - 1]) / dt * 3.6)
    return np.array(app_v), np.array(true_v)

print("\n" + "=" * 62)
print("2. RED CELULAR — velocidad APARENTE de un terminal casi estático")
print("=" * 62)
print(f"{'ISD (m)':>8} {'desplaz. real':>14} {'n handovers':>12} "
      f"{'v.ap. mediana':>14} {'P(v.ap>80)':>11} {'P(v.ap>40)':>11}")

cell_rows = []
for isd in (500, 800, 1200):
    for mv in (0.0, 50.0, 150.0):
        av, tv = simulate_apparent_velocity(isd, mv, n_runs=2500)
        if len(av) == 0:
            continue
        row = dict(isd=isd, mv=mv, n=len(av), med=np.median(av),
                   p80=(av > 80).mean(), p40=(av > 40).mean(),
                   true_med=np.median(tv), p99=np.percentile(av, 99))
        cell_rows.append(row)
        print(f"{isd:>8} {mv:>12.0f} m {len(av):>12} "
              f"{np.median(av):>12.1f} km/h {(av>80).mean():>10.3f} "
              f"{(av>40).mean():>10.3f}")
OUT["cell"] = cell_rows

# Caso de referencia para la figura
av_ref, tv_ref = simulate_apparent_velocity(800, 50.0, n_runs=9000)
OUT["cell_ref"] = dict(n=len(av_ref), med=np.median(av_ref),
                       p80=(av_ref > 80).mean(),
                       true_med=np.median(tv_ref),
                       true_p95=np.percentile(tv_ref, 95))
print(f"\n  Caso de referencia (ISD 800 m, desplazamiento real ~50 m):")
print(f"    velocidad REAL mediana      : {np.median(tv_ref):6.2f} km/h")
print(f"    velocidad APARENTE mediana  : {np.median(av_ref):6.1f} km/h")
print(f"    P(velocidad aparente > 80)  : {(av_ref>80).mean():.4f}")
print(f"    factor de exageración       : {np.median(av_ref)/max(np.median(tv_ref),1e-9):6.1f}x")

# curva analítica: qué separación/intervalo genera 80 km/h
seps = np.linspace(200, 4000, 400)
dt_for_80 = seps / (80 / 3.6)

fig, ax = plt.subplots(1, 3, figsize=(10.6, 3.0))
ax[0].hist(np.clip(av_ref, 0, 300), bins=90, color="#8c3b8c",
           alpha=.85, density=True)
ax[0].axvline(80, color="crimson", lw=1.6, ls="--")
ax[0].text(84, ax[0].get_ylim()[1]*.75, "80 km/h", color="crimson", fontsize=8)
ax[0].set_xlabel("velocidad aparente (km/h)"); ax[0].set_ylabel("densidad")
ax[0].set_title("(a) Móvil casi quieto: v. inferida")

ax[1].hist(np.clip(tv_ref, 0, 12), bins=70, color="#2f8f5b", alpha=.85,
           density=True)
ax[1].set_xlabel("velocidad real (km/h)")
ax[1].set_title("(b) Su desplazamiento real")

ax[2].plot(seps, dt_for_80, color="#c2521a", lw=1.8)
ax[2].fill_between(seps, 0, dt_for_80, color="#c2521a", alpha=.13)
ax[2].scatter([2000], [90], color="k", zorder=5, s=22)
ax[2].annotate("2 km entre antenas,\n90 s entre registros\n$\\to$ 80 km/h",
               (2000, 90), textcoords="offset points", xytext=(-8, 26),
               fontsize=7.5, ha="center")
ax[2].set_xlabel("separación entre emplazamientos (m)")
ax[2].set_ylabel("intervalo entre registros (s)")
ax[2].set_title("(c) Combinaciones que dan 80 km/h")
ax[2].set_ylim(0, 180)
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("fig2_celular.pdf"); plt.close()

# =====================================================================
# 3. BÚSQUEDA BAYESIANA — mapa posterior
# =====================================================================
GR = 40.0
lim = 3000.0
gx = np.arange(-lim, lim + GR, GR)
gy = np.arange(-lim, lim + GR, GR)
GX, GY = np.meshgrid(gx, gy)

def rad(P):
    return np.hypot(GX - P[0], GY - P[1])

r_zh = rad(P_ZH)

# --- A priori: escenario peatonal. Difusión desde el punto de dispersión
#     durante la holgura, con decaimiento gamma calibrado al tiempo disponible.
v_typ = 1.15                       # m/s efectivo incluyendo paradas
t_slack_s = np.median(slack) * 60
scale = v_typ * t_slack_s / 3.0
prior_ped = stats.gamma.pdf(r_zh, a=2.0, scale=scale)

# corrección de accesibilidad: la llamada ancla masa cerca del corredor ZH-Sud
seg = P_SUD - P_ZH
L = np.linalg.norm(seg); u = seg / L
proj = ((GX - P_ZH[0]) * u[0] + (GY - P_ZH[1]) * u[1])
perp = np.abs(-(GX - P_ZH[0]) * u[1] + (GY - P_ZH[1]) * u[0])
corridor = np.exp(-(perp / 400.0) ** 2) * np.exp(
    -((np.clip(proj, 0, L) - proj) / 600.0) ** 2)
prior = prior_ped * (0.35 + 0.65 * corridor)
prior /= prior.sum()

# --- Batidas infructuosas documentadas públicamente
#     lambda*z = esfuerzo efectivo; depende de la detectabilidad del terreno
searches = [
    dict(name="Entorno inmediato zona ocio (150 m)", P=P_ZH, R=150.0, lz=2.5),
    dict(name="Castell de Can Feu y entorno",        P=P_FEU, R=350.0, lz=1.2),
    dict(name="Corredor viario ZH-estación",         P=(P_ZH+P_SUD)/2, R=400.0, lz=0.8),
]
post = prior.copy()
mass_before = []
for s in searches:
    m_before = post[rad(np.asarray(s["P"])) <= s["R"]].sum()
    mass_before.append(m_before)
    att = np.where(rad(np.asarray(s["P"])) <= s["R"], np.exp(-s["lz"]), 1.0)
    post = post * att
    post /= post.sum()

print("\n" + "=" * 62)
print("3. BÚSQUEDA BAYESIANA")
print("=" * 62)
print("  Batidas infructuosas y masa de probabilidad afectada:")
for s, mb in zip(searches, mass_before):
    resid = np.exp(-s["lz"])
    print(f"    {s['name']:<38} masa previa {mb*100:5.1f}%  "
          f"retiene {resid*100:4.1f}%  (lambda·z = {s['lz']})")

# concentración de masa por anillos
rings = [(0, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 3000)]
print("\n  Distribución posterior por distancia al punto de dispersión:")
ring_rows = []
for a, b in rings:
    mk = (r_zh >= a) & (r_zh < b)
    ring_rows.append(dict(a=a, b=b, pri=prior[mk].sum(), post=post[mk].sum()))
    print(f"    {a:>5}-{b:<5} m   a priori {prior[mk].sum()*100:5.1f}%   "
          f"posterior {post[mk].sum()*100:5.1f}%")
OUT["rings"] = ring_rows
OUT["searches"] = [(s["name"], mb, np.exp(-s["lz"])) for s, mb in zip(searches, mass_before)]

# esfuerzo óptimo (llenado de agua) sobre la posterior
lam = np.full_like(post, 1.0)
Zbudget = 3000.0
lo, hi = 1e-14, (lam * post).max()
for _ in range(80):
    mu = np.sqrt(lo * hi)
    z = np.maximum(0, np.log(lam * post / mu) / lam)
    if z.sum() > Zbudget: lo = mu
    else: hi = mu
z_opt = np.maximum(0, np.log(lam * post / np.sqrt(lo * hi)) / lam)
frac_area = (z_opt > 0).mean()
mass_cov = post[z_opt > 0].sum()
OUT["alloc"] = dict(frac_area=frac_area, mass_cov=mass_cov)
print(f"\n  Asignación óptima de esfuerzo (llenado de agua):")
print(f"    concentra el esfuerzo en el {frac_area*100:.1f}% del área")
print(f"    que contiene el {mass_cov*100:.1f}% de la masa posterior")

fig, ax = plt.subplots(1, 3, figsize=(11.0, 3.4))
ext = [-lim, lim, -lim, lim]
for a, M, ttl in zip(ax, [prior, post, z_opt],
                     ["(a) A priori (escenario peatonal)",
                      "(b) Posterior tras batidas infructuosas",
                      "(c) Asignación óptima de esfuerzo"]):
    im = a.imshow(M, origin="lower", extent=ext, cmap="magma", aspect="equal")
    a.set_title(ttl, fontsize=9)
    a.set_xlabel("este (m)")
    for P, lab, c in [(P_ZH, "ZH", "cyan"), (P_SUD, "Sud", "lime"),
                      (P_FEU, "Can Feu", "white")]:
        a.plot(*P, "o", ms=4, color=c, mec="k", mew=.5)
        a.annotate(lab, P, textcoords="offset points", xytext=(5, 4),
                   color=c, fontsize=7.5)
    a.grid(False)
for s in searches[:2]:
    ax[1].add_patch(Circle(np.asarray(s["P"]), s["R"], fill=False,
                           ec="cyan", lw=1.0, ls="--"))
ax[0].set_ylabel("norte (m)")
plt.tight_layout(); plt.savefig("fig3_busqueda.pdf"); plt.close()

# =====================================================================
# 4. ESCENARIO VEHICULAR — ventana de paso
# =====================================================================
NV = 300_000
T0 = rng.uniform(5.92, 6.42, NV)                 # salida 05:55-06:25
Vveh = np.clip(rng.normal(112, 14, NV), 70, 150)
overhead = rng.exponential(4.0, NV)              # incorporación, peajes
D_JONQ = 146.0
T_arr = T0 + D_JONQ / Vveh + overhead / 60.0
q = np.percentile(T_arr, [5, 25, 50, 75, 95])
def hhmm(t):
    h = int(t); mm = int(round((t - h) * 60))
    if mm == 60: h, mm = h + 1, 0
    return f"{h:02d}:{mm:02d}"
OUT["veh"] = dict(q=q, width=(q[4] - q[0]) * 60)
print("\n" + "=" * 62)
print("4. ESCENARIO VEHICULAR — paso por frontera (152 km por AP-7)")
print("=" * 62)
print(f"    P05 {hhmm(q[0])}   P25 {hhmm(q[1])}   mediana {hhmm(q[2])}   "
      f"P75 {hhmm(q[3])}   P95 {hhmm(q[4])}")
print(f"    anchura de la ventana al 90%: {(q[4]-q[0])*60:.0f} minutos")

fig, ax = plt.subplots(figsize=(6.2, 2.5))
ax.hist(T_arr, bins=160, color="#3d6ea8", alpha=.85, density=True)
ax.axvspan(q[0], q[4], color="orange", alpha=.16)
ax.set_xlabel("hora de paso estimada por la frontera")
ax.set_ylabel("densidad")
ticks = np.arange(7.0, 9.01, 0.5)
ax.set_xticks(ticks); ax.set_xticklabels([hhmm(t) for t in ticks])
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("fig4_vehiculo.pdf"); plt.close()

print("\n" + "=" * 62)
print("Figuras generadas: fig1_tiempo.pdf fig2_celular.pdf "
      "fig3_busqueda.pdf fig4_vehiculo.pdf")
print("=" * 62)

np.save("results.npy", OUT, allow_pickle=True)
