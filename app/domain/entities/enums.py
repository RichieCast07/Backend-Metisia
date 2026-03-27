from enum import Enum

class BusinessType(str, Enum):
    panaderia = "panaderia"
    cafeteria = "cafeteria"
    dark_kitchen = "dark_kitchen"
    food_truck = "food_truck"
    otro = "otro"

class Plan(str, Enum):
    basico = "basico"
    pro = "pro"

class Unit(str, Enum):
    kg = "kg"
    g = "g"
    l = "l"
    ml = "ml"
    pza = "pza"
    caja = "caja"

class IngredientMovementType(str, Enum):
    entrada = "entrada"
    salida = "salida"
    ajuste = "ajuste"

class PromotionType(str, Enum):
    porcentaje = "porcentaje"
    monto_fijo = "monto_fijo"
    dos_por_uno = "dos_por_uno"

class PromotionApplicableTo(str, Enum):
    todo = "todo"
    categoria = "categoria"
    producto = "producto"

class CashRegisterStatus(str, Enum):
    abierta = "abierta"
    cerrada = "cerrada"

class WorkerPaymentType(str, Enum):
    automatico = "automatico"
    manual = "manual"

class PaymentMethod(str, Enum):
    efectivo = "efectivo"
    tarjeta = "tarjeta"
    transferencia = "transferencia"
    mixto = "mixto"

class ExpenseCategory(str, Enum):
    insumos = "insumos"
    renta = "renta"
    servicios = "servicios"
    nomina = "nomina"
    marketing = "marketing"
    otro = "otro"
