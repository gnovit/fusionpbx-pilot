from dynaconf import Dynaconf, Validator, ValidationError
import sys
import logging


# Dynaconf can´t yet validate lists :-(
# This is the workaround: https://github.com/rochacbruno/dynaconf/issues/676
def validate_user(users: list) -> bool:
    for user in users:
        if not user.name or not isinstance(user.name, str):
            raise ValidationError(f"User: {user} name must to be type str and not null")

        if not user.password or not isinstance(user.password, str):
            raise ValidationError(
                f"User: {user} password must to be type str and not null"
            )
    return True


# `envvar_prefix` = export envvars with `export FSCONNECTOR_FOO=bar`.
# `settings_files` = Load these files in the order.
settings = Dynaconf(
    envvar_prefix="FSCONNECTOR",
    settings_files=[
        "conf/settings.toml",
        "conf/.secrets.toml",
        "/etc/fusionpbx-pilot/settings.toml",
    ],
)
settings.validators.register(
    Validator("fusionpbx.url", is_type_of=str, must_exist=True),
    Validator("fusionpbx.password", is_type_of=str, must_exist=True),
    Validator("freeswitch.user", is_type_of=str, default="admin"),
    Validator("users", condition=validate_user),
)

try:
    settings.validators.validate()

except ValidationError as error:
    logging.error(f"Error validating config files: {error}")
    sys.exit(255)
