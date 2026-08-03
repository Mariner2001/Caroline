#!/usr/bin/env python3
"""Figura de orientación geográfica. Genera fig0_mapa.pdf"""
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
plt.rcParams.update({"font.size":8.5,"axes.labelsize":8.5,"xtick.labelsize":7.5,
 "ytick.labelsize":7.5,"legend.fontsize":7.5,"figure.dpi":150,"savefig.bbox":"tight"})

LAT0,LON0=41.5336445,2.0998452
ML=111320.; MO=111320.*np.cos(np.radians(LAT0))
def xy(la,lo): return np.array([(lo-LON0)*MO,(la-LAT0)*ML])

P={"ZH":(xy(41.5336445,2.0998452),"Zona de ocio\n(dispersión)"),
   "SUD":(xy(41.5287051,2.1054052),"Est. Sabadell Sud\n(última llamada)"),
   "FEU":(xy(41.5393237,2.0936818),"Castell de\nCan Feu"),
   "CEN":(xy(41.5464246,2.1156055),"Est. Sabadell\nCentre"),
   "NOR":(xy(41.5619458,2.0962433),"Est. Sabadell\nNord")}
SEC=np.array([xy(41.5261315,2.0894665),xy(41.5167637,2.1151786),
              xy(41.5010170,2.1284971),xy(41.4920899,2.1441170)])
RIP=np.array([xy(41.562338,2.109377),xy(41.5564364,2.1169399),xy(41.5436708,2.1257046)])
d=RIP[2]-RIP[1]; RIP=np.vstack([RIP,RIP[2]+d/np.linalg.norm(d)*2200])
RAIL=np.array([P["SUD"][0],P["NOR"][0]])

BAT=[(P["ZH"][0],150.,"r=150 m"),(P["FEU"][0],350.,"r=350 m"),
     ((P["ZH"][0]+P["SUD"][0])/2,400.,"r=400 m")]

def base(ax,lim,detalle=False):
    ax.add_patch(Circle(P["SUD"][0],1246,fill=False,ec="#888",ls=(0,(4,3)),lw=.8,zorder=1))
    ax.add_patch(Circle(P["SUD"][0],1869,fill=False,ec="#888",ls=(0,(4,3)),lw=.8,zorder=1))
    for c,r,_ in BAT:
        ax.add_patch(Circle(c,r,fc="#d94801",alpha=.13,ec="#d94801",lw=.8,ls=":",zorder=2))
    ax.plot(SEC[:,0],SEC[:,1],color="#00897b",lw=2.6,zorder=3,solid_capstyle="round",
            label="Riu Sec")
    ax.plot(RIP[:,0],RIP[:,1],color="#1e6fd9",lw=2.2,zorder=3,solid_capstyle="round",
            label="Riu Ripoll")
    ax.plot(RAIL[:,0],RAIL[:,1],color="#e08214",lw=1.5,ls=(0,(6,3)),zorder=3,
            label="Traza ferroviaria R4")
    for k,(pt,lab) in P.items():
        if detalle and k in("CEN","NOR"): continue
        ax.plot(*pt,"o",ms=6.5,mfc="w",mec="k",mew=1.5,zorder=6)
        ax.plot(*pt,"o",ms=2.5,color="k",zorder=7)
    ax.set_aspect("equal"); ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_xlabel("este (m)"); ax.grid(alpha=.15,lw=.5)

fig,ax=plt.subplots(1,2,figsize=(11.4,5.4))

# ---- (a) contexto
base(ax[0],3100)
for k,(pt,lab) in P.items():
    dx,dy = {"ZH":(-40,150),"SUD":(120,-120),"FEU":(-180,120),
             "CEN":(130,60),"NOR":(120,-60)}[k]
    ha = "right" if k in("ZH","FEU") else "left"
    ax[0].annotate(lab,pt,xytext=(pt[0]+dx,pt[1]+dy),fontsize=7.2,ha=ha,
                   va="center",zorder=8,
                   bbox=dict(fc="w",ec="none",alpha=.75,pad=1.2))
ax[0].set_ylabel("norte (m)")
ax[0].set_title("(a) Contexto — ventana de análisis $6\\times6$ km",fontsize=9.5)
ax[0].legend(loc="lower left",framealpha=.92,fontsize=7.2)
# norte
ax[0].annotate("",xy=(2650,2850),xytext=(2650,2250),
               arrowprops=dict(arrowstyle="-|>",color="k",lw=1.4))
ax[0].text(2650,2930,"N",ha="center",fontsize=9,fontweight="bold")
# escala
ax[0].plot([-2900,-1900],[-2820,-2820],color="k",lw=2.5,solid_capstyle="butt")
ax[0].plot([-2900,-2400],[-2820,-2820],color="w",lw=1.6,solid_capstyle="butt")
ax[0].text(-2400,-2720,"1 km",ha="center",fontsize=7.5)

# ---- (b) detalle
base(ax[1],1450,detalle=True)
for k,(pt,lab) in P.items():
    if k in("CEN","NOR"): continue
    dx,dy={"ZH":(-70,130),"SUD":(90,-140),"FEU":(-90,130)}[k]
    ha="right" if k in("ZH","FEU") else "left"
    ax[1].annotate(lab,pt,xytext=(pt[0]+dx,pt[1]+dy),fontsize=7.2,ha=ha,va="center",
                   zorder=8,bbox=dict(fc="w",ec="none",alpha=.8,pad=1.2))
ax[1].annotate("",xy=P["SUD"][0],xytext=P["ZH"][0],
               arrowprops=dict(arrowstyle="<->",color="#b2182b",lw=1.6,shrinkA=7,shrinkB=7))
ax[1].text(280,-330,"719 m",color="#b2182b",fontsize=8,fontweight="bold",rotation=-50)
ax[1].annotate("839 m",xy=(-380,-1180),fontsize=7.5,color="#00695c",fontweight="bold")
ax[1].text(P["SUD"][0][0]-60,P["SUD"][0][1]+1246+40,"20 min",fontsize=6.8,color="#666",ha="center")
ax[1].set_title("(b) Detalle del corredor crítico",fontsize=9.5)
ax[1].text(-1380,-1380,"Discos naranja: batidas documentadas\n"
           "Discos grises: alcance peatonal a 20 y 30 min\ndesde el ancla de la llamada",
           fontsize=6.8,va="bottom",bbox=dict(fc="w",ec="#bbb",alpha=.9,pad=3))
for a in ax: a.tick_params(length=2.5)
plt.tight_layout(); plt.savefig("fig0_mapa.pdf"); plt.close()
print("fig0_mapa.pdf generada")
