from enum import IntEnum
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, Any

class GridAction(IntEnum):
    TOGGLE_SOLAR = 0
    TOGGLE_WIND = 1
    CONNECT_BATTERY = 2

# CHANGE: ActionModel -> IndustrialPowerGridAction  
class IndustrialPowerGridAction(BaseModel):
    model_config = ConfigDict(extra='ignore', str_strip_whitespace=False)
    
    action: int = Field(default=0, description="The energy source you want to toggle (0: Solar, 1: Wind, 2: Battery)")
    message: str = Field(default="", description="Optional message")

# CHANGE: ObservationModel -> IndustrialPowerGridObservation
class IndustrialPowerGridObservation(BaseModel):
    is_demand_met: bool = Field(description="True if power supply equals or exceeds demand")
    carbon_footprint: float = Field(description="A score from 0 to 1 (lower is better)")
    grid_stability: str = Field(description="Status of the grid: STABLE, WARNING, or CRITICAL")
    reward: float = Field(default=0.0, description="Reward for the current step")
    done: bool = Field(default=False, description="Whether the episode is done")