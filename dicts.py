def get_statuses_dict():
    statuses_dict = {
        "status_id": [2, 3, 4, 5],
        "status_name": ["Open", "Pending", "Resolved", "Closed"]
    }
    return statuses_dict


def get_sources_dict():
    sources_dict = {
        "source_id": [1, 2, 3, 7, 9, 10],
        "source_name": ["Email", "Portal", "Phone", "Chat", "Feedback Widget", "Outbound Email"]
    }
    return sources_dict


def get_priorities_dict():
    priority_dict = {
        "priority_id": [1, 2, 3, 4],
        "priority_name": ["Low", "Medium", "High", "Urgent"]
    }
    return priority_dict
