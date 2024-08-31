app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document

active_view = ui_doc.ActiveView
phases = {phase.Name: phase for phase in list(doc.Phases)}


def get_phase(phase_name):
    return phases.get(phase_name)


new_construction_phase = get_phase("New Construction")

existing_phase = get_phase("Existing")

demolishing_phase = get_phase("Demolishing")
