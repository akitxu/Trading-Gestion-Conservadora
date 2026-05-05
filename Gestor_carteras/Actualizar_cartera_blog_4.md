Gestor de Carteras
Estructura del sistema
📦 Sistema de Análisis de Cartera  
├── 📄 01_GestorRutas.py  
├── 📄 02_GestorCartera.py  
├── 📄 03_DescargadorYahoo.py  
├── 📄 04_AnalizadorMetricas.py  
├── 📄 05_AnalizadorTecnico.py  
├── 📄 06_AnalizadorCartera.py  
├── 📄 07_Exportador.py  
├── 📄 main.py (Orquestador)  
└── 📓 Consulta_github_actualizar_cartera.ipynb (Notebook Jupyter)  

```
# Flujo de ejecución
┌─────────────────────────────────┐
│  Iniciar MainAnalisisCartera    │
└────────────┬────────────────────┘
             │
      ┌──────▼──────┐
      │ Menú Principal
      └──────┬──────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
Gestionar         Descargar
Cartera           Datos
    │                 │
    ▼                 ▼
 Análisis          Análisis
Fundamental       Técnico
    │                 │
    └────────┬────────┘
             │
             ▼
      Análisis de
       Cartera
             │
             ▼
         Exportar
        Resultados

```
```
╔══════════════════════════════════════════════════════════════════════════════╗
║          GESTOR DE CARTERA DE VALORES — actualizar_cartera.py               ║
║          Versión 2.0  ·  Python 3.10+  ·  Jupyter / Google Colab / CLI      ║
╚══════════════════════════════════════════════════════════════════════════════╝

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
1. QUÉ HACE    
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

  Gestor completo de carteras de inversión para el inversor particular.
  Combina tres capas de análisis:

  a) GESTIÓN DE CARTERA
  
 - Crea y almacena carteras en Excel con estructura estándar.    
 - Descarga cotizaciones históricas de Yahoo Finance (fondos, ETFs,  
   acciones e índices) directamente en Datos_CSV/.    
 - Actualiza automáticamente Valor_actual, Peso%, Benef. y Plusv.%  
   usando el precio más reciente del CSV de cada valor.    
 - Soporta múltiples aportaciones por valor (suscripciones parciales,  
   traspasos, compras adicionales).    
 - Compatible con fondos de inversión (NAV diario), ETFs, acciones  
   españolas/europeas/USA y planes de pensiones (CSV manual).    

  b) ANÁLISIS CUANTITATIVO
  
 - Métricas básicas: CAGR, volatilidad diaria y mensual, Sharpe,  
   Max Drawdown, RSI(14), Beta, Alpha, R².    
 - Métricas avanzadas de distribución: Sortino, Omega, Skewness  
   (inclinación), Kurtosis (curtosis) y Tail Ratio (relación de cola).    
 - Metodología Morningstar: Sharpe y Sortino calculados con retornos
   mensuales y Euribor 3M del periodo como tasa libre de riesgo.    
 - Benchmark automático por categoría (BENCHMARK_CATEGORIAS): renta
   fija → iShares Euro Govt Bond 1-3yr; acciones .MC → Ibex 35, etc.    
 - Correlación estática y rodante entre fondos; detección automática
   de convergencias (señal de crisis) y pares con alta correlación.    
 - Frontera eficiente Markowitz (Monte Carlo 8.000 simulaciones +
   optimización scipy): carteras de Sharpe máximo y mínima varianza.  
 - VaR histórico, paramétrico y CVaR (Expected Shortfall) en % y €.  
 - Contribución marginal al riesgo por fondo.  

  c) VISUALIZACIÓN Y EXPORTACIÓN
  
 - Gráfica base 100 con benchmark superpuesto (zonas verde/rojo).    
 - Gráfica técnica: SMA 20/50/200 + Bollinger + MACD + ATR + RSI.    
 - Gráfico subacuático: NAV + drawdown continuo + histograma de
   retornos mensuales con curva normal teórica + tiempo bajo el agua
   por año.   
 - Heatmap mensual (año × mes) y comparativo anual (fondo × año).  
 - Correlación rodante con bandas de referencia.    
 - Exportación PDF (portada + diagnóstico + gráficas) y Excel.    

  Por qué combina mercado y análisis estadístico avanzado: 
     Los indicadores técnicos (SMA, MACD) detectan señales de corto plazo;
     las métricas de distribución (Skewness, Tail Ratio) revelan si el
     perfil de riesgo real coincide con el declarado; la frontera eficiente
     guía la asignación estratégica. La combinación permite una visión
     completa: ¿está batiendo al benchmark? ¿es el riesgo simétrico?
     ¿está bien diversificada la cartera?


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
2. CÓMO SE USA  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    

  ── USO RÁPIDO ──────────────────────────────────────────────────────────────

    # Desde terminal:
    python actualizar_cartera.py  

    # Especificando el Excel directamente:  
    python actualizar_cartera.py Carteras/mi_cartera_2026.xlsx  

    # Desde Jupyter Notebook / Google Colab:  
    %run actualizar_cartera.py  
    %run actualizar_cartera.py Carteras/mi_cartera_2026.xlsx  

    # En Google Colab — variable de entorno para parametrizar sin tocar código:  
    import os  
    os.environ["CARTERA_EXCEL"] = "/content/drive/MyDrive/Gestor_Cartera/Carteras/mi.xlsx"  
    %run actualizar_cartera.py  

  ── FLUJO DE PRIMERA EJECUCIÓN ───────────────────────────────────────────────    

    1. El programa detecta el entorno (local / Colab) automáticamente.  
    2. Busca Excels en Carteras/. Si no hay ninguno, lanza el asistente
       de creación interactivo: nombre → selección de valores del catálogo
       → datos de cada aportación → guarda en Carteras/.  
    3. Descarga las cotizaciones de los valores de la cartera → Datos_CSV/.  
    4. Actualiza el Excel y muestra el menú principal.  

  ── FLUJO SEMANAL HABITUAL ───────────────────────────────────────────────────    

    1. Ejecutar el script → seleccionar cartera → responder S a
       "¿Actualizar cotizaciones?" → el Excel queda al día.  
    2. Opción 4 → métricas y diagnóstico.  
    3. Opción 6 → exportar informe PDF.  

  ── MENÚ PRINCIPAL ───────────────────────────────────────────────────────────    

    1  Descargar cotizaciones desde internet  (catálogo FONDOS_DATA → Descargas_yahoo/)    
    2  Actualizar cartera desde CSVs en disco (Datos_CSV/ → Excel)    
    3  Informe completo de un valor           (ficha + métricas + técnico + PDF)    
    4  Métricas y diagnóstico                 (todas las métricas por fondo)    
    5  Correlaciones y medias móviles         (matriz + rodante + MM)    
    6  Exportar informe PDF + Excel           (informe completo de la cartera)    
    7  Análisis técnico avanzado              (SMA/Bollinger/MACD/ATR + PDF)    
    8  Análisis de cartera agregado           (Markowitz + VaR + RC)    
    9  Contextualización                      (benchmark + heatmaps)    
    A  Crear nueva cartera                    (asistente interactivo)    
    B  Cambiar cartera activa                 (seleccionar de Carteras/)    
    0  Salir

  ── ESTRUCTURA DE CARPETAS ───────────────────────────────────────────────────   

    Mi_Cartera/
    ├── actualizar_cartera.py  
    ├── Carteras/              ← Excels de carteras (*.xlsx)    
    ├── Datos_CSV/             ← CSVs curados para análisis (fuente de verdad)    
    ├── Descargas_yahoo/       ← Descargas automáticas del catálogo completo    
    ├── exports/               ← Informes PDF y Excel exportados    
    ├── logs/                  ← Archivo de registro de actualizaciones    
    └── Alertas/               ← Reservado para alertas automáticas (futuro)    

  ── ACTIVOS SOPORTADOS ───────────────────────────────────────────────────────  

    · Fondos de inversión europeos  : ticker 0PXXXXXXXXX.F (Morningstar/Yahoo)    
    · ETFs                          : ticker EXSA.DE, URTH, IBGS, etc.    
    · Índices                       : ^IBEX, ^GSPC, ^STOXX50E, ^GDAXI, etc.    
    · Acciones españolas            : IBE.MC, REP.MC, TEF.MC, etc.    
    · Acciones europeas             : ENI.MI, ORA.PA, NDA-SE.ST, etc.    
    · Acciones USA                  : AAPL, MSFT, GOOGL, etc.    
    · Planes de pensiones           : CSV manual con columnas Date y Close    

  ── PERSONALIZAR EL CATÁLOGO ─────────────────────────────────────────────────    

    Edita el diccionario FONDOS_DATA al inicio del script:  

      FONDOS_DATA = {
          "Mi categoría": {
              "Nombre del fondo": {"ISIN": "IE00XXXXXXXX", "ticker": "0PXXXXXXXX.F"},
          },
      }

    Y el diccionario BENCHMARK_CATEGORIAS para asignar benchmarks:  

      BENCHMARK_CATEGORIAS = {
          "IE00XXXXXXXX": "IE00B4WXJJ64",  # → iShares Euro Govt Bond 1-3yr
          ".MC"         : "ESI143420005",  # acciones españolas → Ibex 35
      }


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   
3. CÓMO INTERPRETAR LOS RESULTADOS  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   

  ── TABLA DE MÉTRICAS BÁSICAS (opción 4) ─────────────────────────────────────    

| Columna      | Descripción                               | Orientativo                         | Alarma                     |
|--------------|--------------------------------------------|--------------------------------------|-----------------------------|
| **NAV**      | Precio actual participación                | —                                    | —                           |
| **Rend%**    | Rentabilidad del periodo                   | > Rf del periodo                     | < 0%                        |
| **CAGR%/a**  | Rentabilidad anual compuesta               | > 2% RF · > 8% RV                    | < 0%                        |
| **Vol%**     | Volatilidad anual (mensual × √12)          | < 2% RF · < 20% RV                   | > 25%                       |
| **Sharpe**   | (CAGR – Rf) / Vol mensual                  | > 1 bueno                            | < 0                         |
| **Sortino**  | (CAGR – Rf) / Vol bajista                  | > 1.0 bueno                          | < 0                         |
| **MaxDD%**   | Caída máxima desde máximo                  | > –5% RF                             | < –15%                      |
| **RSI(14)**  | Fuerza relativa                            | 30–70 neutral                        | > 80 / < 20                 |
| **Años**     | Antigüedad del CSV en el rango             | > 3 para fiabilidad                  | < 1                         |
| **Alpha%/a** | Exceso de rentabilidad vs benchmark        | > 0% genera valor                    | < –1%                       |
| **Beta**     | Sensibilidad al benchmark                  | < 0.5 RF · ~1 RV                     | > 1.5                       |
| **R²**       | Explicación del benchmark                  | > 60% representativo                 | < 20%                       |
| **Omega**    | Relación ganancias/pérdidas                | > 1.5 bueno                          | < 1.0                       |
| **Skewness** | Asimetría (derecha = positivo)             | > 0 mejor                            | < –0.5                      |
| **Kurtosis** | Colas extremas vs normal                   | ~0 mejor                             | > 2                         |
| **Tail Ratio** | P95 / |P5| de retornos                   | > 1.2 mejor                          | < 0.8                       |
| **Años BW**  | % años con drawdown > 50%                  | < 20% mejor                          | > 40%                       |

```
  ── INTERPRETACIÓN DE MÉTRICAS AVANZADAS ─────────────────────────────────────    

    SHARPE RATIO (Ratio de Sharpe):    
      Fórmula: (Rentabilidad - Rf) / Volatilidad    
      ├─ >1.0  ✓ Excelente rendimiento ajustado al riesgo  
      ├─ 0.5-1.0  ○ Bueno, pero hay margen de mejora  
      ├─ 0-0.5  △ Moderado, el riesgo no está justificado  
      └─ <0  ✗ Rentabilidad menor que Rf (evitar)  
      
      Uso: Comparar fondos del mismo tipo (RF con RF, RV con RV).  
           No comparar RF vs RV directamente (la pendiente es diferente).  

    SORTINO RATIO (Ratio de Sortino):  
      Fórmula: (Rentabilidad - Rf) / Volatilidad_bajista  
      └─ Ignora volatilidad positiva (subidas), solo penaliza bajadas.  
      └─ >1.0  ✓ Muy recomendable, especialmente para fondos conservadores  
      └─ Más relevante que Sharpe para RF y fondos defensivos  
      └─ CVaR es la evolución moderna de este concepto  

    OMEGA RATIO (Ratio Omega):  
      Fórmula: Σ(ganancias - umbral) / Σ(umbral - pérdidas)  
      └─ >1.5  ✓ Excelente (ganancias superan pérdidas en proporción 1.5:1)  
      └─ 1.0-1.5  ○ Bueno  
      └─ <1.0  ✗ Más pérdidas que ganancias (evitar)  
      └─ Más intuitivo que Sharpe para inversores con aversión al riesgo  

    SKEWNESS (Asimetría):  
      └─ >0  ✓ Distribución sesgada a la derecha (colas de ganancias)  
      └─ ~0  ○ Distribución simétrica (ideal en teoría)  
      └─ <-0.5  ✗ Sesgada a la izquierda (colas de pérdidas, evitar)  
      └─ En crisis: aumenta hacia -1 (distribución muy asimétrica hacia pérdidas)  

    KURTOSIS (Curtosis):  
      └─ ~0  ✓ Distribución similar a la normal (sin sorpresas extremas)  
      └─ >2  ⚠ Colas gruesas (más sorpresas negativas de lo esperado)  
      └─ <-1  ✓ Colas ligeras (menos sorpresas, pero también pocas ganancias)  
      └─ En fondos monetarios: kurtosis alto indica cambios bruscos de calidad  

    TAIL RATIO (Relación de colas):  
      Fórmula: P95 (mejor mes) / |P5| (peor mes)  
      └─ >1.2  ✓ Mejor, colas de ganancias más gruesas que pérdidas  
      └─ ~1.0  ○ Simétrico  
      └─ <0.8  ✗ Peor, colas de pérdidas más gruesas (asymmetric risk)  
      └─ Durante crisis: converge hacia 0.5 en RV  

    VaR (Value at Risk):
      └─ VaR 95% mensual = -3%  →  en 1 de cada 20 meses, pérdida ≥ 3%
      └─ Para RF: <-2% mensual es alto
      └─ Para RV: <-5% mensual es bajo, >-8% es alto
      └─ CVaR (Expected Shortfall): media de las pérdidas en el peor 5%
      └─ CVaR siempre > VaR en valor absoluto (más conservador)

    BETA (Sensibilidad al benchmark):
      └─ <0.5  ✓ Muy defensivo (mitiga bajadas del mercado)
      └─ 0.5-1.0  ○ Moderadamente defensivo
      └─ ~1.0  ○ Refleja el mercado
      └─ 1.0-1.5  △ Amplificador (sube/baja más que el mercado)
      └─ >1.5  ✗ Alto apalancamiento o estrategia especulativa

    ALPHA (Exceso de rentabilidad):
      └─ >0%  ✓ El gestor genera valor extra respecto al benchmark
      └─ ~0%  ○ Gestor sigue el benchmark (seguidor o muy eficiente)
      └─ <-0%  ✗ El gestor destruye valor (incluso con gestión pasiva hubiera ido mejor)
      └─ En fondos pasivos (ETFs): Alpha ~0 por diseño (replicar índice)

    R² (Bondad de ajuste):
      └─ >80%  ✓ Benchmark es muy representativo del fondo
      └─ 60-80%  ○ Benchmark es representativo
      └─ 40-60%  △ Benchmark parcialmente representativo
      └─ <40%  ✗ Benchmark muy diferente (considerar otro o sin benchmark)
      └─ En fondos con múltiples activos: R² bajo es esperado
```
  ── GRÁFICO SUBACUÁTICO (UNDERWATER CHART) ───────────────────────────────────    

    Panel superior: NAV base 100 (azul) + drawdown continuo (rojo).  
                    Zona roja = tiempo "bajo el agua" respecto al máximo histórico.  
                    Cada vez que NAV cae bajo su máximo anterior, el área roja crece.  

    Panel inferior izq.: Histograma retornos mensuales (verde/rojo) + curva normal
                        teórica (azul discontinuo).  
                        Si las colas son más gruesas que la curva: más sorpresas
                        extremas de lo esperado.  
                        P5 (naranja) = peor mes típico  
                        P95 (azul) = mejor mes típico  

    Panel inferior der.: % días bajo el agua por año.
                        Verde <20%   → excelente (renta fija/defensivos)  
                        Naranja 20-50% → normal (renta variable moderada)  
                        Rojo >50%   → preocupante (fondos muy volátiles)  
                        
                        Un fondo conservador no debería superar 20% en ningún año.  
                        En crisis 2008-2009: muchos fondos >80% bajo el agua.  

    Interpretación combinada:  
      Si Panel sup. tiene muchas "islas" roja → múltiples recuperaciones de máximos  
      Si Panel inf.izq. tiene colas muy gruesas → distribución no es normal  
      Si Panel inf.der. tiene barras rojas → periodos prolongados de pérdidas  

  ── FRONTERA EFICIENTE (opción 8) ────────────────────────────────────────────       

    Cada punto de la nube = una cartera simulada (8.000 simulaciones).  
    Color del punto = Sharpe (verde=alto, rojo=bajo).
      
    ★ Cartera de Sharpe máximo  → mejor relación rentabilidad/riesgo
                                  (punto más al noroeste de la nube).  
    ◆ Cartera de mínima varianza → menor riesgo posible con estos activos
                                  (punto más a la izquierda).  
    ● Cartera equi-ponderada     → referencia igualitaria (1/N pesos).  
    ◇ Cartera actual             → composición presente de tu cartera.  

    Lectura:  
    ├─ Si Cartera actual está lejos (SE) de ★ → hay margen de mejora
    ├─ Si Cartera actual está cerca de ◆ → muy conservadora
    ├─ Si Cartera actual está en la nube densa → buena diversificación
    └─ Si Cartera actual está aislada → concentrada en pocos activos

    Caveats:  
    ├─ La frontera no considera fiscalidad ni restricciones de liquidez
    ├─ Supone que la correlación histórica se mantiene (no es cierto en crisis)
    ├─ Los retornos esperados futuros pueden diferir de los históricos
    └─ Considera cambios de pesos, no rebalanceos periódicos (costes)

  ── VaR Y CVaR (opción 8) ────────────────────────────────────────────────────    

    Tres métodos calculados:
  
    1. VaR Histórico (95%):  
       └─ Percentil 5 de los retornos históricos mensual.
       └─ Más robusto en distribuciones no-normales.
       └─ Para cartera RF de renta fija:  
          ├─ VaR mensual < -1%  ✓ Muy bajo (monetarios)
          ├─ VaR mensual -1% a -3%  ○ Moderado (RF corta/media)
          ├─ VaR mensual -3% a -5%  △ Elevado (RF larga)
          └─ VaR mensual < -5%  ✗ Revisar composición

    2. VaR Paramétrico (normal):  
       └─ Supone distribución normal: Retorno_medio - 1.645*Volatilidad (para 95%)
       └─ Subestima el riesgo si hay colas gruesas (kurtosis > 0)
       └─ Pero es rápido de calcular y actualizar

    3. CVaR / Expected Shortfall (media de pérdidas en peor 5%):  
       └─ Siempre mayor en valor absoluto que VaR.
       └─ Más conservador y recomendado por reguladores (Basilea III)
       └─ Para tomar decisiones de riesgo extremo: usar CVaR, no VaR.

    Ejemplo de interpretación:  
    ├─ VaR 95% mensual = -2.5%  →  en el peor mes de 20 (5%), pérdida ≥ 2.5%
    ├─ CVaR 95% mensual = -3.8%  →  media de pérdidas en el 5% peor de los meses
    ├─ Si cartera = 100.000 €:
    │  ├─ Riesgo normal (VaR): -2.500 €
    │  └─ Riesgo extremo (CVaR): -3.800 €
    └─ En crisis, diferencia crece (VaR subestima mucho)

  ── CORRELACIONES (opción 5) ─────────────────────────────────────────────────    

    Correlación estática (período completo):  
      >0.80  ✗ Alta correlación, diversificación limitada
      0.40–0.80  ○ Correlación moderada, diversificación parcial
      0.00–0.40  ✓ Baja correlación, buena diversificación real
      <0.00  ✓✓ Correlación negativa (ideal, se compensan las bajadas)

    Correlación rodante (ventana 60 días):  
      └─ Muestra cómo evolucionan las correlaciones en el tiempo
      └─ Si sube >0.30 en pocas semanas → posible co-movimiento o evento de mercado
      └─ En crisis las correlaciones convergen hacia +1 → diversificación "falla"
      └─ La banda punteada marca desviación estándar histórica
      └─ Si sale de la banda → comportamiento anómalo

    Matriz de calor (heatmap):  
      └─ Células verdes (correlación negativa) → diversificación excelente
      └─ Células amarillas (correlación ~0.5) → diversificación buena
      └─ Células rojas (correlación >0.8) → diversificación pobre

    Detección de crisis por correlación:  
      └─ Si MUCHAS correlaciones pares suben simultáneamente
      └─ Y convergen hacia +1 en pocas semanas
      └─ → Probable event de estrés sistémico (crisis de mercado)
      └─ Acciones a tomar: revisar VaR, aumentar RF, vender volátiles

  ── ANÁLISIS TÉCNICO (opción 7) ──────────────────────────────────────────────    

| Indicador   | Fórmula / Descripción                         | Señal +                         | Señal -                         |
|-------------|-----------------------------------------------|----------------------------------|----------------------------------|
| **SMA**     | Promedio móvil simple (20, 50, 200 días)      | Cruce dorado (50 > 200)          | Cruce de la muerte (50 < 200)    |
| **Bollinger** | Media ± 2·Desv.Est. (20d)                   | NAV en banda inferior            | NAV en banda superior            |
| **Squeeze** | Bandwidth < P10 histórico                     | Calma antes de la tormenta       | —                                |
| **MACD**    | (EMA12 – EMA26) vs EMA9 señal                 | Cruce alcista (L>S, hist>0)      | Cruce bajista (L<S, hist<0)      |
|             | Histograma = diferencia                       |                                  |                                  |
| **ATR**     | Rango verdadero promedio (14 días)            | Bajo (vol ↓) = oportunidad       | Alto (vol ↑) = riesgo            |
| **RSI**     | Fuerza relativa (14 días, escala 0–100)       | Divergencia alcista (RSI↓, NAV↑) | Divergencia bajista (RSI↑, NAV↓) |
|             |                                               | RSI 30–70 neutral                | >80 o <20 extremo                |

```
    Aplicabilidad según tipo de fondo:  
    ├─ RF ultra corto / Monetario: ESCASA UTILIDAD (volumen muy bajo)
    ├─ RF corto-medio plazo: BAJA-MEDIA (menos ruido que acciones)
    ├─ RF largo plazo: MEDIA (máxima sensibilidad a tasas de interés)
    ├─ Renta variable: ALTA (ruido técnico, reversiones, momentum)
    └─ Acciones individuales: ALTA (máxima especulación)

    Estrategia de trading técnico:  
    └─ Usar MÚLTIPLES indicadores (no solo uno)
    └─ Esperar CONFIRMACIÓN entre indicadores
    └─ Ejemplo: Cruce alcista MACD + RSI <70 + SMA bullish
    └─ Usar ATR para ajustar stop-loss (p.ej. -2*ATR desde entrada)
    └─ Nunca ignorar el fundamento (técnico es corto plazo)

    Limitaciones:  
    ├─ Profecía autocumplida: todos usan los mismos indicadores
    ├─ Genera falsos positivos en consolidaciones laterales
    ├─ No funciona en mercados sin tendencia (range-bound)
    ├─ Máxima efectividad en mercados trending y volátiles
    └─ Stop-loss técnico puede ser ejecutado por ruido intradiario
```

  ── HEATMAP MENSUAL (CALENDAR HEATMAP) ───────────────────────────────────────    

    Estructura: Filas = Años, Columnas = Meses (Ene-Dic)  
    Color de cada celda = Retorno mensual (verde=positivo, rojo=negativo)  
    Intensidad del color = Magnitud del retorno  

    Lecturas útiles:  
    ├─ Buscar patrones estacionales (p.ej. enero fuerte, verano débil)
    ├─ Identificar años problemáticos (fila muy roja)
    ├─ Meses recurrentemente flojos (columna con más rojo)
    ├─ Evolución temporal (¿empeora en años recientes?)
    └─ Simetría de retornos (¿más positivos que negativos?)

    Para gestores:  
    ├─ Gestor A: Heatmap verde mayormente → valor añadido consistente
    ├─ Gestor B: Alternancia verde/rojo → rentabilidad errática
    ├─ Si gestor A bate benchmark > 60% de meses → Alpha real


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
4. DEPENDENCIAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    

  ── INSTALACIÓN ──────────────────────────────────────────────────────────────    

    pip install yfinance openpyxl pandas matplotlib scipy

| Paquete     | Versión mín.   | Para qué se usa                                                |
|-------------|----------------|-----------------------------------------------------------------|
| **pandas**      | 2.0            | DataFrames, resampleo, retornos, series temporales             |
| **yfinance**    | 0.2            | Descarga de cotizaciones desde Yahoo Finance                   |
| **openpyxl**    | 3.1            | Lectura/escritura de .xlsx con estilos                         |
| **matplotlib**  | 3.7            | Gráficas (base 100, técnico, subacuático, heatmap)             |
| **scipy**       | 1.11           | Markowitz, VaR paramétrico, normal, optimización, curvas       |
| **numpy**       | (con pandas)   | Cálculos vectoriales y métricas                                |
| **reportlab**   | (opcional)     | Generación avanzada de PDF (futuro)                            |

  ── INSTALACIÓN EN DIFERENTES ENTORNOS ───────────────────────────────────────    

    En Linux/Mac terminal:  
      $ pip install --upgrade pip
      $ pip install yfinance openpyxl pandas matplotlib scipy

    En Anaconda Prompt (Windows):  
      > conda install -c conda-forge yfinance openpyxl pandas matplotlib scipy

    En Google Colab (ejecutar en celda):  
      !pip install yfinance openpyxl --upgrade

    En Jupyter sin conda:  
      import sys  
      !{sys.executable} -m pip install yfinance openpyxl scipy --upgrade

  ── ENTORNOS SOPORTADOS ──────────────────────────────────────────────────────    

· Python 3.10, 3.11, 3.12 (3.13 en desarrollo)  
· Jupyter Notebook / JupyterLab (recomendado para uso interactivo)  
· Google Colab (monta Google Drive automáticamente)  
· Terminal / línea de comandos (modo texto sin gráficas interactivas)  
· Anaconda / conda — instalación recomendada para usuarios no técnicos 
· VSCode con extensión Jupyter

Instalación recomendada para usuarios sin experiencia:  
  1. Descargar Anaconda desde https://www.anaconda.com  
  2. Abrir Anaconda Navigator → crear entorno Python 3.11  
  3. Lanzar Jupyter Notebook desde Navigator  
  4. En terminal de Jupyter: pip install yfinance openpyxl scipy  

    Para compatibilidad máxima:  
      pip install pandas>=2.0 yfinance>=0.2 openpyxl>=3.1 scipy>=1.11 matplotlib>=3.7  

  ── DATOS EXTERNOS ───────────────────────────────────────────────────────────    
```    Yahoo Finance (gratuito, sin clave):  
      └─ Cotizaciones históricas de fondos, ETFs, acciones e índices
      └─ Limitación: fondos monetarios publicados sin cupones (NAV plano)
      └─ El programa detecta y avisa este caso automáticamente
      └─ Latencia ~15-20 min para datos intradiarios
      └─ Datos EOD (fin de día) disponibles al día siguiente

    Datos macroeconómicos (futuro):  
      └─ FRED (Federal Reserve Economic Data) para tasas, inflación, paro
      └─ Se obtendrá en: https://fred.stlouisfed.org/docs/api/api_key.html
      └─ Clave de API gratuita para usuarios registrados
      └─ Versión futura integrará automáticamente
```
    No se requiere clave de API para las funcionalidades actuales.

  ── FICHEROS DE DATOS ────────────────────────────────────────────────────────    

    Formato CSV esperado en Datos_CSV/:  
      ├─ Columna obligatoria : Date  (formato YYYY-MM-DD o similar)
      ├─ Columna de precio   : Adj Close  (preferida) o  Close
      ├─ Generado por el programa automáticamente al descargar de Yahoo Finance
      └─ Estructura esperada:
            Date,       Close,    Adj Close,    Volume
            2024-01-02, 123.45,   123.45,       1000000
            2024-01-03, 124.10,   124.10,       900000
            ...

    Para planes de pensiones o fondos sin ticker Yahoo:  
      ├─ Crear manualmente un CSV con las columnas Date y Close
      ├─ NAV unitario diario (NO el valor total de la posición)
      ├─ Formato fecha: YYYY-MM-DD
      └─ Ejemplo:
            Date,       Close
            2024-01-02, 50.123
            2024-01-03, 50.456
            ...

    Validación automática del programa:  
      ├─ Detecta columnas faltantes
      ├─ Convierte fechas a formato estándar
      ├─ Rellena huecos (forward fill si <5%, error si >5%)
      └─ Avisa si hay datos duplicados (por fecha)

  ── REQUISITOS DE SISTEMA ────────────────────────────────────────────────────    

    Espacio en disco:  
      ├─ Programa principal: 500 KB
      ├─ Datos para 50 fondos (5 años): ~100 MB
      ├─ Excels de carteras: <1 MB cada uno
      ├─ PDFs exportados: 2-5 MB cada uno
      └─ Total recomendado: 500 MB

    Memoria RAM:  
      ├─ Mínimo: 2 GB (análisis de carteras pequeñas <100 fondos)
      ├─ Recomendado: 4-8 GB (para 100-500 fondos, cálculo Markowitz)
      ├─ Simulación Markowitz (8.000 carteras): ~200 MB temporal
      └─ No es paralizable (uso single-thread)

    Conexión a internet:  
      ├─ Primera descarga de todos los fondos: 30-60 min dependiendo de volumen
      ├─ Actualización semanal de 20 fondos: 5-10 min
      ├─ Ancho de banda: ~50 MB por 100 fondos/5 años
      └─ Se puede ejecutar offline si los CSVs ya están descargados


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
5. METODOLOGÍA Y REFERENCIAS  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
```
  ── FUENTES TEÓRICAS ─────────────────────────────────────────────────────────    

    Teoría Moderna de Carteras (MPT — Markowitz 1952):  
      └─ Referencias en código: frontera eficiente, pesos óptimos
      └─ Libro: "Portfolio Selection" — Harry Markowitz
      └─ Limitaciones: asume normalidad de retornos (en crisis no se cumple)

    Capital Asset Pricing Model (CAPM):  
      └─ Fórmula: E(Rx) = Rf + β(E(Rm) - Rf)
      └─ Usado para calcular Alpha: Rx - [Rf + β(Benchmark - Rf)]
      └─ Referencias: William Sharpe (1964)
      └─ Limitaciones: relación lineal beta-retorno (simplista)

    Análisis de Riesgo de Colas (Tail Risk):  
      └─ CVaR / Expected Shortfall como mejora sobre VaR
      └─ Método de valor en riesgo condicional
      └─ Regulación: Basilea III (instituciones financieras)
      └─ Acevedo et al. "Conditional Value-at-Risk" (2002)

    Análisis Técnico:  
      └─ Elliott Wave, Dow Theory, patrones de velas
      └─ MACD: Gerald Appel (1979)
      └─ Bandas de Bollinger: John Bollinger (1983)
      └─ RSI: J. Welles Wilder Jr. (1978)
      └─ Crítica académica: "A Random Walk Down Wall Street" (Burton Malkiel)

    Metodología Morningstar:  
      └─ Sharpe y Sortino calculados con retornos MENSUALES
      └─ Tasa libre de riesgo = Euribor 3M del período
      └─ Comparación con fondos peer de la misma categoría
      └─ Rating de estrellas basado en Morningstar Risk-Adjusted Return
```
  ── DECISIONES DE DISEÑO EN EL CÓDIGO ────────────────────────────────────────    
```
    1. Retornos logarítmicos vs simples:  
       └─ Se usa LOG porque: mejor comportamiento en compounding,
          propiedades estadísticas más limpias, menos sesgo en distribución.
       └─ Fórmula: r = ln(P_t / P_{t-1})

    2. Volatilidad anualizada:  
       └─ Fórmula: σ_anual = σ_diaria × √252 (días de trading/año)
       └─ No es: σ_diaria × 252 (eso sería error común)

    3. Sharpe Ratio:  
       └─ Usa Euribor 3M trimestral como Rf
       └─ Se calcula con RETORNOS MENSUALES, no diarios
       └─ Motivo: Morningstar standard, menos ruido en datos mensuales

    4. Beta:  
       └─ Regresión lineal: Fondo vs Benchmark (mínimos cuadrados)
       └─ Ventana: últimos 3 años si disponible, sino máximo histórico
       └─ Interpretación: β=1.2 significa sube 12% si benchmark sube 10%

    5. Alpha:  
       └─ Fórmula: α = (Retorno_fondo) - [Rf + β(Retorno_benchmark - Rf)]
       └─ Anualizado: α_anual = α_mensual × 12
       └─ Positivo = gestor agrega valor, Negativo = destruye valor

    6. Max Drawdown:  
       └─ Máxima caída DESDE UN MÁXIMO hasta cualquier mínimo posterior
       └─ NO es la diferencia entre máximo y mínimo del período
       └─ Fórmula: DD = (Precio_min - Precio_max) / Precio_max

    7. VaR Histórico:  
       └─ Percentil 5 de retornos mensuales históricos
       └─ Se ordena: -sorteo retornos -coge el percentil P5
       └─ Ventaja: no asume distribución normal
       └─ Desventaja: necesita muchos datos (~5 años mínimo)

    8. CVaR / Expected Shortfall:  
       └─ Media de retornos PEORES que el VaR
       └─ Siempre > VaR en valor absoluto (más conservador)
       └─ No asume normalidad
       └─ Recomendado por reguladores modernos

    9. Frontera Eficiente:  
       └─ Monte Carlo: 8.000 carteras aleatorias
       └─ Para cada una: calcula Sharpe y almacena
       └─ Luego: optimización con scipy.optimize.minimize para ★ y ◆
       └─ Razón: Monte Carlo más robusto en n activos > 5

    10. Análisis Técnico:  
        └─ SMA con pandas.rolling().mean()
        └─ MACD: EMA12 - EMA26, señal = EMA9
        └─ ATR: Range true = max(H-L, |H-Close_prev|, |L-Close_prev|)
        └─ RSI: RS = (Gains_avg / Loss_avg), RSI = 100 - (100/(1+RS))
```
  ── LIMITACIONES Y CAVEATS ───────────────────────────────────────────────────    
```
    Limitaciones de datos:  
    ├─ Fondos monetarios: NAV no incluye cupones acumulados → rentabilidad incorrecta
    ├─ Yahoo Finance: latencia 15-20 min en datos, puede haber gaps
    ├─ Fondos jóvenes (<1 año): insuficientes datos para métricas robustas
    ├─ ETFs sintéticos (swap): tracking error puede ser alto, no captado aquí
    └─ Fondos cerrados: pueden tener spreads bid-ask superiores a lo normal

    Limitaciones teóricas:  
    ├─ Markowitz: asume normalidad (en crisis hay colas gruesas) → VaR subestimado
    ├─ CAPM: relación lineal β-retorno (en realidad hay estructuras más complejas)
    ├─ Correlaciones: supone estables (en crisis convergen todas hacia +1)
    ├─ Bench mark: único vs múltiples factores (Fama-French sería mejor)
    └─ Retornos pasados: no garantizan futuros ("past performance is not indicative...")

    Limitaciones prácticas:  
    ├─ Costes de transacción: frontera eficiente no los considera
    ├─ Fiscalidad: no calcula IRPF/impuestos sobre ganancias
    ├─ Liquidez: supone venta inmediata al precio actual
    ├─ Restricciones: no permite posiciones cortas (short selling)
    ├─ Rebalanceo: frontera es estática, no dinámicas
    └─ Cambio de divisa: todos los CSVs en misma moneda (ojo con internacionales)
```
  ── CÓMO COMBATIR ESTOS PROBLEMAS ────────────────────────────────────────────    
```
    1. Datos de fondos monetarios:  
       └─ Solución: obtener NAV+cupones acumulados del folleto del fondo
       └─ O: usar iShares Money Market ETF (VMVX) como proxy

    2. Insuficientes datos:  
       └─ Solución: para fondos <1 año usar Benchmark proxy (peer group)
       └─ O: esperar a 1 año de datos para confianza estadística

    3. Markowitz subestima riesgo en crisis:  
       └─ Solución: aumentar VaR teórico 1.5x-2x para stress testing
       └─ O: usar modelo de colas pesadas (Student-t distribution)

    4. Correlaciones cambian en crisis:  
       └─ Solución: usar correlación rodante (ventana 60d)
       └─ O: tener cartera con activos con correlación negativa acreditada (oro, bonos)

    5. No considerar costes:  
       └─ Solución: restar comisiones a retornos calculados (α_ajustado)
       └─ Fórmula: α_real = α_calculado - comisión_anual(%)

    6. Fiscalidad:  
       └─ Solución: calcular IRPF = ganancias * 19% (España)
       └─ Rentabilidad neta = rentabilidad_bruta - IRPF
       └─ (Pero esto requiere interacción con sistema tributario)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
6. EJEMPLOS DE USO AVANZADO  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    

  ── SCENARIO 1: INVERSOR CONSERVADOR CON FONDO MONETARIO ──────────────────────    

    Objetivo: Verificar que la cartera genera caja sin sorpresas.  
```    
    Pasos:  
    1. Descargar cotizaciones (opción 1)
    2. Actualizar cartera (opción 2)
    3. Revisar métricas (opción 4):
       └─ Buscar Volatilidad < 0.5% (normal)
       └─ Sharpe > 0.5 (mínimo esperado)
       └─ Si vol > 1% o Sharpe < 0 → problemas de calidad crediticia
    4. Revisar gráfico subacuático (opción 7):
       └─ % días bajo el agua debería ser <5% (fondos monetarios)
       └─ Si aparecen islas de rojo extensas → cambios de calidad

    Acción recomendada:  
    └─ Si métricas normales: hodl (mantener posición sin cambios)
    └─ Si volatilidad anormal: revisar composición (hay de crédito)
    └─ Si downgrade de rating: considerar salida
    └─ Rebalanceo: no necesario (posición defensiva estática)
```
  ── SCENARIO 2: INVERSOR MODERADO CON CARTERA BALANCEADA 50/50 ────────────────    

    Objetivo: Verificar que la cartera mantiene equilibrio riesgo/retorno.
```    
    Pasos:  
    1. Actualizar cartera (opción 2)  
    2. Ver correlaciones (opción 5):  
       └─ RF vs RV correlación debería ser 0.30-0.50 (buena diversificación)
       └─ Si >0.70 → mercado acoplado, comprar activos descorrelacionados
       └─ Si <0.20 → poco movimiento de RV (mercado plano o deflacionista)
    3. Análisis agregado (opción 8):  
       └─ Frontera eficiente: ¿está la cartera cerca de ★?
       └─ VaR mensual: ¿está dentro de tolerancia (p.ej. -3%)?
       └─ Contribución riesgo: ¿RF <30%, RV >70% del riesgo?
    4. Exportar PDF (opción 6): informe para asesor  

    Acción recomendada:  
    └─ Si Sharpe <0.5 para cartera balanceada → ineficiente, rebalancear
    └─ Si correlación RF/RV sube >0.70 → evento sistémico, aumentar RF
    └─ Si VaR sale de límite → reducir RV
    └─ Rebalanceo anual (trimestral en volatilidad alta)
```
  ── SCENARIO 3: GESTOR DE CARTERAS MULTICLIENTE ──────────────────────────────    

    Objetivo: Comparar desempeño de múltiples carteras vs benchmark.  
```    
    Pasos:  
    1. Cargar cartera cliente A (opción B)
    2. Ver métricas (opción 4) y Alpha vs benchmark:
       └─ Repetir para clientes B, C, D...
    3. Consolidar resultados en Excel exportado (opción 6)
    4. Identificar fondos con Alpha positivo consistente (>0.5% anual)
    5. Identificar fondos con correlación alta con benchmark (R² > 90%):
       └─ Candidatos para cambio a fondos indexados (menor comisión)

    KPIs monitoreados:  
    ├─ Alpha medio por cartera: media ponderada de αs de fondos
    ├─ % fondos batiendo benchmark: >50% es signo de valor
    ├─ Volatilidad vs benchmark: si cartera es más volátil con mismo α → ineficiente
    ├─ Ratio Sharpe cartera: >0.7 es objetivo mínimo
    └─ Máximo drawdown vs benchmark: cartera no debe ser peor

    Reportes:  
    └─ Mensual: Alpha, Sharpe, Drawdown por cartera
    └─ Trimestral: análisis técnico, heatmaps estacionales
    └─ Anual: revisión de benchmarks, rotación de fondos
```
  ── SCENARIO 4: TRADER TÉCNICO EN ACCIONES ───────────────────────────────────    

    Objetivo: Identificar señales técnicas para entrada/salida corto plazo.  
```    
    Pasos:  
    1. Cargar acción individual (p.ej. AAPL) (opción 1)
    2. Análisis técnico avanzado (opción 7):
       └─ SMA: ¿está en cruce dorado (50>200)?
       └─ MACD: ¿acaba de girar positivo?
       └─ Bollinger: ¿está en banda inferior (rebote)?
       └─ RSI: ¿está <30 (sobreventa)?
    3. Si MÚLTIPLES indicadores confirman → entrada larga
    4. Poner stop-loss 2*ATR bajo entrada
    5. Objetivo: 1.5-2x del ATR de ganancia

    Trade setup ejemplo:  
    ├─ Precio NAV 150 €
    ├─ ATR(14) = 3 €
    ├─ Entrada larga: cuando Cruce dorado SMA (50>200) + RSI gira >30
    ├─ Stop loss: 150 - 2*3 = 144 € (riesgo 6 €)
    ├─ Target: 150 + 1.5*3 = 154.5 € (ganancia 4.5 €)
    ├─ Risk/Reward: 6/4.5 = 1.33x (aceptable)
    └─ Esperar confirmación de volumen

    Limitación:  
    └─ Técnico sin fundamental = casino (máximo uso 10-20% cartera)
```
  ── SCENARIO 5: ANÁLISIS POST-CRISIS (ESTRÉS SISTÉMICO) ──────────────────────    

    Objetivo: Cuantificar impacto de shock de mercado.  
```    
    Pasos:  
    1. Descarga de datos: activar rango largo (5-10 años)
    2. Correlación rodante (opción 5):  
       └─ Buscar período de crisis (2008, 2011, 2020, 2022)
       └─ Observar convergencia todas correlaciones → +0.9-1.0
       └─ Duración del pico (semanas, meses?)
    3. Gráfico subacuático (opción 7):  
       └─ % días bajo el agua en 2008 → probablemente >60-80%
       └─ Drawdown máximo: típicamente -40% a -60% en acciones
    4. VaR histórico (opción 8):  
       └─ Construir escenarios:  
       └─ "¿Si repite 2008, cuál es máxima pérdida?"
       └─ Respuesta: máximo drawdown histórico
    5. Stress test:  
       └─ "¿Si cae 20% más de lo peor visto?" → aplicar factor 1.2x al drawdown

    Acciones recomendadas:  
    ├─ Si cartera tiene correlación RF/RV < 0.5: buena diversificación
    ├─ Si tiene > 0.7: cambiar a fondos decorrelacionados (oro, bonos LT)
    ├─ Aumentar % RF: cada 1% más de RF reduce drawdown ~0.5-1%
    ├─ Considerar futuros o opciones de protección (VIX)
    └─ Rebalanceo: contraciclíco (vender ganadores, comprar perdedores)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
7. AVISO LEGAL  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    

  Este programa es una herramienta de análisis personal y seguimiento de
  carteras de inversión. No constituye asesoramiento financiero, fiscal ni
  legal de ningún tipo.

  Los resultados que genera —métricas, gráficas, diagnósticos, sugerencias
  de pesos, VaR, frontera eficiente— son puramente informativos y no deben
  interpretarse como recomendaciones de compra, venta o mantenimiento de
  ningún instrumento financiero.

  El autor no se responsabiliza de las decisiones de inversión que el usuario
  pueda tomar basándose en los resultados del programa, ni de las pérdidas
  patrimoniales que pudieran derivarse de dichas decisiones.

  Los datos de cotizaciones se obtienen de Yahoo Finance y pueden diferir
  de los datos oficiales publicados por las gestoras, depositarios o
  mercados regulados. Yahoo Finance no garantiza la exactitud, integridad
  ni actualidad de sus datos.

  Para fondos monetarios, Yahoo Finance no incluye los cupones en el NAV
  publicado, lo que produce métricas de rendimiento y riesgo incorrectas.
  El programa detecta esta situación y emite un aviso, pero no corrige
  los datos automáticamente.

  En España: Este programa no está regulado por la CNMV. Su uso no sustituye
  la asesoramiento de un profesional financiero certificado (SNMV/CNMV).

  Consulte siempre a un asesor financiero profesional regulado (CNMV en
  España) antes de tomar cualquier decisión de inversión relevante.

  USO BAJO RESPONSABILIDAD PROPIA: El usuario acepta que usa este programa
  enteramente bajo su responsabilidad. El autor rechaza toda responsabilidad
  civil, penal o administrativa derivada del uso de este programa.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
8. LICENCIA DE USO  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    

  Creative Commons BY-NC 4.0 — Atribución – No Comercial

  Este proyecto y su documentación se distribuyen bajo licencia
  Creative Commons BY-NC 4.0 (Atribución – No Comercial).

  SE PERMITE:
    · Usar, copiar y adaptar el código con fines educativos o personales.
    · Compartir versiones modificadas citando la fuente original.
    · Integrar en proyectos personales o académicos sin ánimo de lucro.
    · Enseñanza y divulgación (blogs, tutoriales, universidades).

  NO ESTÁ PERMITIDO:
    · Uso comercial del código o derivados del mismo.
    · Redistribución con fines lucrativos o en productos de pago.
    · Integración en plataformas de asesoramiento automatizado (robo-advisors).
    · Uso por fondos, gestoras u otros intermediarios financieros.
    · Venta del código o documentación asociada.
    · Eliminar o modificar los avisos de autoría y licencia.

  Texto completo de la licencia:
    https://creativecommons.org/licenses/by-nc/4.0/deed.es

  Cita sugerida:
    "Gestor de Cartera de Valores en Python — actualizar_cartera.py
     Versión 2.0 · Publicado en [plataforma] bajo licencia CC BY-NC 4.0"

  Preguntas frecuentes sobre la licencia:
    P: ¿Puedo usar esto en mi startup financiera?
    R: No, es NO-COMERCIAL. Si esperas generar ingresos, solicita licencia
       por separado.

    P: ¿Puedo enseñarlo en mi universidad?
    R: Sí, educación es permitido. Cita la fuente.

    P: ¿Puedo hacer una API REST con este código?
    R: No, eso sería comercial. Pregunta al autor.

    P: ¿Puedo traducir la documentación a otro idioma?
    R: Sí, siempre que cites y mantengas la licencia CC BY-NC.

    P: ¿Puedo usarlo si los datos son de acceso libre?
    R: El dato acceso libre no revoca la licencia. La restricción es sobre
       el código/programa, no sobre los datos.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
9. ROADMAP Y MEJORAS FUTURAS  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
```
  Versión 2.1 (Próximo mes):
  ├─ Soporte para fondos de fondos (FoF)
  ├─ Cálculo de beta rolling (ventana móvil 60d)
  ├─ Gráfico de contribución de retorno por activo
  └─ Exportación a CSV con todas las métricas

  Versión 2.2 (3 meses):
  ├─ Integración con FRED (datos macroeconómicos)
  ├─ Correlación con tasa de cambio EUR/USD
  ├─ Factor models (Fama-French 5 factores)
  ├─ Análisis de performance attribution (Brinson-Fachler)
  └─ Alertas automáticas (email/Telegram)

  Versión 3.0 (6 meses):
  ├─ Machine learning: predicción de correlaciones (LSTM)
  ├─ Optimización con restricciones (mínimo/máximo por activo)
  ├─ Backtesting de estrategias técnicas
  ├─ Interfaz gráfica (PyQt o Streamlit)
  ├─ Base de datos (SQLite o PostgreSQL) en lugar de CSVs
  └─ API REST para integración con brokers (Saxo, Degiro)

  Versión 3.1 (9 meses):
  ├─ Simulación de Montecarlo de trayectorias futuras
  ├─ Cálculo de capital necesario (subnormación)
  ├─ Integración fiscal (IRPF automático por jurisdicción)
  ├─ Análisis de cambio de divisa (FX hedging)
  └─ Comparación con robo-advisors del mercado

  Funcionalidades lejanas (futuro):
  ├─ Órdenes automáticas directas al broker
  ├─ Ejecutar trades basado en señales técnicas
  ├─ Rebalanceo automático
  ├─ Sincronización multi-dispositivo (cloud)
  └─ App móvil (iOS/Android)

  Contributing:
  └─ Para reportar bugs: github.com/[proyecto]/issues
  └─ Para sugerencias: github.com/[proyecto]/discussions
  └─ Para pull requests: ver CONTRIBUTING.md
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
10. SOPORTE Y CONTACTO  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
```
  Reportar bugs:
  └─ GitHub Issues: [enlace del proyecto]
  └─ Email: [email del autor]
  └─ Título: "[BUG] Descripción breve"

  Solicitar funcionalidad:
  └─ GitHub Discussions: [enlace del proyecto]
  └─ Incluir caso de uso y justificación

  Documentación online:
  └─ Wiki: [enlace]
  └─ Blog: [enlace]
  └─ Video tutoriales: [enlace YouTube]

  Comunidad:
  └─ Discord: [enlace]
  └─ Telegram: [enlace]
  └─ Reddit: r/[comunidad]

  Financiar el proyecto:
  └─ GitHub Sponsors: [enlace]
  └─ Patreon: [enlace]
  └─ Compra de café: [buymeacoffee]

  Preguntas frecuentes: ver FAQ.md en el repositorio

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
11. CHANGELOG  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    
```
  v2.0 (2026-05-02):
  ├─ Release inicial de versión 2.0
  ├─ Soporte para 7 clases modularizadas
  ├─ Análisis técnico avanzado (SMA, MACD, Bollinger, ATR, RSI)
  ├─ Frontera eficiente Markowitz (Monte Carlo 8.000 carteras)
  ├─ VaR histórico, paramétrico y CVaR
  ├─ Correlación estática y rodante
  ├─ Exportación PDF y Excel
  ├─ Gráfico subacuático con histograma de retornos
  ├─ Heatmap mensual y anual
  ├─ Soporte multi-entorno (Jupyter, Colab, CLI, Anaconda)
  ├─ Documentación completa y ejemplos
  └─ Licencia CC BY-NC 4.0

  v1.9 (2026-04-15):
  ├─ Corrección de bugs en descarga de Yahoo Finance
  ├─ Optimización de rendimiento en Markowitz (paralización)
  ├─ Mejora de manejo de excepciones
  └─ Actualización de dependencias

  v1.0 (2025-01-01):
  ├─ Versión inicial beta
  ├─ Gestión de carteras básica
  ├─ Métricas Sharpe, Sortino, máx drawdown
  └─ Exportación a Excel

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    

                              FIN DE DOCUMENTACIÓN

  Última actualización: 2026-05-02
  Versión: 2.0
  Mantenidor: [autor]
  Licencia: CC BY-NC 4.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  