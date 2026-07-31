#!/usr/bin/env python3
"""
02_geospatial.py — Análisis geoespacial.

Genera: dispersión inicial, métrica geodésica con barreras, a priori en dos
fases condicionado al anclaje de la llamada, búsqueda bayesiana con
detectabilidad diferenciada, y matriz de tiempos mínimos de tránsito.

Hidrografía: Riu Sec (curso relevante, SO) y Ripoll (E). Ambos modelados.

Figuras: fig5_barreras.pdf, fig6_posterior.pdf, fig7_riusec.pdf
Semilla fija: 20150315.  Tiempo de ejecución: ~10 min.
"""
import numpy as np, heapq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(20150315)
plt.rcParams.update({"font.size":9,"axes.labelsize":9,"axes.titlesize":9.5,
    "xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":8,"figure.dpi":150,
    "savefig.bbox":"tight","axes.grid":True,"grid.alpha":.25,"axes.axisbelow":True})

# ---------------------------------------------------------------- geometría
LAT0, LON0 = 41.5336445, 2.0998452
MLAT, MLON = 111_320.0, 111_320.0*np.cos(np.radians(LAT0))
def xy(la, lo): return np.array([(lo-LON0)*MLON, (la-LAT0)*MLAT])

P_ZH  = xy(41.5336445, 2.0998452)   # zona de ocio / punto de dispersión
P_SUD = xy(41.5287051, 2.1054052)   # est. Sabadell Sud — ancla de la llamada
P_FEU = xy(41.5393237, 2.0936818)   # Castell de Can Feu
P_NOR = xy(41.5619458, 2.0962433)   # est. Sabadell Nord
P_CEN = xy(41.5464246, 2.1156055)   # est. Sabadell Centre

# Riu Sec: NO -> SE, atraviesa transversalmente el Vallès
SEC = np.array([xy(41.5261315, 2.0894665),   # Sant Quirze del Vallès
                xy(41.5167637, 2.1151786),   # Barberà del Vallès
                xy(41.5010170, 2.1284971),   # Cerdanyola
                xy(41.4920899, 2.1441170)])  # Cerdanyola (Acàcies)
# Ripoll: margen oriental
RIP = np.array([xy(41.5623380, 2.1093770),
                xy(41.5564364, 2.1169399),
                xy(41.5436708, 2.1257046)])
_d = RIP[2]-RIP[1]; RIP = np.vstack([RIP, RIP[2]+_d/np.linalg.norm(_d)*2200])
RAIL = np.array([P_SUD, P_NOR])              # traza ferroviaria R4

GR, LIM = 50.0, 3000.0
g = np.arange(-LIM, LIM+GR, GR); GX, GY = np.meshgrid(g, g)

def dpoly(GX, GY, poly):
    best = np.full(np.shape(GX), np.inf)
    for k in range(len(poly)-1):
        a, b = poly[k], poly[k+1]; ab = b-a; L2 = ab@ab
        t = np.clip(((GX-a[0])*ab[0]+(GY-a[1])*ab[1])/L2, 0, 1)
        best = np.minimum(best, np.hypot(GX-(a[0]+t*ab[0]), GY-(a[1]+t*ab[1])))
    return best

d_sec, d_rip, d_rail = dpoly(GX,GY,SEC), dpoly(GX,GY,RIP), dpoly(GX,GY,RAIL)

def dpoint(P, poly):
    return dpoly(np.array([[P[0]]]), np.array([[P[1]]]), poly)[0,0]

# ---------------------------------------------------------------- §1 dispersión
print("="*70); print("1. DISPERSIÓN INICIAL"); print("="*70)
R = lambda t, v0, vw=1.35, ga=1/45: vw*t + (v0-vw)/ga*(1-np.exp(-ga*t))
for t in (30,60,120,180):
    print(f"   t={t:4d} s   R={R(t,4.5):6.0f} m")
R120 = R(120, 4.5)
print(f"   radio de dispersión adoptado (120 s, v0=4.5 m/s): {R120:.0f} m")
print(f"   modelo v(t)=v0·exp(-γt): asíntota {5.5*45:.0f} m -> refutado (§Apéndice A)")

# ---------------------------------------------------------------- §2 hidrografía
print("\n"+"="*70); print("2. HIDROGRAFÍA Y BARRERAS"); print("="*70)
print(f"   {'':32}{'Riu Sec':>12}{'Ripoll':>12}")
for nm, P in [("Zona de ocio (dispersión)",P_ZH),
              ("Sabadell Sud (llamada)",P_SUD),
              ("Castell de Can Feu",P_FEU)]:
    ds, dr = dpoint(P,SEC), dpoint(P,RIP)
    print(f"   {nm:<32}{ds:>10.0f} m{dr:>10.0f} m")
print(f"\n   Tiempo de marcha (1.35 m/s, rodeo 1.3):")
for nm, P in [("Zona de ocio",P_ZH),("Sabadell Sud",P_SUD),("Can Feu",P_FEU)]:
    ds, dr = dpoint(P,SEC), dpoint(P,RIP)
    print(f"   {nm:<32}{ds*1.3/1.35/60:>9.1f} min{dr*1.3/1.35/60:>9.1f} min")
print(f"\n   Traza ferroviaria R4 a {dpoint(P_ZH,RAIL):.0f} m de la zona de ocio")

# longitud de cauce accesible a pie desde el ancla
def cauce_en_radio(poly, P, R_):
    tt=[]
    for k in range(len(poly)-1):
        for s in np.linspace(0,1,600): tt.append(poly[k]+s*(poly[k+1]-poly[k]))
    tt=np.array(tt); L=sum(np.linalg.norm(poly[k+1]-poly[k]) for k in range(len(poly)-1))
    return (np.linalg.norm(tt-P,axis=1)<=R_).mean()*L
print(f"\n   Longitud de cauce accesible desde el ancla de la llamada:")
print(f"   {'radio':<28}{'Riu Sec':>12}{'Ripoll':>12}")
for Rr,lab in [(1246,"1246 m (20 min)"),(1869,"1869 m (30 min)"),
               (2661,"2661 m (42.7 min)")]:
    print(f"   {lab:<28}{cauce_en_radio(SEC,P_SUD,Rr):>10.0f} m"
          f"{cauce_en_radio(RIP,P_SUD,Rr):>10.0f} m")

# ---------------------------------------------------------------- §3 métrica
cost = (1.0 + 5.0*np.exp(-(d_sec/55.)**2) + 7.0*np.exp(-(d_rip/60.)**2)
            + 4.0*np.exp(-(d_rail/45.)**2)
            + 1.0*np.exp(-(d_sec/200.)**2) + 1.2*np.exp(-(d_rip/220.)**2))

def geo(cost, P):
    D = np.full(cost.shape, np.inf)
    j0,i0 = np.unravel_index(np.argmin(np.hypot(GX-P[0],GY-P[1])), GX.shape)
    D[j0,i0]=0.; pq=[(0.,j0,i0)]
    nb=[(-1,0,1),(1,0,1),(0,-1,1),(0,1,1),(-1,-1,1.4142),(-1,1,1.4142),
        (1,-1,1.4142),(1,1,1.4142)]
    while pq:
        dd,j,i = heapq.heappop(pq)
        if dd>D[j,i]: continue
        for dj,di,w in nb:
            k,l = j+dj, i+di
            if 0<=k<D.shape[0] and 0<=l<D.shape[1]:
                nd = dd + w*GR*.5*(cost[j,i]+cost[k,l])
                if nd<D[k,l]: D[k,l]=nd; heapq.heappush(pq,(nd,k,l))
    return D

D_ZH, D_SUD = geo(cost,P_ZH), geo(cost,P_SUD)
E_ZH = np.hypot(GX-P_ZH[0], GY-P_ZH[1])
rat = D_ZH/np.maximum(E_ZH,1.); mk_ = E_ZH>300
print(f"\n   Rodeo geodésico/euclídeo: mediana {np.median(rat[mk_]):.2f}  "
      f"p95 {np.percentile(rat[mk_],95):.2f}  máx {rat[mk_].max():.2f}")
print(f"   celdas con rodeo > 1.5x: {100*(rat[mk_]>1.5).mean():.1f}%  "
      f"-> corrección de BARRERA modesta")

# ---------------------------------------------------------------- §4 a priori
DT_S = 54.5*60; VMAX = 1.35; BUDGET = VMAX*DT_S
d0 = D_SUD[np.unravel_index(np.argmin(np.hypot(GX-P_ZH[0],GY-P_ZH[1])),GX.shape)]
exc = (D_ZH+D_SUD) - d0
prism = np.where(D_ZH+D_SUD <= BUDGET, np.exp(-np.maximum(exc,0)/700.), 0.)
phaseB = stats.gamma.pdf(np.maximum(D_SUD,1.), a=2., scale=1.15*42.7*60/3.)
def mezcla(wA):
    p = wA*prism/prism.sum() + (1-wA)*phaseB/phaseB.sum(); return p/p.sum()
prior = mezcla(0.50)

lam = np.clip(2.2 - 1.9*np.exp(-(d_rip/180.)**2) - 1.7*np.exp(-(d_sec/160.)**2)
                  - 0.6*np.exp(-(d_rail/70.)**2), .25, 2.5)
lam_solo_rip = np.clip(2.2 - 1.9*np.exp(-(d_rip/180.)**2)
                           - 0.6*np.exp(-(d_rail/70.)**2), .25, 2.5)

searches = [("Entorno zona de ocio (r=150 m)", P_ZH, 150., 1.2),
            ("Castell de Can Feu (r=350 m)",  P_FEU, 350., 1.0),
            ("Corredor a la estación (r=400 m)", (P_ZH+P_SUD)/2, 400., 0.8)]
def run(prior, lam):
    post = prior.copy(); rows=[]
    for n,P,Rr,z in searches:
        m = np.hypot(GX-P[0],GY-P[1]) <= Rr
        rows.append((n, post[m].sum(), np.exp(-(lam*z)[m]).mean()))
        post = post*np.where(m, np.exp(-lam*z), 1.); post/=post.sum()
    return post, rows
post, rows = run(prior, lam)
post_old, _ = run(prior, lam_solo_rip)

print("\n"+"="*70); print("3. BÚSQUEDA BAYESIANA"); print("="*70)
for n,mb,ret in rows:
    print(f"   {n:<34} masa {mb*100:5.2f}%   retiene {ret*100:5.1f}%")

bs, br = d_sec<250, d_rip<250; bu = ~(bs|br)
print(f"\n   {'corredor':<26}{'a priori':>11}{'posterior':>11}{'λ':>7}{'retiene':>10}")
for nm,m in [("Riu Sec (<250 m)",bs),("Ripoll (<250 m)",br),("Trama urbana",bu)]:
    l = lam[m].mean()
    print(f"   {nm:<26}{prior[m].sum()*100:>10.2f}%{post[m].sum()*100:>10.2f}%"
          f"{l:>7.2f}{np.exp(-l)*100:>9.1f}%")
print(f"\n   Razón de masa residual Riu Sec / urbano : "
      f"{np.exp(-lam[bs].mean())/np.exp(-lam[bu].mean()):.1f}x")
print(f"   Masa posterior Riu Sec / Ripoll        : {post[bs].sum()/post[br].sum():.1f}x")
print(f"\n   Masa dentro del alcance peatonal desde el ancla:")
for Rr,lab in [(1246,"20 min"),(1869,"30 min"),(2661,"42.7 min")]:
    m = np.hypot(GX-P_SUD[0],GY-P_SUD[1])<=Rr
    print(f"     {lab:9s}: Riu Sec {post[m&bs].sum()*100:5.2f}%   "
          f"Ripoll {post[m&br].sum()*100:5.2f}%")
print(f"\n   {'anillo (m)':>14}{'a priori':>11}{'posterior':>12}")
for a,b in [(0,250),(250,500),(500,1000),(1000,2000),(2000,3000)]:
    m=(E_ZH>=a)&(E_ZH<b)
    print(f"   {a:>6}-{b:<7}{prior[m].sum()*100:>9.1f}%{post[m].sum()*100:>11.1f}%")
print(f"\n   Sensibilidad al peso de la fase A:")
for wA in (0.35,0.50,0.65):
    p=mezcla(wA); m=E_ZH<1000
    print(f"     w_A={wA:.2f} -> masa dentro de 1 km: {p[m].sum()*100:5.1f}%")

# ---------------------------------------------------------------- §5 tránsito
print("\n"+"="*70); print("4. TIEMPOS MÍNIMOS DE TRÁNSITO (min, a pie, 1.35 m/s)")
print("="*70)
pts={"Zona de ocio":P_ZH,"Can Feu":P_FEU,"Sabadell Sud":P_SUD,"Sabadell Centre":P_CEN}
nm_=list(pts); T=np.zeros((4,4))
for i,a in enumerate(nm_):
    Di=geo(cost,pts[a])
    for j,b in enumerate(nm_):
        jj=np.argmin(np.hypot(GX-pts[b][0],GY-pts[b][1]))
        T[i,j]=Di.ravel()[jj]/1.35/60
T=(T+T.T)/2; np.fill_diagonal(T,0)
print("   "+" "*17+"".join(f"{n[:13]:>16}" for n in nm_))
for i,a in enumerate(nm_):
    print(f"   {a:<17}"+"".join(f"{T[i,j]:>16.1f}" if i!=j else f"{'—':>16}"
                                for j in range(4)))
tfs=T[nm_.index("Can Feu"), nm_.index("Sabadell Sud")]
print(f"\n   Criterio: m_ij = |t_i - t_j| / τ_ij ;  m_ij < 1  => IMPOSIBLE")
print(f"   Cadena Can Feu -> estación -> Sants:")
print(f"     tramo a pie          : {tfs:.1f} min")
print(f"     margen declarado     : 30.0 min")
print(f"     máximo ferroviario   : {30-tfs:.1f} min  <- contrastable con horario R4")

# ---------------------------------------------------------------- figuras
ext=[-LIM,LIM,-LIM,LIM]
def mk(a, leg=False):
    for P,l,c in [(P_ZH,"ZH","cyan"),(P_SUD,"Sud","lime"),(P_FEU,"Can Feu","w")]:
        a.plot(*P,"o",ms=4,color=c,mec="k",mew=.5)
        a.annotate(l,P,textcoords="offset points",xytext=(5,4),color=c,fontsize=7)
    a.plot(SEC[:,0],SEC[:,1],color="#00e5c0",lw=2.2,label="Riu Sec")
    a.plot(RIP[:,0],RIP[:,1],color="#4da6ff",lw=2.0,label="Ripoll")
    a.plot(RAIL[:,0],RAIL[:,1],color="#ff9a3c",lw=1.5,ls="--",label="ferrocarril")
    a.set_xlim(-LIM,LIM); a.set_ylim(-LIM,LIM); a.grid(False); a.set_xlabel("este (m)")
    if leg: a.legend(loc="upper right",fontsize=6.5,framealpha=.85)

f,ax=plt.subplots(1,3,figsize=(11.2,3.5))
ax[0].imshow(cost,origin="lower",extent=ext,cmap="bone_r"); mk(ax[0],True)
ax[0].set_title("(a) Coste de tránsito"); ax[0].set_ylabel("norte (m)")
im=ax[1].imshow(np.where(E_ZH>300,rat,1),origin="lower",extent=ext,
                cmap="YlOrRd",vmin=1,vmax=1.6); mk(ax[1])
ax[1].set_title("(b) Rodeo geodésico/euclídeo"); plt.colorbar(im,ax=ax[1],fraction=.046)
im=ax[2].imshow(lam,origin="lower",extent=ext,cmap="viridis"); mk(ax[2])
ax[2].set_title("(c) Detectabilidad $\\lambda$"); plt.colorbar(im,ax=ax[2],fraction=.046)
plt.tight_layout(); plt.savefig("fig5_barreras.pdf"); plt.close()

f,ax=plt.subplots(1,3,figsize=(11.2,3.5))
ax[0].imshow(prism/prism.max(),origin="lower",extent=ext,cmap="magma"); mk(ax[0])
ax[0].set_title("(a) Fase A: prisma ZH$\\leftrightarrow$estación")
ax[0].set_ylabel("norte (m)")
ax[1].imshow(prior,origin="lower",extent=ext,cmap="magma"); mk(ax[1])
ax[1].set_title("(b) A priori combinado ($w_A=0{,}5$)")
ax[2].imshow(post,origin="lower",extent=ext,cmap="magma"); mk(ax[2])
ax[2].set_title("(c) Posterior tras batidas")
plt.tight_layout(); plt.savefig("fig6_posterior.pdf"); plt.close()

f,ax=plt.subplots(1,3,figsize=(11.2,3.5))
ax[0].imshow(lam,origin="lower",extent=ext,cmap="viridis"); mk(ax[0],True)
ax[0].set_title("(a) Detectabilidad con ambos cauces"); ax[0].set_ylabel("norte (m)")
ax[1].imshow(post,origin="lower",extent=ext,cmap="magma"); mk(ax[1])
ax[1].set_title("(b) Posterior resultante")
D=post-post_old; v=np.abs(D).max()
im=ax[2].imshow(D,origin="lower",extent=ext,cmap="RdBu_r",vmin=-v,vmax=v); mk(ax[2])
ax[2].set_title("(c) Cambio al incorporar el Riu Sec")
plt.colorbar(im,ax=ax[2],fraction=.046)
plt.tight_layout(); plt.savefig("fig7_riusec.pdf"); plt.close()

print("\nFiguras: fig5_barreras.pdf  fig6_posterior.pdf  fig7_riusec.pdf")
