from .enums import ProfileOptions

USER_PROFILES_MAP = {
    ProfileOptions.superadmin: 1,
    ProfileOptions.admin: 2,
    ProfileOptions.employee: 3,
}


def get_group_id_by_profile(profile):
    """Returns the user group based on profile"""
    if profile:
        return USER_PROFILES_MAP.get(profile, 3)

    return USER_PROFILES_MAP.get(ProfileOptions.employee)


import json

json.dump()
