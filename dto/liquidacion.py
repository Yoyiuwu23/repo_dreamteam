# dto/liquidacion.py
from pydantic import BaseModel
from typing import Optional


class LiquidacionCreate(BaseModel):
    nombre: str
    rut: str
    cargo: str
    sueldo_base: float
    # En la UI se envía normalmente el número de horas extra; aquí lo aceptamos
    # y lo convertiremos a monto en los métodos de cálculo.
    horas_extras: float = 0.0


class LiquidacionResponse(LiquidacionCreate):
    id: int
    total: Optional[float] = None
    dias_trabajados: int = 30

    # Campos calculados
    horas_extras_monto: float = 0.0
    total_imponible: float = 0.0
    afp_monto: float = 0.0
    salud_monto: float = 0.0
    afc_monto: float = 0.0
    total_descuentos: float = 0.0
    liquido: float = 0.0
    gratificacion: float = 0.0

    # Identificadores (si se desean pasar desde la BD)
    contrato_id: Optional[int] = None
    afp_id: Optional[int] = None
    salud_id: Optional[int] = None
    afc_id: Optional[int] = None

    def calcular_horas_extras(self, horas: float, multiplier: float = 1.5) -> float:
        """
        Calcula el monto por horas extras a partir del número de horas.

        Asunciones:
        - Jornada diaria de 8 horas
        - Mes de referencia de 30 días
        - Pago por hora extra = (sueldo_base / 30 / 8) * multiplier

        Parámetros:
        - horas: número de horas extra trabajadas (float)
        - multiplier: multiplicador por hora extra (por defecto 1.5)

        Retorna el monto calculado y lo asigna a `horas_extras_monto`.
        """
        if horas is None:
            horas = 0.0
        sueldo_diario = self.sueldo_base / 30.0
        sueldo_hora = sueldo_diario / 8.0
        monto = horas * sueldo_hora * multiplier
        self.horas_extras_monto = round(monto, 2)
        return self.horas_extras_monto

    def calcular_afp(self, tasa_afp_pct: Optional[float] = None) -> float:
        """
        Calcula el descuento AFP sobre el total imponible.
        - tasa_afp_pct: porcentaje (ej. 11.44). Si es None, usa 10.0% por defecto.
        """
        tasa = tasa_afp_pct if tasa_afp_pct is not None else 10.0
        self.afp_monto = round(self.total_imponible * (tasa / 100.0), 2)
        return self.afp_monto

    def calcular_salud(self, tasa_salud_pct: Optional[float] = None) -> float:
        """
        Calcula el monto de salud (Fonasa / Isapre) sobre el total imponible.
        - tasa_salud_pct: porcentaje (ej. 7.0). Si es None, usa 7.0% por defecto.
        """
        tasa = tasa_salud_pct if tasa_salud_pct is not None else 7.0
        self.salud_monto = round(self.total_imponible * (tasa / 100.0), 2)
        return self.salud_monto

    def calcular_afc(self, tasa_afc_pct: Optional[float] = None) -> float:
        """
        Calcula la cotización AFC (seguro de cesantía) sobre el total imponible.
        - tasa_afc_pct: porcentaje (ej. 0.6). Si es None, usa 0.6% por defecto.
        """
        tasa = tasa_afc_pct if tasa_afc_pct is not None else 0.6
        self.afc_monto = round(self.total_imponible * (tasa / 100.0), 2)
        return self.afc_monto

    def calcular_total(self,
                       afp_pct: Optional[float] = None,
                       salud_pct: Optional[float] = None,
                       afc_pct: Optional[float] = None,
                       horas_multiplier: float = 1.5) -> float:
        """
        Calcula todos los montos relevantes para la liquidación:
        - convierte `self.horas_extras` (se interpreta como número de horas) a monto
        - calcula total imponible, descuentos (AFP, Salud, AFC) y líquido a pagar

        Parámetros opcionales (si provienen de la BD, pásalos aquí):
        - afp_pct, salud_pct, afc_pct: porcentajes (ej. 11.44, 7.0, 0.6)
        - horas_multiplier: multiplicador para horas extras (default 1.5)

        Retorna el líquido a pagar y lo asigna en `self.liquido` y `self.total`.
        """
        # Sueldo proporcional al período trabajado
        sueldo_diario = self.sueldo_base / 30.0
        sueldo_periodo = sueldo_diario * float(self.dias_trabajados)

        # Horas extras: interpretamos self.horas_extras como número de horas
        horas_input = float(self.horas_extras) if self.horas_extras is not None else 0.0
        self.calcular_horas_extras(horas_input, multiplier=horas_multiplier)

        # Gratificación: 30% del sueldo del periodo
        self.gratificacion = round(sueldo_periodo * 0.30, 2)

        # Total imponible (sueldo proporcional + horas extras + gratificación)
        self.total_imponible = round(sueldo_periodo + self.horas_extras_monto + self.gratificacion, 2)

        # Descuentos
        self.calcular_afp(afp_pct)
        self.calcular_salud(salud_pct)
        self.calcular_afc(afc_pct)

        self.total_descuentos = round(self.afp_monto + self.salud_monto + self.afc_monto, 2)

        # Líquido a pagar
        self.liquido = round(self.total_imponible - self.total_descuentos, 2)

        # Mantener compatibilidad: self.total almacenará el líquido a pagar
        self.total = self.liquido
        return self.liquido

