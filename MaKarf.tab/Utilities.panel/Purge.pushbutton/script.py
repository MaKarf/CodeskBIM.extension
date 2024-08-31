from Autodesk.Revit.DB import *
from System.Collections.Generic import List

from lib.UI.Popup import Alert

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Revit Transaction")
active_view = ui_doc.ActiveView


def get_purgeable_elements(rule_id_lst):
    failure_messages = PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, rule_id_lst)
    if failure_messages.Count > 0:
        purgeable_element_ids = failure_messages[0].GetFailingElements()
        return purgeable_element_ids


def run():
    # A constant
    purge_guid = "e8c63650-70b7-435a-9010-ec97660c1bda"

    """A generic list of PerformanceAdviserRuleIds as required by the ExecuteRules method"""
    rule_id_list = List[PerformanceAdviserRuleId]()

    """Iterating through all PerformanceAdviser rules looking to find that which matches PURGE_GUID"""
    for rule_id in PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds():
        if str(rule_id.Guid) == purge_guid:
            rule_id_list.Add(rule_id)
            break

    """Attempting to retrieve the elements which can be purged"""
    purgeable_element_ids = get_purgeable_elements(rule_id_list)

    if purgeable_element_ids is not None:

        t.Start()
        doc.Delete(purgeable_element_ids)
        t.Commit()
    else:
        out = "No elements left to purge"
        Alert(content="",
              title="Notification",
              header=out)


run()
