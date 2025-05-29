# API: Generador de Umbrales del Coeficiente R²

Este script automatiza el proceso de cálculo y almacenamiento de coeficientes de determinación (R²) para organizaciones ÚM. Además, genera umbrales por tipo de ajuste para pares relevantes de índices.

## Flujo del Proceso

Cada vez que se ejecuta el script:

### 1. Lista de organizaciones pendientes
- Se identifican todas las organizaciones de ÚM que aún **no tienen coeficientes R² calculados y almacenados** en el caché del script.

### 2. Bucle por organización
Por cada organización identificada en el paso anterior:

#### 2.1. Búsqueda de archivos relevantes
- Se buscan los siguientes archivos de datos:
  - `P Demography`
  - `IDT` (Índice de la Transacción)
  - `IDC` (Índice del Compromiso)
  - `IAL` (Índice del Ambiente Laboral)
  - `IDL` (Índice del Liderazgo)

#### 2.2. Filtro de AD
- Se filtran las áreas de desempeño que:
  - Tienen **al menos 14 personas**.
  - **No** hacen referencia a:
    - “Otros colaboradores”
    - “AD sin identificar”

#### 2.3. Cálculo del coeficiente R²
- Para las siguientes parejas:
  - `IDT` vs. `IDC`
  - `IAL` vs. `IDL`
- Se calcula el coeficiente R²g para cada función de ajuste:
  - Lineal
  - Exponencial
  - Logarítmica
  - Potencial

#### 2.4. Almacenamiento en caché
- Los valores de R² obtenidos se almacenan en el archivo `R2 Cache.csv`, el cual tiene como campos:
  - Encu_Id
  - Index Pair
  - Function
  - R2

### 3. Cálculo de umbrales de R²
- Con base en la información de `R2 Cache.csv`, se calculan **umbrales estadísticos** del coeficiente R²:
  - Por cada **pareja conceptualmente relevante de índices**
  - Por cada **tipo de función de ajuste**

### 4. Publicación de umbrales de R²
- Se actualizan los umbrales calculados en el paso 3. en el Google Sheets `R2 Thresholds`

## Consideraciones
- El script es **idempotente** si no cambia la base de organizaciones.
- Puede programarse para ejecución periódica o manual según necesidad operativa.

## Requisitos
- Python 3.8+
- Pandas
- NumPy

## Autor
Jaime Andrés Torres Duque, Analista Técnico
