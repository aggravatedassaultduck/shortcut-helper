import toml
import shortcuts as sh

# load the TOML file
config = toml.load("config.toml")

plugin_config = config.get("plugins", {}).get("sh", {})
sound_options = config.get("misc", {}).get("sound_options")

# create the dictionary
plugins = {
    getattr(sh, key): keys 
    for key, keys in plugin_config.items()
}
