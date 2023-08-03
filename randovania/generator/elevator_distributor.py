from __future__ import annotations

import copy
from collections import defaultdict
from typing import TYPE_CHECKING

from randovania.game_description.db.dock_node import DockNode

if TYPE_CHECKING:
    from random import Random

    from randovania.game_description.db.dock import DockType
    from randovania.game_description.db.node_identifier import NodeIdentifier
    from randovania.game_description.db.region_list import RegionList
    from randovania.game_description.game_patches import ElevatorConnection


class ElevatorHelper:
    teleporter: NodeIdentifier
    destination: NodeIdentifier
    connected_elevator: ElevatorHelper | None

    def __init__(self, teleporter: NodeIdentifier, destination: NodeIdentifier):
        self.teleporter = teleporter
        self.destination = destination
        self.connected_elevator = None

    @property
    def region_name(self):
        return self.teleporter.area_location.region_name

    @property
    def area_name(self):
        return self.teleporter.area_location.area_name

    def connect_to(self, other: ElevatorHelper):
        self.destination = other.teleporter
        other.destination = self.teleporter
        self.connected_elevator = other
        other.connected_elevator = self

    @property
    def area_location(self):
        return self.teleporter.area_location


def try_randomize_elevators(rng: Random,
                            echoes_elevators: tuple[ElevatorHelper, ...],
                            ) -> list[ElevatorHelper]:
    elevator_database: list[ElevatorHelper] = list(echoes_elevators)
    assert len(elevator_database) % 2 == 0

    elevator_list = copy.copy(elevator_database)
    elevators_by_region: dict[str, list[ElevatorHelper]] = defaultdict(list)
    for elevator in elevator_list:
        elevators_by_region[elevator.region_name].append(elevator)

    while elevator_list:
        source_elevators: list[ElevatorHelper] = max(elevators_by_region.values(), key=len)
        target_elevators: list[ElevatorHelper] = [
            elevator
            for elevator in elevator_list
            if elevator not in source_elevators
        ]
        source_elevator = source_elevators[0]
        target_elevator = rng.choice(target_elevators)

        source_elevator.connect_to(target_elevator)

        elevators_by_region[source_elevator.region_name].remove(source_elevator)
        elevators_by_region[target_elevator.region_name].remove(target_elevator)
        elevator_list.remove(source_elevator)
        elevator_list.remove(target_elevator)

    # TODO
    list3 = copy.copy(elevator_database)
    celevator_list3 = [list3[0]]
    while list3:
        celevator_list1 = []
        for celevator1 in celevator_list3:
            index = 0
            while index < len(list3):
                celevator2 = list3[index]
                if (celevator2.region_name == celevator1.region_name
                        or celevator2.area_name == celevator1.destination.area_name):
                    celevator_list1.append(celevator2)
                    list3.remove(celevator2)
                else:
                    index += 1
        if celevator_list1:
            celevator_list3 = celevator_list1
        else:
            # Randomization failed
            return try_randomize_elevators(rng, echoes_elevators)

    return elevator_database


def two_way_elevator_connections(rng: Random,
                                 elevator_database: tuple[ElevatorHelper, ...],
                                 between_areas: bool
                                 ) -> ElevatorConnection:
    if len(elevator_database) % 2 != 0:
        raise ValueError("Two-way elevator shuffle, but odd number of elevators to shuffle.")
    if between_areas:
        elevator_database = try_randomize_elevators(rng, elevator_database)
    else:
        elevators = list(elevator_database)
        rng.shuffle(elevators)
        while elevators:
            elevators.pop().connect_to(elevators.pop())

    return {
        elevator.teleporter: elevator.connected_elevator.teleporter
        for elevator in elevator_database
    }


def one_way_elevator_connections(rng: Random,
                                 elevator_database: tuple[ElevatorHelper, ...],
                                 target_locations: list[NodeIdentifier],
                                 replacement: bool,
                                 ) -> ElevatorConnection:
    target_locations.sort()
    rng.shuffle(target_locations)

    def _create_target():
        if replacement:
            return rng.choice(target_locations)
        else:
            return target_locations.pop()

    return {
        elevator.teleporter: _create_target()
        for elevator in elevator_database
    }


def create_elevator_database(region_list: RegionList,
                             all_teleporters: list[NodeIdentifier],
                             allowed_dock_types: list[DockType]
                             ) -> tuple[ElevatorHelper, ...]:
    """
    Creates a tuple of Elevator objects, exclude those that belongs to one of the areas provided.
    :param region_list:
    :param all_teleporters: Set of teleporters to use
    :return:
    """
    all_helpers = [
        ElevatorHelper(region_list.identifier_for_node(node), node.default_connection.area_identifier)

        for region, area, node in region_list.all_regions_areas_nodes
        if isinstance(node, DockNode) and node.dock_type in allowed_dock_types
    ]
    return tuple(
        helper
        for helper in all_helpers
        if helper.teleporter in all_teleporters
    )
