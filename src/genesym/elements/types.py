from typing import Dict, NewType


ScenarioIndex = NewType('ScenarioIndex', int)
IntervIndex = NewType('IntervIndex', int)
ElementName =  NewType('ElementName', str)
# the name that we use with ElementName in dataStore
# is not element.name, but we intend to represent a group of elements
# that are across scenarios and intervals,
# maybe Element is not a good name
# maybe ObjName
# also I got a bit confused here If We wish to Store the Element 
# itself, in a Data Store, then how would access the vars etc?
# Also Does An ElementGroup NEED to have ONE Element per Sceanrio/Interval or can have multiple
# well I feel that if I to replace ElementName with ObjName, then ElementStore, and all of it 
# would need to change, we would need to store Elements with this
# but we will also Need to Store Other Type of Objects

# VarName = NewType('VarName', str)