"""Test Alpha/Beta: discriminacion entre 'terminal se movio' y 'terminal quieto'
   a partir del patron de conmutacion. Desarrollo formal de la idea del borrador."""
import numpy as np
rng = np.random.default_rng(20150315)

print("="*70)
print("TEST ALPHA/BETA: razon de verosimilitud sobre el patron de celdas")
print("="*70)
print("""
  H_alpha: el terminal se desplazo (vehiculo)  -> secuencia de celdas
           MONOTONA a lo largo de un eje, sin retornos
  H_beta : el terminal permanecio en zona de solapamiento -> secuencia
           OSCILANTE con retornos (ping-pong)

  Estadistico discriminante: numero de RETORNOS R en la secuencia
  (visitas a una celda ya visitada tras haber estado en otra)
""")

def simulate_beta(n_events, n_cells=3):
    """Terminal quieto en solapamiento: reseleccion casi aleatoria."""
    return rng.integers(0, n_cells, n_events)

def simulate_alpha(n_events, n_cells=8):
    """Terminal en vehiculo: avance monotono, ocasional repeticion contigua."""
    seq=[0]; cur=0
    for _ in range(n_events-1):
        if rng.random()<0.75: cur=min(cur+1,n_cells-1)
        seq.append(cur)
    return np.array(seq)

def retornos(seq):
    """Cuenta visitas a una celda ya abandonada."""
    r=0; vistas=set()
    for k,c in enumerate(seq):
        if k>0 and c!=seq[k-1]:
            if c in vistas: r+=1
            vistas.add(seq[k-1])
    return r

for n in (5,8,12):
    Rb=np.array([retornos(simulate_beta(n)) for _ in range(20000)])
    Ra=np.array([retornos(simulate_alpha(n)) for _ in range(20000)])
    print(f"  n={n:2d} registros:  H_beta retornos={Rb.mean():.2f}+/-{Rb.std():.2f}"
          f"   H_alpha retornos={Ra.mean():.2f}+/-{Ra.std():.2f}")
    # razon de verosimilitud para R=0 y R>=2
    for thr,lab in [(0,'R=0'),(2,'R>=2')]:
        pa = (Ra==0).mean() if thr==0 else (Ra>=2).mean()
        pb = (Rb==0).mean() if thr==0 else (Rb>=2).mean()
        lr = pa/max(pb,1e-6)
        print(f"        {lab:5s}: P|alpha={pa:.3f}  P|beta={pb:.3f}  "
              f"LR(alpha:beta) = {lr:7.2f}")

print("""
  LECTURA:
  - Una sola conmutacion NO discrimina nada (n=2 -> R=0 siempre).
  - Con >=8 registros el estadistico separa bien: ausencia total de
    retornos favorece H_alpha por un factor de ~30x; dos o mas retornos
    favorecen H_beta de forma casi determinante.
  - Es un test que se aplica al DATO QUE YA EXISTE en el expediente,
    sin necesidad de conocer las areas de servicio reales.
""")
