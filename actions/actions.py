from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionValidateCreditApplication(Action):
    def name(self) -> Text:
        return "action_validate_credit_application"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        credit_type = tracker.get_slot("credit_type")
        credit_amount = tracker.get_slot("credit_amount")
        income = tracker.get_slot("income_info")
        age = tracker.get_slot("age_verification")
        employment_status = tracker.get_slot("employment_status")
        
        # Validación de edad
        if age and age < 18:
            dispatcher.utter_message(
                text="❌ Debes ser mayor de edad (18 años) para solicitar un crédito."
            )
            return []
        
        if age and age > 75:
            dispatcher.utter_message(
                text="⚠️ La edad máxima permitida al finalizar el crédito es de 75-80 años. "
                     "Esto podría afectar el plazo disponible para tu crédito."
            )
        
        # Validación de capacidad de pago
        if income and credit_amount:
            monthly_payment_estimate = (credit_amount * 0.01)  # Estimación básica
            debt_to_income_ratio = monthly_payment_estimate / income
            
            if debt_to_income_ratio > 0.3:
                dispatcher.utter_message(
                    text="⚠️ El pago mensual estimado excede el 30% de tus ingresos. "
                         "Te recomendamos ajustar el monto para mejorar las posibilidades de aprobación."
                )
            else:
                dispatcher.utter_message(
                    text="✅ Los datos preliminares lucen bien. Procederemos con la evaluación completa."
                )
        
        # Mensaje específico según tipo de crédito
        if credit_type == "liquidez":
            dispatcher.utter_message(
                text="💡 **Importante para crédito de liquidez:** El monto máximo será determinado "
                     "por el avalúo de tu inmueble (generalmente hasta 50-65% del valor comercial) "
                     "y tu capacidad de pago."
            )
        
        return []