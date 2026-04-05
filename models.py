from enum import IntEnum
from pydantic import BaseModel, Field

class GridAction(IntEnum):
    TOGGLE_SOLAR = 0
    TOGGLE_WIND = 1
    CONNECT_BATTERY = 2

class ActionModel(BaseModel):
    action: GridAction = Field(description="The energy source you want to toggle")

class ObservationModel(BaseModel):
    is_demand_met: bool = Field(description="True if power supply equals or exceeds demand")
    carbon_footprint: float = Field(description="A score from 0 to 1 (lower is better)")
    grid_stability: str = Field(description="Status of the grid: STABLE, WARNING, or CRITICAL")
    # Link our new names to the names the internal system expects
IndustrialPowerGridAction = ActionModel
IndustrialPowerGridObservation = ObservationModel
