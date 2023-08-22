from .service import Service
from .model import Model



class EnergyImportCharge(Service):
    def __init__(
        self,
        model: Model,
        service_params: EnergyImportChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        
        return