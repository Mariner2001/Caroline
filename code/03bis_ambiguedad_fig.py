import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":9,"axes.labelsize":9,"axes.titlesize":9.5,
 "xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":7.5,"figure.dpi":150,
 "savefig.bbox":"tight","axes.grid":True,"grid.alpha":.25,"axes.axisbelow":True})
c=299_792_458.0; eta=44.9-6.55*np.log10(25.0); ta=c*(48/13*1e-6)/2
r=np.linspace(150,2500,600)

fig,ax=plt.subplots(1,2,figsize=(9.6,3.3))
# (a) anillo por potencia
for d,lab,col in [(4,"$\\pm4$ dB (instrumental)","#3d6ea8"),
                  (8,"$\\pm8$ dB ($1\\sigma$)","#2f8f5b"),
                  (13,"$\\pm13$ dB (IC$_{90}$)","#c2521a")]:
    f=np.sqrt(10**(2*d/eta))
    ax[0].fill_between(r,r/f,r*f,alpha=.20,color=col)
    ax[0].plot(r,r*f,color=col,lw=1.3,label=lab); ax[0].plot(r,r/f,color=col,lw=1.3)
ax[0].plot(r,r,"k--",lw=.9,label="distancia nominal")
ax[0].set_xlabel("distancia nominal (m)"); ax[0].set_ylabel("distancia compatible (m)")
ax[0].set_title("(a) Ambigüedad por medida de potencia")
ax[0].legend(loc="upper left"); ax[0].set_ylim(0,4000)

# (b) anchura: potencia vs TA
for d,lab,col in [(8,"potencia, $1\\sigma$","#2f8f5b"),(13,"potencia, IC$_{90}$","#c2521a")]:
    f=np.sqrt(10**(2*d/eta)); ax[1].plot(r,r*f-r/f,color=col,lw=1.6,label=lab)
ax[1].axhline(ta,color="#8c3b8c",lw=1.8,ls="-",label="TA GSM (cuanto 553 m)")
ax[1].axhline(78.1,color="#555",lw=1.4,ls=":",label="TA LTE (78 m, no aplicable 2015)")
ax[1].axvspan(300,800,color="gray",alpha=.13)
ax[1].text(550,3400,"radio urbano\ntípico 2015",ha="center",fontsize=7,color="#444")
ax[1].set_xlabel("distancia nominal (m)"); ax[1].set_ylabel("anchura de la banda (m)")
ax[1].set_title("(b) Anchura resultante"); ax[1].legend(loc="upper left"); ax[1].set_ylim(0,4200)
for a in ax: a.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("fig3_ambiguedad.pdf"); plt.close()
print("fig3_ambiguedad.pdf generada")
